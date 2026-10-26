"""calc.py를 SPEC.md「5. 손 계산 사례」기대값과 비교한다. 기대값은 SPEC에서만 가져온다."""
from calc import (apply_scenario, breakeven_qty_change, cost_ratio, loss_count, margin_ratio, pct1, profit_per_cup,
                  recovery_rate, round_won, sales_shares, sort_menus, summary)

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
NO_SALES = [{**AMERICANO, "qty": 0}, {**LATTE, "qty": 0}]
s = summary(NO_SALES, 5_000_000, FEE)
check("E2", "이유", s["reason"], "예상 판매량이 없음")

# C5: 대시보드 회수율·손해 메뉴 수, 매출 비중과 기본 정렬
check("C5", "회수율", pct1(recovery_rate(C2_MENUS, 5_000_000, FEE)), 92.1)
check("C5", "손해 메뉴 수", loss_count(C2_MENUS, FEE), 0)
check("C5", "매출 비중", [pct1(r) for r in sales_shares(C2_MENUS)], [61.5, 38.5])
check("C5", "순서", [m["name"] for m in sort_menus(C2_MENUS, "매출 비중", FEE)], ["아메리카노", "라떼"])

# C6: 매출이 같으면 마진율 높은 순. 넣는 순서를 기대 순서와 다르게 둬서 마진율 비교를 실제로 검사한다
C6_MENUS = [
    {"name": "초코라떼", "price": 5500, "cost": 1500, "qty": 100},
    {"name": "레모네이드", "price": 5500, "cost": 1300, "qty": 100},
    {"name": "딸기스무디", "price": 6500, "cost": 2200, "qty": 80},
    {"name": "망고스무디", "price": 6500, "cost": 2100, "qty": 80},
]
check("C6", "순서", [m["name"] for m in sort_menus(C6_MENUS, "매출 비중", FEE)], ["레모네이드", "초코라떼", "망고스무디", "딸기스무디"])

# C7·C8: C2에서 값 하나를 바꾼 월 이익
check("C7", "월 이익", round_won(summary([{**AMERICANO, "cost": 1500}, LATTE], 5_000_000, FEE)["monthly_profit"]), -893_000)
check("C8", "월 이익", round_won(summary([AMERICANO, {**LATTE, "qty": 0}], 5_000_000, FEE)["monthly_profit"]), -2_088_000)

# C9: C3 시나리오별 고정비 회수율
check("C9", "회수율 현재·A·B", [pct1(recovery_rate(ms, 5_000_000, FEE)) for ms in
                              (C2_MENUS, apply_scenario(C2_MENUS, 10, -10), apply_scenario(C2_MENUS, -10, 20))], [92.1, 94.4, 95.3])

# C10: 판매가만 바꿨을 때 지금 월 이익을 지키는 판매량 변화 (판매량 기준)
check("C10", "가격 +10%·−10%", [pct1(breakeven_qty_change(C2_MENUS, p, FEE)) for p in (10, -10)], [-12.1, 16.0])

# C11: 가격 변화별 판매량 기준표
check("C11", "가격 −20·−10·−5·+5·+10·+20%", [pct1(breakeven_qty_change(C2_MENUS, p, FEE)) for p in (-20, -10, -5, 5, 10, 20)],
      [38.1, 16.0, 7.4, -6.5, -12.1, -21.6])

# E3: C2에 손해 메뉴(E1 디저트) 추가
check("E3", "손해 메뉴 수", loss_count(C2_MENUS + [dessert], FEE), 1)

# E4: 1잔 이익이 정확히 0원이어도 손해 메뉴
check("E4", "1잔 이익", round_won(profit_per_cup(4400, 3912, FEE)), 0)
check("E4", "손해 메뉴 수", loss_count([{"name": "이익 0원", "price": 4400, "cost": 3912, "qty": 100}], FEE), 1)

# E5: 판매량 모두 0 → 비중 "-"(None), 회수율 "손익분기 없음"(None)
check("E5", "매출 비중", sales_shares(NO_SALES), [None, None])
check("E5", "회수율", recovery_rate(NO_SALES, 5_000_000, FEE), None)

# E6: 지금 남긴 돈이 0 이하면 판매량 기준을 계산할 수 없음
check("E6", "판매량 기준", breakeven_qty_change([dessert], 10, FEE), None)

print("\n".join(failures) if failures else "check ok")
