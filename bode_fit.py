from control import *
import numpy as np
from lmfit import Model
import inspect

def convert_magnitude_phase_to_complex (mag, phase_deg):
    """
    Parameters
    ----------
    mag: numpy array or object convertable using numpy.array(object) 
        Contains gain magnitude data corresponding to a specific frequency, with 
        associated phase angle. Units of gain. 
    phase_deg: numpy array or object convertable using numpy.array(object)    
        Contains phase data in degrees corresponding to a specific frequency. 
    """

    # Ensure that inputs are numpy arrays
    mag = np.array(mag)
    phase_deg = np.array(phase_deg)
    # Calculate the complex values
    cos = np.cos(phase_deg*np.pi/180)
    sin = np.sin(phase_deg*np.pi/180)*1j
    Z = np.multiply(mag,cos) + np.multiply(mag,sin)
    # Return complex vector
    return Z

class bode_fit: 
    """
    Attributes
    ----------
    transfer_function : 
    freqs_hz :
    Z_meas :
    model_function : 
    fit_model :
    params :
    result :
    v : 

    Methods
    -------
    fit()
    """

    def __init__(self, transfer_function, freqs_hz, Z_meas):
        """
        Parameters
        ----------
        transfer_function : 
        freqs_hz :
        Z_meas : 
        """

        self.transfer_function = transfer_function
        self.freqs_hz = freqs_hz
        self.Z_meas = Z_meas
        self.model_function = self._make_model_function()
        self.fit_model = Model(self.model_function)
        self.params = self._make_params()

    def _make_params(self):
        """
        internal method used upon instance creation

        Parameters
        ----------
        none 
        """
        params = self.fit_model.make_params()
        arglist = inspect.getfullargspec(self.transfer_function).args
        # TO-DO: Also get values if defaults are given in the transfer function. 
        print('params = ', arglist)
        for arg in arglist:
            params.add(arg)
            # Also set values if any
        return params

    def _make_model_function(self):
        """
        internal method used upon instance creation

        Parameters
        ----------
        none
        """
        def model(_frequencies, **kwargs):
            x = _frequencies*(2*np.pi)*1j
            Z = evalfr(self.transfer_function(**kwargs), x)
            # Since lmfit is aware of complex numbers, Z can be returned directly
            return Z
        # The signature of the returned model function will not contain the tranfer-
        # function's arguments as explicit positional arguments. It's made to work by 
        # using inspection in _make_params to separately generate the parameters. 
        # TO-DO: Possibly use functools or wrapt library to modify model's function 
        #   signature before its returned
        return model

    def fit(self):
        """
        Wrapper for lmfit's Model.fit method. Fits the data supplied to the model (Z_meas) 
        upon instance creation using the transfer function passed in as transfer_function. 

        fit results are stored in .result, and a condensed version of the fit coefficient 
        values are stored in *.v 
        
        Parameters
        ----------
        none 
        """
        self.result = self.fit_model.fit(self.Z_meas, self.params, _frequencies=self.freqs_hz)
        self.v = list(self.result.values.values())
        return self.result



