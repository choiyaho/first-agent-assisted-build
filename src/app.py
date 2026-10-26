"""calffeine 화면. 계산은 calc.py 함수를 호출하고, 여기서는 입력과 표시만 한다."""
from pathlib import Path

import pandas as pd
import streamlit as st

from calc import (SORT_BY, apply_scenario, cost_ratio, is_loss, loss_count, margin_ratio, pct1, profit_per_cup,
                  recovery_rate, round_won, sales_shares, sort_menus, summary)

# 가상의 예시 메뉴 (SPEC D9). 실행 위치와 상관없이 찾도록 app.py 옆의 파일을 읽는다
EXAMPLE = pd.read_csv(Path(__file__).parent / "menu.csv")
# 메뉴 그림(SVG 글자). menu.csv의 「그림」 열이 파일 이름이고, [+ 메뉴]로 추가한 메뉴는 기본 컵
PICTURES = {p.name: p.read_text() for p in (Path(__file__).parent / "images").glob("*.svg")}
# 메뉴 하나의 값. session_state의 f"{칸}_{메뉴 ID}"에만 둔다 → 고치는 곳이 한 군데 (SPEC D10). img는 입력 칸이 아님
FIELDS = ["name", "price", "cost", "qty", "img"]

# Streamlit 옵션으로 안 되는 화면 다듬기만 CSS로 한다. key를 준 위젯에는 Streamlit이 `st-key-<key>` 클래스를 붙인다
STYLE = """<style>
/* 한국어는 낱말 단위로 줄을 바꾼다 ("남깁니/다"처럼 글자 중간에서 끊기지 않게) */
.stApp, .stApp h1, .stApp h2, .stApp h3, .stApp p { word-break: keep-all !important; overflow-wrap: break-word; }

/* 로고: 기본 h1(2.75rem)의 2배 이상. 좁은 화면에서는 화면 폭에 맞춰 줄인다 */
[data-testid="stHeading"] h1 { font-size: clamp(3rem, 14vw, 6rem) !important; line-height: 1.1; }

/* 메뉴명·판매량·정렬 기준 칸: 평소엔 글자 길이에 맞추고, 누르면 끝까지 늘었다가, 다 쓰면 다시 글자에 맞춘다 */
/* 칸 묶음(라벨 포함) → 테두리 상자 → 글자 칸, 세 겹 모두 평소엔 내용 폭, 누르면(:focus-within) 끝까지 */
:root { interpolate-size: allow-keywords; }
[class*="st-key-name_"], [class*="st-key-qty_"], .st-key-sort_by { width: fit-content !important; max-width: 100%; }
[class*="st-key-qty_"] [data-testid="stNumberInputContainer"], .st-key-sort_by [role="group"] { width: fit-content; }
[class*="st-key-name_"] input, [class*="st-key-qty_"] input, .st-key-sort_by input { field-sizing: content; min-width: 3ch; }
[class*="st-key-name_"]:focus-within, [class*="st-key-qty_"]:focus-within, .st-key-sort_by:focus-within { width: 100% !important; }
[class*="st-key-qty_"]:focus-within [data-testid="stNumberInputContainer"], .st-key-sort_by:focus-within [role="group"] { width: 100%; }
[class*="st-key-name_"]:focus-within input, [class*="st-key-qty_"]:focus-within input, .st-key-sort_by:focus-within input { field-sizing: fixed; width: 100%; }
/* 정렬 기준은 목록 창이 칸 폭을 따라가므로 애니메이션 없이 바로 늘린다 */
[class*="st-key-name_"], [class*="st-key-qty_"] { transition: width .2s ease; }

/* 용어 설명: 접혀 있으면 제목 길이만큼, 펼치면 끝까지 */
.st-key-glossary details:not([open]) { width: fit-content; }

@media (prefers-reduced-motion: reduce) { [class*="st-key-"] { transition: none; } }
</style>"""


def won(x):
    """금액을 '1,234원' 문자열로. 반올림은 여기서만 한다."""
    return f"{round_won(x):,}원"


def pct(ratio):
    """비율을 '24.7%' 문자열로. 계산할 수 없으면 '-'."""
    p = pct1(ratio)
    return "-" if p is None else f"{p:.1f}%"


def be_text(s):
    """손익분기 결과를 (잔 수, 매출액) 문자열 쌍으로. 없으면 ('없음', '없음')."""
    if s["be_cups"] is None:
        return "없음", "없음"
    return f"{s['be_cups']:,}잔", f"{s['be_sales']:,}원"


def rate_text(rate):
    """고정비 회수율 문자열. 계산할 수 없으면 '손익분기 없음' (SPEC D12)."""
    return "손익분기 없음" if rate is None else pct(rate)


def menus_in_input_order():
    """지금 입력된 메뉴 목록 (먼저 넣은 순 = ID 순). 이름을 비우면 '(이름 없음)'."""
    ss = st.session_state
    return [
        {"id": i, "name": ss[f"name_{i}"] or "(이름 없음)", "price": ss[f"price_{i}"], "cost": ss[f"cost_{i}"],
         "qty": ss[f"qty_{i}"], "img": ss[f"img_{i}"]}
        for i in sorted(ss.order)
    ]


def put_menu(name, price, cost, qty, img="default.svg"):
    """새 메뉴에 ID를 주고 카드 맨 뒤에 붙인다 (SPEC D11·D16)."""
    ss = st.session_state
    i = ss.next_id
    ss.next_id += 1
    for f, v in zip(FIELDS, [name, int(price), int(cost), int(qty), img]):
        ss[f"{f}_{i}"] = v
    ss.order.append(i)


def resort():
    """고른 정렬 기준으로 카드 순서를 다시 정한다. 정렬 기준을 바꿀 때와 [다시 정렬]에서만 부른다 (SPEC D11)."""
    ss = st.session_state
    ss.order = [m["id"] for m in sort_menus(menus_in_input_order(), ss.sort_by, ss.fee_pct)]


def add_from_form():
    """[+ 메뉴] 양식에 넣은 값으로 메뉴를 추가한다."""
    ss = st.session_state
    put_menu(ss.new_name, ss.new_price, ss.new_cost, ss.new_qty)


def delete_menu(i):
    """메뉴 하나를 지운다. 다른 카드 순서는 그대로 (SPEC D16)."""
    ss = st.session_state
    ss.order.remove(i)
    for f in FIELDS:
        del ss[f"{f}_{i}"]


def draw_card(m, share, fee_pct):
    """메뉴 카드 하나: 그림, 이름·판매가·원가 입력, 1잔 이익과 비율, 손해 경고 (SPEC D10·D13)."""
    i = m["id"]
    st.image(PICTURES.get(m["img"], PICTURES["default.svg"]), width=96, alt=m["name"])
    st.text_input("메뉴명", key=f"name_{i}", placeholder="(이름 없음)", label_visibility="collapsed")
    left, right = st.columns(2)
    left.number_input("판매가 (원)", min_value=1, step=100, key=f"price_{i}", help="부가세 포함 메뉴판 가격")
    right.number_input("1잔 원가 (원)", min_value=0, step=100, key=f"cost_{i}", help="재료 + 포장")
    st.metric("1잔 이익", won(profit_per_cup(m["price"], m["cost"], fee_pct)))
    st.caption(
        f"원가율 {pct(cost_ratio(m['price'], m['cost'], fee_pct))}, "
        f"마진율 {pct(margin_ratio(m['price'], m['cost'], fee_pct))}, 매출 비중 {pct(share)}"
    )
    if is_loss(m["price"], m["cost"], fee_pct):
        st.error("1잔을 팔아도 남는 돈이 없습니다 (0원 이하). 판매가를 올리거나 원가를 줄여 보세요.")
    st.button("삭제", key=f"del_{i}", on_click=delete_menu, args=(i,), type="tertiary")


st.set_page_config(page_title="calffeine", page_icon="☕", layout="wide")
st.html(STYLE)  # style만 있으면 화면에 자리를 차지하지 않는다

# ① 사이드바: 고정비·수수료율 (SPEC D15: 고정비 1원 이상)
with st.sidebar:
    st.header("가게 정보")
    fixed_cost = st.number_input("월 고정비 (원)", min_value=1, value=5_000_000, step=100_000, key="fixed_cost",
                                 help="임대료·인건비·공과금 등. 사장님 본인 인건비도 포함하는 것을 권장합니다.")
    fee_pct = st.number_input("카드 수수료율 (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1, key="fee_pct",
                              help="결제 중 카드 비율을 감안한 평균 수수료율을 넣으세요.")

# 처음 열 때 한 번만 예시 메뉴를 채우고 기본 기준(매출 비중)으로 정렬한다
if "order" not in st.session_state:
    st.session_state.order, st.session_state.next_id = [], 0
    for _, r in EXAMPLE.iterrows():
        put_menu(r["메뉴"], r["판매가"], r["1잔 원가"], r["월 판매량"], r["그림"])
    st.session_state.order = [m["id"] for m in sort_menus(menus_in_input_order(), SORT_BY[0], fee_pct)]

menus = menus_in_input_order()
by_id = {m["id"]: m for m in menus}
shown = [by_id[i] for i in st.session_state.order]  # 카드에 보이는 순서

st.title("☕ calffeine")

# ② 대시보드(왼쪽)와 ③ 월 판매 계획(오른쪽): 판매량을 고치면 바로 옆 숫자가 바뀐다. 좁은 화면에서는 위아래 (SPEC D10·D12)
if menus:
    s = summary(menus, fixed_cost, fee_pct)
    rate = recovery_rate(menus, fixed_cost, fee_pct)
    profit = s["monthly_profit"]
    cups, sales = be_text(s)
    dash, plan = st.columns([3, 2], gap="large")
    with dash:
        if profit >= 0:
            st.subheader(f"이 계획대로면 한 달에 {won(profit)}을 남깁니다")
        else:
            st.subheader(f"이 계획대로면 한 달에 {won(-profit)} 적자입니다")
        if rate is not None:
            st.progress(float(min(rate, 1)), text=f"메뉴를 팔아 남긴 돈으로 고정비의 {pct(rate)}를 메웁니다")
        for label, value, meaning in [
            ("월 이익 (고정비 반영)", won(profit), "메뉴를 팔아 남긴 돈 − 월 고정비"),
            ("손익분기 판매량", cups, "본전이 되려면 한 달에 팔아야 하는 잔 수"),
            ("손익분기 매출액", sales, "본전이 되는 한 달 매출 (부가세 포함)"),
            ("고정비 회수율", rate_text(rate), "100% 이상이면 고정비를 다 메우고 남습니다"),
            ("손해 메뉴", f"{loss_count(menus, fee_pct)}개", "1잔 이익이 0원 이하인 메뉴 수"),
        ]:
            left, right = st.columns(2, vertical_alignment="center")
            left.markdown(f"**{label}**")
            left.caption(meaning)
            right.metric(label, value, label_visibility="collapsed")
        if s["be_cups"] is None:
            st.error(f"손익분기 없음 — {s['reason']}")

    # 판매량은 여기서만 고친다. 처음부터 펼쳐 둔다
    with plan, st.expander(f"월 판매 계획 (총 {sum(m['qty'] for m in menus):,}잔)", expanded=True):
        st.caption("메뉴별 예상 월 판매량입니다. 예측이 아니라 사장님이 세우는 가정값입니다.")
        cols = st.columns(2)
        for n, m in enumerate(shown):
            cols[n % 2].number_input(m["name"], min_value=0, step=10, key=f"qty_{m['id']}")
else:
    st.info("메뉴가 없습니다. 아래 메뉴판의 [+ 메뉴]로 첫 메뉴를 추가하세요.")

tab_menu, tab_scn = st.tabs(["메뉴판", "시나리오 비교"])

# ④ 메뉴판 카드 그리드 (SPEC D11·D16)
with tab_menu:
    a, b, c = st.columns([3, 1, 1], vertical_alignment="bottom")
    a.selectbox("정렬 기준", SORT_BY, key="sort_by", on_change=resort,
                help="값을 고쳐도 카드는 제자리에 있습니다. 바뀐 값으로 다시 줄 세우려면 [다시 정렬]을 누르세요.")
    b.button("다시 정렬", on_click=resort, width="stretch")
    with c.popover("+ 메뉴", width="stretch"):
        with st.form("add_menu", clear_on_submit=True):
            st.text_input("메뉴명", key="new_name")
            st.number_input("판매가 (부가세 포함, 원)", min_value=1, value=5000, step=100, key="new_price")
            st.number_input("1잔 원가 (재료+포장, 원)", min_value=0, value=1500, step=100, key="new_cost")
            st.number_input("월 판매량 (잔)", min_value=0, value=100, step=10, key="new_qty")
            st.form_submit_button("메뉴 추가", on_click=add_from_form)

    shares = dict(zip(by_id, sales_shares(menus)))
    for row in range(0, len(shown), 3):
        for col, m in zip(st.columns(3), shown[row:row + 3]):
            with col.container(border=True):
                draw_card(m, shares[m["id"]], fee_pct)

# ⑤ 시나리오 비교: "가격을 바꾸면 손님 수가 변해도 더 남나?"를 지금과 나란히 본다 (SPEC D7)
with tab_scn:
    if not menus:
        st.info("메뉴를 추가하면 시나리오를 비교할 수 있습니다.")
    else:
        st.subheader("가격을 바꾸면 한 달에 얼마나 남을까?")
        st.caption("가격을 올리면 손님이 줄고, 내리면 늘 수 있습니다. 두 가지 경우를 A안·B안으로 정해 지금과 비교해 보세요. "
                   "모든 메뉴에 같은 비율로 적용됩니다.")
        scenario_menus = {"지금": menus}
        for col, name, price0, qty0 in zip(st.columns(2, gap="large"), ["A", "B"], [10, -10], [-10, 20]):
            with col.container(border=True):
                st.markdown(f"**{name}안**")
                price = st.slider("판매가를 이만큼 바꾸면", -50, 50, price0, format="%+d%%", key=f"{name.lower()}_price")
                qty = st.slider("판매량은 이만큼 바뀔 것 같다", -50, 50, qty0, format="%+d%%", key=f"{name.lower()}_qty")
            scenario_menus[f"{name}안 (가격 {price:+d}%, 판매량 {qty:+d}%)"] = apply_scenario(menus, price, qty)
        scenarios = {k: summary(ms, fixed_cost, fee_pct) for k, ms in scenario_menus.items()}
        rates = {k: recovery_rate(ms, fixed_cost, fee_pct) for k, ms in scenario_menus.items()}

        st.markdown("**한 달에 남는 돈 (월 이익)**")
        now = scenarios["지금"]["monthly_profit"]
        for col, (k, v) in zip(st.columns(3), scenarios.items()):
            diff = v["monthly_profit"] - now  # 지금과의 차이: 두 계산 결과를 빼서 보여주기만 한다
            col.metric(k, won(v["monthly_profit"]), border=True,
                       delta=None if k == "지금" else ("+" if diff > 0 else "") + won(diff),
                       delta_description=None if k == "지금" else "지금보다")

        st.dataframe(
            pd.DataFrame(
                [
                    {"시나리오": k, "월 이익": won(v["monthly_profit"]), "손익분기 판매량": be_text(v)[0],
                     "손익분기 매출액": be_text(v)[1], "고정비 회수율": rate_text(rates[k])}
                    for k, v in scenarios.items()
                ]
            ),
            hide_index=True,
            width="stretch",
        )
        st.caption("판매량만 바꾸면 메뉴별 판매 비중이 그대로라 손익분기 판매량은 변하지 않습니다. "
                   "판매량 변화의 효과는 월 이익과 고정비 회수율에서 보입니다.")

with st.expander("용어 설명", key="glossary"):
    st.markdown(
        "- **1잔 이익** = 판매가 ÷ 1.1 − 원가 − 판매가 × 수수료율 (부가세는 사장님 몫이 아니라 뺍니다)\n"
        "- **원가율** = (원가 + 수수료) ÷ 판매가\n"
        "- **마진율** = 1잔 이익 ÷ 판매가\n"
        "- 원가율 + 마진율 = 90.9% (나머지 9.1%는 부가세)\n"
        "- **매출 비중** = 메뉴 매출(판매가 × 월 판매량) ÷ 전체 매출. 반올림 때문에 합이 100%가 아닐 수 있습니다.\n"
        "- **고정비 회수율** = 메뉴를 팔아 남긴 돈(1잔 이익 × 월 판매량의 합) ÷ 월 고정비. 100% 이상이면 흑자입니다.\n"
        "- **손해 메뉴** = 1잔 이익이 0원 이하인 메뉴\n"
        "- **손익분기** = 월 이익이 0원이 되는 판매량. 메뉴 판매 비중은 지금 입력한 그대로로 봅니다."
    )
