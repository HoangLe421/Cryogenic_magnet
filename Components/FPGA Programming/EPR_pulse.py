import numpy as np

class EPR_pulse:
    def __init__(self):
        # You can initialize default parameters here if desired.
        pass

    def Gaussian(self, amplitude=1.0, t0=0.0, sigma=1.0, t_min=-5.0, t_max=5.0, dt=0.01):
        """
        Generate a Gaussian pulse.
        
        Parameters:
            amplitude : float
                The peak amplitude of the pulse.
            t0 : float
                The center of the Gaussian.
            sigma : float
                The standard deviation of the Gaussian.
            t_min : float
                Start time of the time axis.
            t_max : float
                End time of the time axis.
            dt : float
                Time resolution (step size).
                
        Returns:
            t : numpy.ndarray
                The time axis.
            y : numpy.ndarray
                The Gaussian pulse amplitudes.
        """
        t = np.arange(t_min, t_max, dt)
        y = amplitude * np.exp(-((t - t0) ** 2) / (2 * sigma ** 2))
        return t, y

    def Square(self, amplitude=1.0, t_start=-1.0, t_end=1.0, t_min=-5.0, t_max=5.0, dt=0.01):
        """
        Generate a square pulse.
        
        Parameters:
            amplitude : float
                The amplitude of the pulse.
            t_start : float
                The start time for the pulse being "on".
            t_end : float
                The end time for the pulse being "on".
            t_min : float
                Start time of the time axis.
            t_max : float
                End time of the time axis.
            dt : float
                Time resolution.
                
        Returns:
            t : numpy.ndarray
                The time axis.
            y : numpy.ndarray
                The square pulse amplitudes.
        """
        t = np.arange(t_min, t_max, dt)
        y = np.zeros_like(t)
        y[(t >= t_start) & (t <= t_end)] = amplitude
        return t, y

    def Chirp(self, amplitude=1.0, f0=0.0, f1=10.0, t_min=0.0, t_max=5.0, dt=0.01):
        """
        Generate a linear chirp pulse.
        
        The instantaneous frequency increases linearly from f0 to f1 over the time span.
        
        Parameters:
            amplitude : float
                The amplitude of the pulse.
            f0 : float
                The starting frequency (Hz).
            f1 : float
                The ending frequency (Hz).
            t_min : float
                Start time of the time axis.
            t_max : float
                End time of the time axis.
            dt : float
                Time resolution.
                
        Returns:
            t : numpy.ndarray
                The time axis.
            y : numpy.ndarray
                The chirp pulse amplitudes.
        """
        t = np.arange(t_min, t_max, dt)
        # Linear frequency sweep constant
        k = (f1 - f0) / (t_max - t_min)
        # Instantaneous phase: phi(t) = 2pi*(f0*(t-t_min) + 0.5*k*(t-t_min)^2)
        phase = 2 * np.pi * (f0 * (t - t_min) + 0.5 * k * (t - t_min) ** 2)
        y = amplitude * np.cos(phase)
        return t, y

    def Triangle(self, amplitude=1.0, t_start=-1.0, t_peak=0.0, t_end=1.0, t_min=-5.0, t_max=5.0, dt=0.01):
        """
        Generate a triangle pulse.
        
        The pulse linearly rises from t_start to t_peak, and then falls linearly from t_peak to t_end.
        
        Parameters:
            amplitude : float
                The peak amplitude of the pulse.
            t_start : float
                The start time of the pulse.
            t_peak : float
                The time at which the pulse reaches its maximum amplitude.
            t_end : float
                The end time of the pulse.
            t_min : float
                Start time of the time axis.
            t_max : float
                End time of the time axis.
            dt : float
                Time resolution.
                
        Returns:
            t : numpy.ndarray
                The time axis.
            y : numpy.ndarray
                The triangle pulse amplitudes.
        """
        t = np.arange(t_min, t_max, dt)
        y = np.zeros_like(t)
        # Rising edge: from t_start to t_peak
        idx_rise = (t >= t_start) & (t <= t_peak)
        y[idx_rise] = amplitude * (t[idx_rise] - t_start) / (t_peak - t_start)
        # Falling edge: from t_peak to t_end
        idx_fall = (t > t_peak) & (t <= t_end)
        y[idx_fall] = amplitude * (t_end - t[idx_fall]) / (t_end - t_peak)
        return t, y

# Example usage:
if __name__ == '__main__':
    p = EPR_pulse()
    
    # Gaussian pulse example
    t_gauss, y_gauss = p.Gaussian(amplitude=2.0, t0=0.0, sigma=0.5)
    
    # Square pulse example
    t_square, y_square = p.Square(amplitude=1.0, t_start=-0.5, t_end=0.5)
    
    # Chirp pulse example
    t_chirp, y_chirp = p.Chirp(amplitude=1.0, f0=0.0, f1=20.0)
    
    # Triangle pulse example
    t_tri, y_tri = p.Triangle(amplitude=1.5, t_start=-1.0, t_peak=0.0, t_end=1.0)
    
    # You can plot the pulses using matplotlib (optional)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 8))
    
    plt.subplot(4, 1, 1)
    plt.plot(t_gauss, y_gauss)
    plt.title("Gaussian Pulse")
    
    plt.subplot(4, 1, 2)
    plt.plot(t_square, y_square)
    plt.title("Square Pulse")
    
    plt.subplot(4, 1, 3)
    plt.plot(t_chirp, y_chirp)
    plt.title("Chirp Pulse")
    
    plt.subplot(4, 1, 4)
    plt.plot(t_tri, y_tri)
    plt.title("Triangle Pulse")
    
    plt.tight_layout()
    plt.show()