import holoviews as hv
import pytest
import searvey

import ioc_cleanup as C

from detide.constants import SHORT, FULL, NOAA, EXTENDED

from detide.plotting import plot_df
from detide.plotting import plot_comparative_amplitudes

from detide.detide import pytides_surge
from detide.detide import pytides_get_coefs
from detide.detide import pytides_get_coefs_df
from detide.detide import resample


STATION = pytest.mark.parametrize(
    "station,sensor",
    [   #            station sensor
        pytest.param("npor", "bub", id="cuxh"),
        pytest.param("cuxh", "flt", id="cuxh"),
        pytest.param("trst", "aqu", id="brom"),
        pytest.param("brom", "aqu", id="brom"),
    ]
)

@STATION
def test_detide_plots(station, sensor):
    df = searvey.fetch_ioc_station(station, "2020-01-01", "2022-01-01")
    ts = C.clean(df, station, sensor)

    ts_hourly = resample(ts) # resample the twl signal for the tidal analysis: faster harmonic analysis

    # compute the surge signal for the 3 sets of tidal constituents
    surges = {}
    for astro, name in zip([SHORT, FULL, NOAA, EXTENDED], ["SHORT", "FULL", "NOAA", "EXTENDED"]):
        coef = pytides_get_coefs(ts_hourly, astro)
        surge = pytides_surge(ts, coef)
        surges[name] = resample(surge) # resample the surge signal: surgeMIP exception

    # plot #1: compare the original signal and the detided signal obtained
    plot_ = plot_df(ts_hourly, "Total Water Level signal", "k") \
        * plot_df(surges["EXTENDED"], "Detided Residual Signal", "r")
    hv.save(plot_.opts(height=700,responsive=True), "docs/assets/plot_demo.html")
    
    # plot #2: compare the surge signals obtained with the 3 sets of tidal constituents
    plot2_ = plot_df(ts_hourly, "Total Water Level signal", "k") \
        * plot_df(surges["SHORT"], "Detided Residual Signal - SHORT set of tidal constituents", "r") \
        * plot_df(surges["FULL"], "Detided Residual Signal - FULL set of tidal constituents", "g") \
        * plot_df(surges["NOAA"], "Detided Residual Signal - NOAA set of tidal constituents", "b") \
        * plot_df(surges["EXTENDED"], "Detided Residual Signal - EXTENDED set of tidal constituents", "purple")
    hv.save(plot2_.opts(height=700, responsive=True, title="Differences induced by different Harmonic subsets"), f"docs/assets/plot_compare_{station}.html")

    # plot #3: compare the amplitudes of the tidal constituents
    coef = pytides_get_coefs_df(ts_hourly, EXTENDED)
    hv.save(plot_comparative_amplitudes(coef, "amplitude"), f"docs/assets/tidal_decomposition_{station}.html")

