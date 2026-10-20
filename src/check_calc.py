"""calc.py를 SPEC.md「5. 손 계산 사례」기대값과 비교한다. 기대값은 SPEC에서만 가져온다."""
from calc import apply_scenario, margin_ratio, cost_ratio, pct1, profit_per_cup, round_won, summary

FEE = 2  # SPEC 5번 공통 수수료율 2%
AMERICANO = {"name": "아메리카노", "price": 4400, "cost": 1000, "qty": 1000}
LATTE = {"name": "라떼", "price": 5500, "cost": 1500, "qty": 500}
C2_MENUS = [AMERICANO, LATTE]

failures = []


def check(case, label, got, expected):
    """기대값과 다르면 실패 목록에 남긴다."""
    if got != expected:
        failures.append(f"{case} {label}: 기대 {expected}, 실제 {got}")


# C1: 메뉴 하나의 마진
check("C1", "1잔 이익", round_won(profit_per_cup(4400, 1000, FEE)), 2912)
check("C1", "원가율", pct1(cost_ratio(4400, 1000, FEE)), 24.7)
check("C1", "마진율", pct1(margin_ratio(4400, 1000, FEE)), 66.2)

# C2: 손익분기
s = summary(C2_MENUS, 5_000_000, FEE)
check("C2", "손익분기 잔 수", s["be_cups"], 1628)
check("C2", "손익분기 매출액", s["be_sales"], 7_759_931)
check("C2", "월 이익", round_won(s["monthly_profit"]), -393_000)

# C3: 시나리오 A(가격 +10%, 판매량 −10%), B(가격 −10%, 판매량 +20%)
check("C3", "A 월 이익", round_won(summary(apply_scenario(C2_MENUS, 10, -10), 5_000_000, FEE)["monthly_profit"]), -281_570)
check("C3", "B 월 이익", round_won(summary(apply_scenario(C2_MENUS, -10, 20), 5_000_000, FEE)["monthly_profit"]), -234_440)

# C4: 나누어떨어지면 올림해도 1잔 더 나오지 않음
s = summary([AMERICANO], 2_912_000, FEE)
check("C4", "손익분기 잔 수", s["be_cups"], 1000)
check("C4", "손익분기 매출액", s["be_sales"], 4_400_000)

# E1: 손해 메뉴 → 손익분기 없음 (오류로 멈추지 않음)
dessert = {"name": "디저트", "price": 4400, "cost": 4000, "qty": 100}
check("E1", "1잔 이익", round_won(profit_per_cup(4400, 4000, FEE)), -88)
s = summary([dessert], 1_000_000, FEE)
check("E1", "손익분기 없음", (s["be_cups"], s["reason"] is not None), (None, True))

# E2: 판매량 모두 0 → 손익분기 없음
s = summary([{**AMERICANO, "qty": 0}, {**LATTE, "qty": 0}], 5_000_000, FEE)
check("E2", "이유", s["reason"], "예상 판매량이 없음")

print("\n".join(failures) if failures else "check ok")
