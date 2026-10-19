* Educational Shichman-Hodges MOS model. Author-created parameters.
* Not fitted to any foundry, PDK, measured silicon, or technology node.
* Used only for functional transistor simulation and illustrative energy.
* This model does not support quantitative 45nm or Cadence GPDK45 claims.
.model nmos nmos level=1 vto=0.30 kp=200u lambda=0.05 gamma=0.4 phi=0.6 tox=3n cgso=200p cgdo=200p cbd=0.1f cbs=0.1f
.model pmos pmos level=1 vto=-0.30 kp=100u lambda=0.05 gamma=0.4 phi=0.6 tox=3n cgso=200p cgdo=200p cbd=0.1f cbs=0.1f
