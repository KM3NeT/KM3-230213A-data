import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def E2Phi(norm: float, gamma: float, e0: float = 1, range: tuple = (-np.inf, np.inf)):
    """Energy-squared flux function for given normalisation, spectral index, and valid energy range."""
    
    return lambda x: np.where((x >= range[0]) & (x <= range[1]), x**2 * norm * np.power(x / e0, -gamma), np.nan)

def get_singlepowerlaw_iceCube(bestfit, contour68):
    """Returns the plotting ingredients for IceCube single power law fits."""
    
    x = np.logspace(np.log10(bestfit["range"][0]), 11, 2000)
    # in central 90% range
    ys = [E2Phi(n, g, bestfit["e0"], bestfit["range"])(x) for g, n in contour68[["SpectralIndex", "FluxNorm [GeV.cm^-2.s.sr]"]].to_numpy()]
    y_min = np.amin(ys, axis=0)
    y_max = np.amax(ys, axis=0)
    # extrapolated
    y = E2Phi(bestfit["norm"], bestfit["gamma"], bestfit["e0"])(x)
    ys_ext = [E2Phi(n, g, bestfit["e0"])(x) for g, n in contour68[["SpectralIndex", "FluxNorm [GeV.cm^-2.s.sr]"]].to_numpy()]
    yext_min = np.amin(ys_ext, axis=0)
    yext_max = np.amax(ys_ext, axis=0)
    
    return x, y, y_min, y_max, yext_min, yext_max

def get_segmented_icecube(fit):
    """Returns the plotting ingredients for IceCube segmented fits."""
    
    x = np.sqrt(fit["Emin [GeV]"] * fit["Emax [GeV]"])  # central bin energy
    xerr = [x - fit["Emin [GeV]"], fit["Emax [GeV]"] - x]
    y = fit["FluxNorm [GeV.cm^-2.s.sr]"]
    yerr = [fit["ErrorMinus [GeV.cm^-2.s.sr]"], fit["ErrorPlus [GeV.cm^-2.s.sr]"]]
    
    return x, y, xerr, yerr

class Flux:
    def __call__(self, energy: float | np.ndarray):
        return 0
    
class SinglePowerLawFlux(Flux):

    def __init__(self, norm: float, spectral_index: float, emin: float = 0, emax: float = np.inf, e0: float = 1):
        self.norm = norm
        self.spectral_index = spectral_index
        self.emin = emin
        self.emax = emax
        self.e0 = e0

    def __call__(self, energy: float | np.ndarray):
        return np.where((energy >= self.emin) & (energy < self.emax), self.norm * np.power(energy / self.e0, -self.spectral_index), 0)
    
class SEDFlux(Flux):
    
    def __init__(self, infile: str):
        df = pd.read_json(infile)
        self.x, self.y = df["Energy [GeV]"], df["log10(E^2 F(E) [GeV.cm^-2.s^-1.sr^-1])"]
        self.f = interp1d(self.x, self.y, bounds_error=False, fill_value=-np.inf)

    def __call__(self, energy: float | np.ndarray):
        return 10**self.f(energy) / energy**2