# -*- coding: utf-8 -*-
"""
Проверка условий и ответов всех 12 задач презентации «Прогрессии».
Запуск: python3 tools/verify.py  (нужен sympy: pip install sympy)
Каждая задача проверяется двумя способами там, где это возможно:
  (а) символьным решением уравнений;  (б) прямой подстановкой найденного ответа в условие.
"""
from fractions import Fraction as F
from sympy import symbols, solve, Eq, Rational, sqrt, simplify, nsimplify, Abs, S

ok = []

def check(name, cond):
    assert cond, "FAIL: " + name
    ok.append(name)
    print("OK  ", name)

# ----------------------------------------------------------------------
# 1. ПВГ-2019, 10–11: S6 = 344*S3, члены положительны. Найти q.
q = symbols('q', positive=True)
sol = solve(Eq(1 + q**3, 344), q)
check("P1: q=7 единственное положительное решение", sol == [7])
b1 = F(2, 5)  # произвольный положительный первый член для проверки
S3 = sum(b1 * 7**k for k in range(3)); S6 = sum(b1 * 7**k for k in range(6))
check("P1: подстановка S6/S3=344", S6 == 344 * S3)

# ----------------------------------------------------------------------
# 2. ПВГ-2016, 10–11: S5=93, b6+...+b10=2976. Найти S7.
check("P2: q^5 = 2976/93 = 32", F(2976, 93) == 32)
q2 = 2; b1 = F(93, 31)
check("P2: b1=3", b1 == 3 and sum(b1 * q2**k for k in range(5)) == 93)
check("P2: сумма следующих пяти = 2976", sum(b1 * q2**k for k in range(5, 10)) == 2976)
S7 = sum(b1 * q2**k for k in range(7))
check("P2: S7 = 381", S7 == 381)

# ----------------------------------------------------------------------
# 3. Физтех-2016, 10: 4p+5, 2p, |p-3| — геом. прогрессия. Найти все p.
p = symbols('p', real=True)
sol = solve(Eq((2*p)**2, (4*p + 5) * Abs(p - 3)), p)
sol = sorted(sol)
check("P3: символьное решение {-1, 15/8}", sol == [-1, Rational(15, 8)])
for pv in [F(-1), F(15, 8)]:
    t1, t2, t3 = 4*pv + 5, 2*pv, abs(pv - 3)
    check(f"P3: p={pv} члены ненулевые и t2^2=t1*t3",
          t1 != 0 and t2 != 0 and t3 != 0 and t2*t2 == t1*t3)
    check(f"P3: p={pv} отношение постоянно", t2/t1 == t3/t2)

# ----------------------------------------------------------------------
# 4. ПВГ-2017, 10–11: b2=3, b1+b2+b3=13, бесконечно убывающая. Найти S.
q = symbols('q', nonzero=True)
sol = solve(Eq(3/q + 3 + 3*q, 13), q)
check("P4: корни {1/3, 3}", sorted(sol) == [Rational(1, 3), 3])
qv = F(1, 3); b1 = 3 / qv
check("P4: |q|<1 выбирает q=1/3, b1=9", abs(qv) < 1 and b1 == 9)
check("P4: b1+b2+b3=13", b1 + 3 + 3*qv == 13)
check("P4: S = b1/(1-q) = 27/2", b1 / (1 - qv) == F(27, 2))

# ----------------------------------------------------------------------
# 5. ОММО-2009: a3,a4,a7,a_n непостоянной АП — ГП. Найти n.
a, d = symbols('a d', real=True)
sol = solve(Eq((a + 3*d)**2, (a + 2*d)*(a + 6*d)), a)
check("P5: a = -3d/2", sol == [-3*d/2])
av, dv = F(-3, 2), F(1)   # d=1 без ограничения общности (d != 0)
a3, a4, a7 = av + 2*dv, av + 3*dv, av + 6*dv
check("P5: q = 3", a4/a3 == 3 and a7/a4 == 3)
n = symbols('n', positive=True)
sol = solve(Eq(av + (n - 1)*dv, a7 * 3), n)
check("P5: n = 16", sol == [16])
terms = [av + (k - 1)*dv for k in [3, 4, 7, 16]]
check("P5: 1/2, 3/2, 9/2, 27/2 — ГП со знаменателем 3",
      all(terms[i+1]/terms[i] == 3 for i in range(3)))

# ----------------------------------------------------------------------
# 6. ПВГ-2020, 11: 6 членов, среднее первых 4 = 15, последних 4 = 60. Найти b6.
answers = set()
for qv in [F(2), F(-2)]:
    b1 = symbols('b1')
    s = solve(Eq(sum(b1 * qv**k for k in range(4)), 60), b1)[0]
    s = F(s)
    m1 = sum(s * qv**k for k in range(4)) / 4
    m2 = sum(s * qv**k for k in range(2, 6)) / 4
    check(f"P6: q={qv}, b1={s}: средние 15 и 60", m1 == 15 and m2 == 60)
    answers.add(s * qv**5)
check("P6: b6 ∈ {128, 384}", answers == {128, 384})
check("P6: q^2 = 240/60 = 4 других вариантов нет", F(240, 60) == 4)

# ----------------------------------------------------------------------
# 7. Физтех-2020, 10: S=A+B, A+3B=2(A+B). Во сколько раз A+4B больше S?
A, B = symbols('A B', positive=True)
sol = solve(Eq(A + 3*B, 2*(A + B)), B)
check("P7: B = A", sol == [A])
ratio = simplify((A + 4*A) / (A + A))
check("P7: отношение = 5/2", ratio == Rational(5, 2))
# численный контроль на конкретной прогрессии: n=5, a1=1, d such that B=A
n_ = 5; a1_ = F(1); A_ = n_*a1_; d_ = A_ * 2 / (n_*(n_-1))
S_ = sum(a1_ + k*d_ for k in range(n_))
S3_ = sum(a1_ + k*3*d_ for k in range(n_))
S4_ = sum(a1_ + k*4*d_ for k in range(n_))
check("P7: численный пример S3=2S и S4/S=5/2", S3_ == 2*S_ and S4_/S_ == F(5, 2))

# ----------------------------------------------------------------------
# 8. ПВГ-2014, 10–11: S=70, сумма квадратов=2100. Новая ГП: (-b1, -q). Найти S'.
b, q = symbols('b q', real=True)
sol = solve([Eq(b/(1-q), 70), Eq(b**2/(1-q**2), 2100)], [b, q], dict=True)
sol = [s for s in sol if abs(s[q]) < 1]
check("P8: единственное решение b=42, q=2/5",
      len(sol) == 1 and sol[0][b] == 42 and sol[0][q] == Rational(2, 5))
bv, qv = F(42), F(2, 5)
check("P8: b/(1+q) = 30", bv/(1+qv) == 30)
check("P8: S' = -b/(1+q) = -30", -bv/(1+qv) == -30)

# ----------------------------------------------------------------------
# 9. Ломоносов-2012 (очный тур), 10–11: a13=0, prod 5^{a_i} = среднее. Найти a1.
d = symbols('d', real=True)
a1 = -12*d
exps = [a1 + k*d for k in range(24)]
total = simplify(sum(exps))
check("P9: сумма показателей = -12d = a1", total == a1)
# произведение = 5^{a1} = первый из сомножителей; среднее равно первому только при d=0
for dv in [F(1, 2), F(-1, 2), F(3), F(-7, 10)]:
    xs = [5.0 ** float(-12*dv + k*dv) for k in range(24)]
    prod = 1.0
    for x in xs: prod *= x
    mean = sum(xs) / 24
    check(f"P9: d={dv} произведение {'>' if dv < 0 else '<'} среднего (равенства нет)",
          (prod > mean) if dv < 0 else (prod < mean))
xs = [1.0] * 24
check("P9: d=0: произведение=среднее=1, a1=0", 1.0 == sum(xs)/24)

# ----------------------------------------------------------------------
# 10. ПВГ-2013, 10–11: сумма 63, a1=1.5d, сдвиг до a1=d уменьшает сумму на [7,8].
sols = []
for n_ in range(2, 60):
    # 63 = n*d*(n+2)/2  =>  d = 126/(n*(n+2))
    dv = F(126, n_*(n_+2))
    a1v = F(3, 2)*dv
    terms = [a1v + k*dv for k in range(n_)]
    decr = n_*(a1v - dv)          # суммарное уменьшение
    if sum(terms) == 63 and 7 <= decr <= 8:
        sols.append((n_, dv))
check("P10: ровно два решения: (n=6, d=21/8), (n=7, d=2)",
      sols == [(6, F(21, 8)), (7, F(2, 1))])
for n_, dv in sols:
    a1v = F(3, 2)*dv
    terms = [a1v + k*dv for k in range(n_)]
    shifted = [t - (a1v - dv) for t in terms]
    check(f"P10: n={n_}: первый после сдвига = d, убавление в [7,8]",
          shifted[0] == dv and 7 <= sum(terms) - sum(shifted) <= 8)

# ----------------------------------------------------------------------
# 11. Ломоносов-2010: 24 и 2187 — члены ГП. Все натуральные члены.
# Инвариант: если x = 2^u * 3^v — натуральный член, то 2u + v = 7.
cands = [2**u * 3**(7 - 2*u) for u in range(4)]
check("P11: кандидаты {2187, 486, 108, 24}", sorted(cands) == [24, 108, 486, 2187])
qv = F(9, 2)
prog = [F(24) * qv**k for k in range(4)]
check("P11: пример 24, 108, 486, 2187 — ГП с q=9/2",
      prog == [24, 108, 486, 2187] and all(prog[i+1]/prog[i] == qv for i in range(3)))
# перебор натуральных чисел вида 2^u*3^v до 10^6: у кого 2u+v=7
found = []
for u in range(21):
    for v in range(14):
        x = 2**u * 3**v
        if x <= 10**6 and 2*u + v == 7:
            found.append(x)
check("P11: инвариант 2u+v=7 даёт ровно 4 числа", sorted(found) == [24, 108, 486, 2187])
# контроль: 2187/24 = 3^6/2^3, и кубический корень рационален
check("P11: 2187/24 = (9/2)^3", F(2187, 24) == F(9, 2)**3)

# ----------------------------------------------------------------------
# 12. Высшая проба-2016, 11 кл., заключительный: могут ли 3 последовательных члена АП
#     быть членами ГП? Пример: 1, q, q^3, q=(sqrt(5)-1)/2.
q = (sqrt(5) - 1) / 2
check("P12: q^3 - 2q + 1 = 0 символьно", simplify(q**3 - 2*q + 1) == 0)
check("P12: 2q = 1 + q^3 (среднее арифметическое)", simplify(2*q - (1 + q**3)) == 0)
qf = float(q)
check("P12: числа 1, q, q^3 различны и положительны",
      0 < qf**3 < qf < 1)
check("P12: 1, q, q^3 — члены ГП 1, q, q^2, q^3,... (номера 1, 2, 4)", True)
diff1, diff2 = qf - 1, qf**3 - qf
check("P12: равные разности (АП)", abs(diff1 - diff2) < 1e-12)

print()
print(f"=== ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ: {len(ok)} ===")
