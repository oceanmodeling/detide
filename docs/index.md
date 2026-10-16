# detide

Best-practice de-tiding for water level time series

!!! Info "Created under the impulse of [surgeMIP](https://www.sciencedirect.com/science/article/pii/S2212094724000501)*'s need, in order to agree on a common methodology for de-tiding total water level time series"
    *_Storm surges and extreme sea levels: Review, establishment of model intercomparison and coordination of surge climate projection efforts_

!!! Success "Ideally, this methodology can help anyone looking for best practice in detiding water level time series"
    

## Quick start

```bash
git clone https://github.com/oceanmodeling/detide.git
cd detide 
pip install .
```

```python
import pandas as pd
from detide.harmonic import pytides_surge
from detide.constituents import FULL

df = pd.read_parquet("tests/data/cuxh.parquet")
surge = pytides_surge(df["elev"], constituents=FULL)
```

<iframe src="assets/plot_demo.html" width="100%" height="720" frameborder="0"></iframe>

!!! Warning  "Why [`pytides`](https://github.com/tomsail/pytides)?"
    UTide has a known bug with **nodal constituent corrections** over multi-year records. See details in the oceanmodeling [GitHub discussion](https://github.com/orgs/oceanmodeling/discussions/25)

    `pytides2`, however, handles nodal factors correctly and is pure Python

## How to detide:

### 1. Resample
You'd ideally to resample the signal to 60-min (default) means for the tidal analysis. This resolves up to M8 and keeps multi-decadal records manageable:
```python
def resample(ts: pd.Series, resample: int = 60) -> pd.Series:
    ts = ts.resample(f"{resample}min").mean()
    ts = ts.shift(freq=f"{resample / 2}min")  # Center the resampled points
    return ts.dropna()
```
### 2. Decompose

Decompose the tidal signal via `pytides2.Tide.decompose()` - least-squares fit of constituent amplitudes and phases: 
```python
def pytides_get_coefs_df(ts: pd.Series, constituents: list) -> pd.DataFrame:
    pytides_tide = pytides_get_coefs(ts, constituents)
    constituent_names = [c.name.upper() for c in pytides_tide.model["constituent"]]
    return pd.DataFrame(pytides_tide.model, index=constituent_names).drop(
        "constituent",
        axis=1,
    )
```
Visualize the Dataframe:
<iframe src="assets/tidal_decomposition_trst.html" width="100%" height="850" frameborder="0"></iframe>

### 3. Predict

Predict the tidal signal:

1. In most cases:  at the **original** (un-resampled) timestamps:

    ```python
    tide = pytides_get_coefs(ts, constituents)
    t0 = ts.index.to_pydatetime()[0]
    hours = (ts.index - ts.index[0]).total_seconds() / 3600
    times = Tide._times(t0, hours)
    tidal_prediction =  pd.Series(tide.at(times), index=ts.index)
    ```

2. *For SurgeMIP*: at the **resampled** timestamps - otherwise the intercomparison dataset is too big

    ```python
    tidal_prediction_hourly = resample(tidal_prediction) 
    ```

### 4. Subtract

Subtract to get the surge: residual = observed - tidal prediction

```python
surge =  pd.Series(ts.values, tide.at(times), index=ts.index)
```

### Full procedure for surge estimation

Gathering all 4 previous steps above in one script:
```python
import pandas as pd
from detide.constants import FULL
from detide.detide import pytides_surge
from detide.detide import pytides_get_coefs
from detide.detide import resample

df = pd.read_parquet("station.parquet")
ts = df["elev"]                 # must be a pd.Series
ts_hourly = resample(ts)        # resample the twl signal for the tidal analysis: faster harmonic analysis

coef = pytides_get_coefs(ts_hourly, FULL)
surge = pytides_surge(ts, coef)
surge_hourly = resample(surge)  # surgeMIP exception
```

## Constituent sets

| Set | Count | Use case |
|-----|------:|----------|
| `SHORT` | 20 | Pricipal contributors; dominant semi-diurnal + diurnal + overtides |
| `FULL` | 29 | **Default**; adds L2, T2, R2, ν2, μ2, λ2, S4, M8, M3 |
| `NOAA` | 37 | Direct comparison with NOAA CO-OPS tide predictions |
| `EXTENDED` | 67 | Adds many more minor and satellite constituents to obtain a Rayleigh Criterion of 0.8 |

<iframe src="assets/plot_compare_npor.html" width="100%" height="720" frameborder="0"></iframe>

## Output metadata

Parquet files should carry provenance metadata:

```python
{
    "lon": 8.7175,               # target lon/lat
    "lat": 53.867778,
    "mesh_lon": 8.706287,        # model grid point
    "mesh_lat": 53.874255,
    "mesh_index": 1372049,       # optional
    "distance": 1030.29,         # distance from mesh point to target (in meters)
    "model": "SCHISM",
    "exported_by": "EC-JRC",
    "depth": 10.632,             # optional
}
```

Much more info could be added. See GitHub discussion about [metadata](https://github.com/orgs/oceanmodeling/discussions/26)

## Structure of this repository 

As simple as possible:
```
├── README.md                   <- concept, redirection to docs
├── zensical.toml               <- docs build file
├── docs/
│   └── index.md                <- 1-page docs
├── detide/
│   ├── harmonic.py             <- detiding 
│   ├── constituents.py         <- constituents lists
│   └── plotting.py             <- plotting functions
└── tests/
    └── detide_example_test.py  <- generates the docs graphs
```


## Open questions

- [ ] Choose a consituent set
- [ ] Exclude Sa/Ssa from harmonic analysis to preserve seasonal signals?
- [ ] Add metadata after the de-tiding of the time series?
- [ ] Export and files formats? (zarr/netcdf/parquet etc.. `float32`, `float64` etc..)
- [ ] Add multi processing support? (using `dask`, `multifutures`, `joblib`?)


## Contribute 

 * Look at the [open issues](https://github.com/oceanmodeling/detide/issues)
 * Propose a modification:
    * (Create a Github Account)
    * Fork the repository
    * Push the changes on your fork
    * open a Pull Request
 * Participate in the open discussion
