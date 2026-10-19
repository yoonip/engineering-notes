from math import exp

R, C, vin = 1000.0, 1e-6, 3.3
dt, steps = 1e-5, 500
v = 0.0
for _ in range(steps):
    v += dt * (vin - v) / (R * C)
t = dt * steps
exact = vin * (1.0 - exp(-t / (R * C)))
print(f"Euler={v:.6f}, analytic={exact:.6f}, error={abs(v-exact):.6f}")
