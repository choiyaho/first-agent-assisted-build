"""calffeine 화면. 계산은 calc.py 함수를 호출하고, 여기서는 입력과 표시만 한다."""
import pandas as pd
import streamlit as st

from calc import apply_scenario, cost_ratio, margin_ratio, pct1, profit_per_cup, round_won, summary

# 가상의 예시 메뉴 (SPEC D9). SPEC 5번 C2와 같은 값
EXAMPLE = pd.DataFrame(
    [
        {"메뉴": "아메리카노", "판매가": 4400, "1잔 원가": 1000, "월 판매량": 1000},
        {"메뉴": "라떼", "판매가": 5500, "1잔 원가": 1500, "월 판매량": 500},
    ]
)


def won(x):
    """금액을 '1,234원' 문자열로. 반올림은 여기서만 한다."""
    return f"{round_won(x):,}원"


def pct(ratio):
    """비율을 '24.7%' 문자열로. 계산할 수 없으면 '-'."""
    p = pct1(ratio)
    return "-" if p is None else f"{p:.1f}%"


def be_text(s):
    """손익분기 결과를 (잔 수, 매출액) 문자열 쌍으로. 없으면 ('없음', 이유)."""
    if s["be_cups"] is None:
        return "없음", s["reason"]
    return f"{s['be_cups']:,}잔", f"{s['be_sales']:,}원"


st.set_page_config(page_title="calffeine", page_icon="☕", layout="wide")
st.title("☕ calffeine")
st.caption("메뉴 가격을 감이 아니라 숫자로 정하기. 입력한 값은 저장되지 않습니다.")

# ① 사이드바: 고정비·수수료율
with st.sidebar:
    st.header("가게 정보")
    fixed_cost = st.number_input("월 고정비 (원)", min_value=0, value=5_000_000, step=100_000,
                                 help="임대료·인건비·공과금 등. 사장님 본인 인건비도 포함하는 것을 권장합니다.")
    fee_pct = st.number_input("카드 수수료율 (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1,
                              help="결제 중 카드 비율을 감안한 평균 수수료율을 넣으세요.")

# ② 메뉴 표 편집
st.subheader("1. 메뉴 입력")
edited = st.data_editor(
    EXAMPLE,
    num_rows="dynamic",
    width="stretch",
    column_config={
        "판매가": st.column_config.NumberColumn("판매가 (부가세 포함, 원)", step=100),
        "1잔 원가": st.column_config.NumberColumn("1잔 원가 (재료+포장, 원)", step=100),
        "월 판매량": st.column_config.NumberColumn("월 판매량 (잔)", step=10),
    },
)

# 빈 칸·음수 행은 계산에서 빼고 이유를 보여준다 (멈추지 않는다)
rows = edited.dropna(subset=["판매가", "1잔 원가", "월 판매량"])
bad = (rows[["판매가", "1잔 원가", "월 판매량"]] < 0).any(axis=1)
if len(rows) < len(edited):
    st.warning("판매가·원가·판매량 중 빈 칸이 있는 행은 계산에서 뺐습니다.")
if bad.any():
    st.warning("음수가 들어 있는 행은 계산에서 뺐습니다.")
rows = rows[~bad]
menus = [
    {"name": r["메뉴"] or "(이름 없음)", "price": int(r["판매가"]), "cost": int(r["1잔 원가"]), "qty": int(r["월 판매량"])}
    for _, r in rows.iterrows()
]
if not menus:
    st.info("계산할 메뉴가 없습니다. 위 표에 메뉴를 한 줄 이상 입력하세요.")
    st.stop()

s = summary(menus, fixed_cost, fee_pct)
be_cups, be_sales = be_text(s)

# ③④ 숫자 카드
st.subheader("2. 가게 전체")
c1, c2, c3 = st.columns(3)
c1.metric("월 이익 (고정비 반영)", won(s["monthly_profit"]))
c2.metric("손익분기 판매량", be_cups)
c3.metric("손익분기 매출액", be_sales)
if s["be_cups"] is None:
    st.error(f"손익분기 없음 — {s['reason']}")

tab_menu, tab_scn = st.tabs(["메뉴별 마진", "시나리오 비교"])

with tab_menu:
    table = pd.DataFrame(
        [
            {
                "메뉴": m["name"],
                "1잔 이익": won(profit_per_cup(m["price"], m["cost"], fee_pct)),
                "원가율": pct(cost_ratio(m["price"], m["cost"], fee_pct)),
                "마진율": pct(margin_ratio(m["price"], m["cost"], fee_pct)),
            }
            for m in menus
        ]
    )
    st.dataframe(table, hide_index=True, width="stretch")
    for m in menus:
        if profit_per_cup(m["price"], m["cost"], fee_pct) < 0:
            st.warning(f"⚠️ {m['name']}: 1잔을 팔 때마다 손해입니다. 판매가를 올리거나 원가를 줄여 보세요.")
    with st.expander("용어 설명"):
        st.markdown(
            "- **1잔 이익** = 판매가 ÷ 1.1 − 원가 − 판매가 × 수수료율 (부가세는 사장님 몫이 아니라 뺍니다)\n"
            "- **원가율** = (원가 + 수수료) ÷ 판매가\n"
            "- **마진율** = 1잔 이익 ÷ 판매가\n"
            "- 원가율 + 마진율 = 90.9% (나머지 9.1%는 부가세)\n"
            "- **손익분기** = 월 이익이 0원이 되는 판매량. 메뉴 판매 비중은 지금 입력한 그대로로 봅니다."
        )

with tab_scn:
    st.caption("전체 메뉴의 판매가와 판매량을 같은 비율로 바꿔 비교합니다.")
    a, b = st.columns(2)
    with a:
        st.markdown("**시나리오 A**")
        a_price = st.slider("A 판매가 변화 (%)", -50, 50, 10, key="a_price")
        a_qty = st.slider("A 판매량 변화 (%)", -50, 50, -10, key="a_qty")
    with b:
        st.markdown("**시나리오 B**")
        b_price = st.slider("B 판매가 변화 (%)", -50, 50, -10, key="b_price")
        b_qty = st.slider("B 판매량 변화 (%)", -50, 50, 20, key="b_qty")

    scenarios = {
        "현재": s,
        "A": summary(apply_scenario(menus, a_price, a_qty), fixed_cost, fee_pct),
        "B": summary(apply_scenario(menus, b_price, b_qty), fixed_cost, fee_pct),
    }
    st.dataframe(
        pd.DataFrame(
            [
                {"시나리오": k, "월 이익": won(v["monthly_profit"]), "손익분기 판매량": be_text(v)[0], "손익분기 매출액": be_text(v)[1]}
                for k, v in scenarios.items()
            ]
        ),
        hide_index=True,
        width="stretch",
    )
    chart = pd.DataFrame({"월 이익 (원)": [round_won(v["monthly_profit"]) for v in scenarios.values()]}, index=list(scenarios))
    st.bar_chart(chart)
