import pandas as pd
import holoviews as hv
import hvplot.pandas

def ylabel(param: str) -> str: 
    if param == "amplitude": 
        return "Amplitude"
    elif param == "phase":
        return "Phase"


def plot_comparative_amplitudes(
    df: pd.DataFrame,
    param: str,
):

    return (
        df[param].iloc[::-1]
        .hvplot.barh(
            ylabel=ylabel(param),
            xlabel="Tidal Constituent",
            grid=True,
            title=f"Tidal Decomposition",
            legend="top_right",
            rot=90,
        )
        .opts(
            width=600,
            height=800,
            fontsize={"title": 13, "labels": 12, "xticks": 8, "yticks": 8},
            line_color=None,
            show_legend=True,
            bar_width=0.8,
            default_tools=["pan"],
        )
    )


def plot_df(df: pd.DataFrame, label: str, color: str) -> hv.Curve:
    ts = df.copy()
    ts = ts.iloc[-744:] # last 31 days
    ts = ts - ts.mean()
    return ts.hvplot(label=label, c=color, responsive = True, grid = True)
