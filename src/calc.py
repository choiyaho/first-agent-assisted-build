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
