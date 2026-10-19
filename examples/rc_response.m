R = 1e3;
C = 1e-6;
t = linspace(0, 5*R*C, 501);
v = 3.3 * (1 - exp(-t/(R*C)));
plot(t*1e3, v);
xlabel('Time [ms]'); ylabel('Voltage [V]'); grid on;
