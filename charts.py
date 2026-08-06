from __future__ import annotations

import plotly.graph_objects as go


BLUE = "#0B5ED7"
RED = "#E1251B"
GREEN = "#15801E"
PURPLE = "#6F1AB1"
ORANGE = "#D97706"
GREY = "#686868"


def _positive_axis_range(
    values,
    top_padding: float,
    minimum_top: float,
):
    maximum = float(values.max())

    return [
        0,
        max(
            minimum_top,
            maximum * top_padding,
        ),
    ]


def create_optimisation_chart(
    results_df,
    summary,
):
    """
    Create three always-visible curves:

    - Production Yield
    - Underweight %
    - Good Units

    Production Yield and Good Units are mathematically proportional. Different
    line styles and slightly different axis padding keep both visible.
    """

    x = results_df["filling_target"]
    production_yield = results_df["production_yield"]
    underweight = results_df["underweight_percentage"]
    good_units = results_df["good_units"]

    figure = go.Figure()

    # Thick solid blue curve.
    figure.add_trace(
        go.Scatter(
            x=x,
            y=production_yield,
            name="Production Yield (%)",
            mode="lines+markers",
            line={
                "color": BLUE,
                "width": 3.2,
            },
            marker={
                "color": BLUE,
                "size": 4,
                "symbol": "circle",
            },
            yaxis="y",
            customdata=results_df[
                [
                    "filling_adjustment",
                    "actual_units",
                    "underweight_percentage",
                    "good_units",
                    "theoretical_filling_yield",
                ]
            ].to_numpy(),
            hovertemplate=(
                "<b>Filling target:</b> %{x:.2f} g"
                "<br><b>Adjustment vs target:</b> %{customdata[0]:+.2f} g"
                "<br><b>Production yield:</b> %{y:.2f}%"
                "<br><b>Actual units:</b> %{customdata[1]:,.1f}"
                "<br><b>Underweight:</b> %{customdata[2]:.2f}%"
                "<br><b>Good units:</b> %{customdata[3]:,.1f}"
                "<br><b>Yield before seconds:</b> %{customdata[4]:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    # Red curve on its own axis.
    figure.add_trace(
        go.Scatter(
            x=x,
            y=underweight,
            name="Underweight (%)",
            mode="lines+markers",
            line={
                "color": RED,
                "width": 2.5,
            },
            marker={
                "color": RED,
                "size": 4,
                "symbol": "square",
            },
            yaxis="y2",
            hovertemplate=(
                "<b>Filling target:</b> %{x:.2f} g"
                "<br><b>Underweight:</b> %{y:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    # Dashed green curve with open markers, drawn last so it remains visible
    # even though it has the same mathematical shape as production yield.
    figure.add_trace(
        go.Scatter(
            x=x,
            y=good_units,
            name="Good Units",
            mode="lines+markers",
            line={
                "color": GREEN,
                "width": 2.2,
                "dash": "dash",
            },
            marker={
                "color": "white",
                "size": 6,
                "symbol": "triangle-up-open",
                "line": {
                    "color": GREEN,
                    "width": 1.8,
                },
            },
            yaxis="y3",
            hovertemplate=(
                "<b>Filling target:</b> %{x:.2f} g"
                "<br><b>Good units:</b> %{y:,.1f}"
                "<extra></extra>"
            ),
        )
    )

    figure.add_vline(
        x=summary["target_filling_weight"],
        line={
            "color": GREY,
            "width": 1.6,
            "dash": "dot",
        },
        annotation_text="Target filling",
        annotation_position="top left",
        annotation_font={
            "color": GREY,
            "size": 10,
        },
    )

    figure.add_vline(
        x=summary["actual_filling_target"],
        line={
            "color": PURPLE,
            "width": 2,
            "dash": "dash",
        },
        annotation_text="Input scenario",
        annotation_position="top right",
        annotation_font={
            "color": PURPLE,
            "size": 10,
        },
    )

    figure.add_vline(
        x=summary["recommended_filling_target"],
        line={
            "color": ORANGE,
            "width": 2,
            "dash": "dashdot",
        },
        annotation_text="Optimum",
        annotation_position="bottom right",
        annotation_font={
            "color": ORANGE,
            "size": 10,
        },
    )

    figure.add_trace(
        go.Scatter(
            x=[summary["actual_filling_target"]],
            y=[summary["actual_production_yield"]],
            name="Input scenario point",
            mode="markers",
            marker={
                "color": PURPLE,
                "size": 10,
                "line": {
                    "color": "white",
                    "width": 1.2,
                },
            },
            yaxis="y",
            showlegend=False,
            hovertemplate=(
                "<b>Input scenario</b>"
                "<br><b>Filling target:</b> %{x:.2f} g"
                "<br><b>Production yield:</b> %{y:.2f}%"
                f"<br><b>Underweight:</b> "
                f"{summary['actual_underweight']:.2f}%"
                f"<br><b>Good units:</b> "
                f"{summary['actual_good_units']:,.1f}"
                "<extra></extra>"
            ),
        )
    )

    figure.add_trace(
        go.Scatter(
            x=[summary["recommended_filling_target"]],
            y=[summary["recommended_production_yield"]],
            name="Optimum point",
            mode="markers+text",
            marker={
                "color": ORANGE,
                "size": 10,
                "line": {
                    "color": "white",
                    "width": 1.2,
                },
            },
            text=[
                f"{summary['recommended_production_yield']:.1f}%"
            ],
            textposition="top center",
            textfont={
                "color": ORANGE,
                "size": 11,
            },
            yaxis="y",
            showlegend=False,
            hovertemplate=(
                "<b>Optimum scenario</b>"
                "<br><b>Filling target:</b> %{x:.2f} g"
                "<br><b>Production yield:</b> %{y:.2f}%"
                f"<br><b>Underweight:</b> "
                f"{summary['recommended_underweight']:.2f}%"
                f"<br><b>Good units:</b> "
                f"{summary['recommended_good_units']:,.1f}"
                "<extra></extra>"
            ),
        )
    )

    yield_range = _positive_axis_range(
        production_yield,
        top_padding=1.16,
        minimum_top=110,
    )

    underweight_range = _positive_axis_range(
        underweight,
        top_padding=1.15,
        minimum_top=1,
    )

    # Extra top padding intentionally separates the green curve visually from
    # the proportional blue curve without changing any data.
    good_units_range = _positive_axis_range(
        good_units,
        top_padding=1.34,
        minimum_top=max(
            100,
            summary["expected_units"] * 1.10,
        ),
    )

    figure.update_layout(
        title={
            "text": (
                "Production Yield, Underweight and Good Units "
                "by Filling Target"
            ),
            "x": 0.5,
            "xanchor": "center",
            "font": {
                "size": 20,
            },
        },
        height=720,
        template="plotly_white",
        hovermode="x unified",
        dragmode="zoom",
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.08,
            "xanchor": "center",
            "x": 0.5,
            "font": {
                "size": 11,
            },
        },
        margin={
            "l": 90,
            "r": 195,
            "t": 125,
            "b": 85,
        },
        xaxis={
            "title": "Filling Target (g per unit)",
            "domain": [0.07, 0.77],
            "autorange": "reversed",
            "showgrid": True,
            "gridcolor": "rgba(128,128,128,0.18)",
            "zeroline": False,
            "fixedrange": False,
        },
        yaxis={
            "title": {
                "text": "Production Yield (%)",
                "font": {
                    "color": BLUE,
                },
            },
            "tickfont": {
                "color": BLUE,
            },
            "linecolor": BLUE,
            "range": yield_range,
            "showgrid": True,
            "gridcolor": "rgba(128,128,128,0.18)",
            "zeroline": False,
            "fixedrange": False,
        },
        yaxis2={
            "title": {
                "text": "Underweight (%)",
                "font": {
                    "color": RED,
                },
            },
            "tickfont": {
                "color": RED,
            },
            "linecolor": RED,
            "overlaying": "y",
            "side": "right",
            "anchor": "x",
            "range": underweight_range,
            "showgrid": False,
            "zeroline": False,
            "fixedrange": False,
        },
        yaxis3={
            "title": {
                "text": "Good Units",
                "font": {
                    "color": GREEN,
                },
            },
            "tickfont": {
                "color": GREEN,
            },
            "linecolor": GREEN,
            "overlaying": "y",
            "side": "right",
            "anchor": "free",
            "position": 0.92,
            "range": good_units_range,
            "showgrid": False,
            "zeroline": False,
            "fixedrange": False,
        },
        annotations=[
            {
                "x": 0.5,
                "y": -0.16,
                "xref": "paper",
                "yref": "paper",
                "text": (
                    "Higher filling is shown on the left. "
                    "Use the mouse wheel or toolbar to zoom; "
                    "double-click to reset."
                ),
                "showarrow": False,
                "font": {
                    "size": 10,
                    "color": GREY,
                },
            }
        ],
    )

    return figure
