# controls-tools

Helper functions and utilities to add more visualization and system identification functionality to the [Python Control Systems Library](https://python-control.readthedocs.io/) package. 

- *bode_overlay.py* overlays transfer function bode plots onto complex domain frequency response measurements.
- *bode_fit.py* contains a class that converts a transfer function into a fit model function and uses lmfit's Model class to determine an optimized parameter set. 

Similarities to [impedance.py](https://github.com/ECSHackWeek/impedance.py). Originally the fitting technique based on curve-fit was copied exact, but then replaced with lmfit.Model to provide an easier interface to the parameter bounds and initialization. lmfit.Model also contains built-in provisions for fitting complex numbers. 

### Dependencies
- bokeh
- lmfit
- [python-control](https://github.com/python-control/python-control)
- inspect
- numpy