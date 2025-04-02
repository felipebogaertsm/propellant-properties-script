from CoolProp.CoolProp import PropsSI
import numpy as np
import plotly.graph_objects as go


def plot_propellant_density_with_temperature(
    propellants: list[str], temperature_range: tuple[int, int], resolution: int
) -> None:
    """
    Plots the density of one or more propellants as a function of temperature at 1 atm.

    Args:
        propellants: List of propellant names (CoolProp-compatible).
        temperature_range: Tuple with (T_min, T_max) in Kelvin.
        resolution: Number of temperature points to evaluate.
    """
    temperatures = np.linspace(temperature_range[0], temperature_range[1], resolution)
    fig = go.Figure()

    for propellant in propellants:
        densities = []
        for T in temperatures:
            try:
                rho = PropsSI("D", "T", T, "P", 101325, propellant)
            except ValueError:
                rho = np.nan  # Skip invalid states (e.g. near phase change)
            densities.append(rho)

        fig.add_trace(
            go.Scatter(
                x=temperatures,
                y=densities,
                mode="lines+markers",
                name=f"{propellant} Density",
                line=dict(shape="spline"),
            )
        )

    fig.update_layout(
        title="Propellant Density vs Temperature at 1 atm",
        xaxis_title="Temperature [K]",
        yaxis_title="Density [kg/m³]",
        template="plotly_dark",
        hovermode="x unified",
    )

    fig.show()


if __name__ == "__main__":
    temperature_range = (273, 323)  # in Kelvin
    plot_propellant_density_with_temperature(
        propellants=["N2O", "H2O2"],
        temperature_range=temperature_range,
        resolution=50,
    )
