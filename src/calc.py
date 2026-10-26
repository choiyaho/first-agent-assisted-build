"""calffeine 계산 함수. 화면(Streamlit)과 분리해 따로 검사할 수 있게 둔다.

계산은 Fraction(분수)으로 정확하게 하고, 반올림은 화면 표시할 때만 한다 (SPEC D8).
메뉴 하나는 {"name", "price", "cost", "qty"} 딕셔너리다.
"""
from fractions import Fraction
from math import ceil, floor

VAT = Fraction(11, 10)  # 판매가 = 공급가 × 1.1 (SPEC D3)


def fee(price, fee_pct):
    """1잔 카드 수수료 = 판매가 × 수수료율(%)."""
    return Fraction(price) * Fraction(str(fee_pct)) / 100


def profit_per_cup(price, cost, fee_pct):
    """1잔 이익 = 공급가 − 원가 − 수수료 (SPEC D4)."""
    return Fraction(price) / VAT - Fraction(cost) - fee(price, fee_pct)


def cost_ratio(price, cost, fee_pct):
    """원가율 = (원가 + 수수료) ÷ 판매가. 판매가 0이면 None."""
    if price == 0:
        return None
    return (Fraction(cost) + fee(price, fee_pct)) / Fraction(price)


def margin_ratio(price, cost, fee_pct):
    """마진율 = 1잔 이익 ÷ 판매가. 판매가 0이면 None."""
    if price == 0:
        return None
    return profit_per_cup(price, cost, fee_pct) / Fraction(price)


def summary(menus, fixed_cost, fee_pct):
    """가게 전체 월 이익과 손익분기 잔 수·매출액. 손익분기가 없으면 None과 이유 (SPEC D5)."""
    total_qty = sum(Fraction(m["qty"]) for m in menus)
    total_profit = sum(profit_per_cup(m["price"], m["cost"], fee_pct) * Fraction(m["qty"]) for m in menus)
    total_sales = sum(Fraction(m["price"]) * Fraction(m["qty"]) for m in menus)
    result = {"monthly_profit": total_profit - fixed_cost, "be_cups": None, "be_sales": None, "reason": None}
    if total_qty == 0:
        result["reason"] = "예상 판매량이 없음"
    elif total_profit <= 0:
        result["reason"] = "메뉴를 팔수록 손해라 판매량을 늘려도 본전에 닿지 않음"
    else:
        # 정수·분수로 곱한 뒤 마지막에 한 번 나누고 올림 (CLAUDE.md 검증 규칙)
        result["be_cups"] = ceil(Fraction(fixed_cost) * total_qty / total_profit)
        result["be_sales"] = ceil(Fraction(fixed_cost) * total_sales / total_profit)
    return result


def recovery_rate(menus, fixed_cost, fee_pct):
    """고정비 회수율 = Σ(1잔 이익×판매량) ÷ 월 고정비. Σ ≤ 0이면 None("손익분기 없음") (SPEC D12)."""
    total_profit = sum(profit_per_cup(m["price"], m["cost"], fee_pct) * Fraction(m["qty"]) for m in menus)
    return None if total_profit <= 0 else total_profit / Fraction(fixed_cost)


def sales_shares(menus):
    """메뉴별 매출 비중 = 판매가×판매량 ÷ 총매출. 총매출이 0이면 모두 None (SPEC D11)."""
    sales = [Fraction(m["price"]) * Fraction(m["qty"]) for m in menus]
    total = sum(sales)
    return [None if total == 0 else s / total for s in sales]


def is_loss(price, cost, fee_pct):
    """손해 메뉴 = 1잔 이익 ≤ 0원 (SPEC D13)."""
    return profit_per_cup(price, cost, fee_pct) <= 0


def loss_count(menus, fee_pct):
    """손해 메뉴 수."""
    return sum(is_loss(m["price"], m["cost"], fee_pct) for m in menus)


SORT_BY = ["매출 비중", "마진율", "1잔 이익", "판매가", "입력 순서"]


def sort_menus(menus, by, fee_pct):
    """카드 순서: 고른 기준 높은 순 → 같으면 마진율 높은 순 → 같으면 입력 순서 (SPEC D11)."""
    if by == "입력 순서":
        return list(menus)

    def key(m):
        margin = margin_ratio(m["price"], m["cost"], fee_pct)
        first = {
            "매출 비중": Fraction(m["price"]) * Fraction(m["qty"]),  # 분모(총매출)가 같아 매출 순서 = 비중 순서
            "마진율": margin,
            "1잔 이익": profit_per_cup(m["price"], m["cost"], fee_pct),
            "판매가": Fraction(m["price"]),
        }[by]
        return (-first, -margin)

    # sorted는 같은 값이면 원래 순서를 지키므로 입력 순서가 마지막 기준이 된다
    return sorted(menus, key=key)


def apply_scenario(menus, price_pct, qty_pct):
    """모든 메뉴의 판매가와 판매량을 %만큼 바꾼 새 메뉴 목록 (SPEC D7)."""
    p = 1 + Fraction(str(price_pct)) / 100
    q = 1 + Fraction(str(qty_pct)) / 100
    return [{**m, "price": Fraction(m["price"]) * p, "qty": Fraction(m["qty"]) * q} for m in menus]


def round_won(x):
    """원 단위 사사오입 (0.5는 0에서 먼 쪽으로). Python round()는 짝수 쪽으로 보내서 쓰지 않는다."""
    x = Fraction(x)
    return floor(x + Fraction(1, 2)) if x >= 0 else -floor(-x + Fraction(1, 2))


def pct1(ratio):
    """비율을 소수 1자리 % 숫자로 (0.2473 → 24.7). None이면 None."""
    return None if ratio is None else round_won(ratio * 1000) / 10
