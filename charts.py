from __future__ import annotations

import plotly.graph_objects as go


BLUE = "#0B5ED7"
RED = "#D91E18"
GREEN = "#157A22"
PURPLE = "#6F1AB1"
GREY = "#666666"


def _axis_range(
    values,
    lower_padding: float = 0.15,
    upper_padding: float = 0.25,
):
    """Create a readable range for a numeric axis."""

    minimum = float(values.min())
    maximum = float(values.max())
    spread = maximum - minimum

    if spread == 0:
        spread = max(
            abs(maximum) * 0.10,
            1.0,
        )

    return [
        max(
            0,
            minimum
            - spread
            * lower_padding,
        ),
        maximum
        + spread
        * upper_padding,
    ]


def create_optimisation_chart(
    results_df,
    summary,
):
    """Create the interactive optimisation chart."""

    filling = results_df[
        "filling_target"
    ].to_numpy()

    yield_percentage = results_df[
        "yield_percentage"
    ].to_numpy()

    underweight = results_df[
        "underweight_percentage"
    ].to_numpy()

    good_units = results_df[
        "good_units"
    ].to_numpy()

    optimal_filling = summary[
        "optimal_filling"
    ]

    optimal_yield = summary[
        "optimal_yield"
    ]

    optimal_good_units = summary[
        "optimal_good_units"
    ]

    nominal_filling = summary[
        "nominal_filling_weight"
    ]

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=filling,
            y=yield_percentage,
            name="Filling Yield (%)",
            mode="lines+markers",
            line={
                "color": BLUE,
                "width": 2.2,
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
                    "produced_units",
                    "underweight_percentage",
                    "good_units",
                ]
            ].to_numpy(),
            hovertemplate=(
                "<b>Filling target:</b> %{x:.2f} g"
                "<br><b>Filling yield:</b> %{y:.2f}%"
                "<br><b>Adjustment:</b> %{customdata[0]:+.2f} g"
                "<br><b>Produced units:</b> %{customdata[1]:,.1f}"
                "<br><b>Underweight:</b> %{customdata[2]:.2f}%"
                "<br><b>Good units:</b> %{customdata[3]:,.1f}"
                "<extra></extra>"
            ),
        )
    )

    figure.add_trace(
        go.Scatter(
            x=filling,
            y=underweight,
            name="Underweight (%)",
            mode="lines+markers",
            line={
                "color": RED,
                "width": 2.2,
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

    figure.add_trace(
        go.Scatter(
            x=filling,
            y=good_units,
            name="Good Units",
            mode="lines+markers",
            line={
                "color": GREEN,
                "width": 2.2,
            },
            marker={
                "color": GREEN,
                "size": 5,
                "symbol": "triangle-up",
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
        x=nominal_filling,
        line={
            "color": GREY,
            "width": 1.6,
            "dash": "dot",
        },
        annotation_text="Nominal filling",
        annotation_position="top left",
        annotation_font={
            "color": GREY,
            "size": 10,
        },
    )

    figure.add_vline(
        x=optimal_filling,
        line={
            "color": PURPLE,
            "width": 2,
            "dash": "dash",
        },
        annotation_text="Selected filling",
        annotation_position="top right",
        annotation_font={
            "color": PURPLE,
            "size": 10,
        },
    )

    figure.add_trace(
        go.Scatter(
            x=[optimal_filling],
            y=[optimal_yield],
            name="Selected yield",
            mode="markers+text",
            marker={
                "color": BLUE,
                "size": 8,
                "line": {
                    "color": "white",
                    "width": 1.2,
                },
            },
            text=[
                f"Yield: {optimal_yield:.1f}%"
            ],
            textposition="top center",
            textfont={
                "color": BLUE,
                "size": 11,
            },
            yaxis="y",
            showlegend=False,
            hovertemplate=(
                "<b>Selected filling:</b> %{x:.2f} g"
                "<br><b>Filling yield:</b> %{y:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    figure.add_trace(
        go.Scatter(
            x=[optimal_filling],
            y=[optimal_good_units],
            name="Selected good units",
            mode="markers",
            marker={
                "color": "rgba(0,0,0,0)",
                "size": 10,
                "line": {
                    "color": PURPLE,
                    "width": 2,
                },
            },
            yaxis="y3",
            showlegend=False,
            hovertemplate=(
                f"<b>{summary['result_status']}</b>"
                "<br><b>Selected filling:</b> %{x:.2f} g"
                "<br><b>Good units:</b> %{y:,.1f}"
                f"<br><b>Yield:</b> {optimal_yield:.2f}%"
                f"<br><b>Underweight:</b> "
                f"{summary['optimal_underweight']:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    x_spread = (
        float(filling.max())
        - float(filling.min())
    )

    x_padding = max(
        0.5,
        x_spread * 0.04,
    )

    figure.update_layout(
        title={
            "text": (
                "Filling Target, Yield, Underweight "
                "and Good Units"
            ),
            "x": 0.5,
            "xanchor": "center",
            "font": {
                "size": 21,
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
            "l": 85,
            "r": 185,
            "t": 125,
            "b": 85,
        },
        xaxis={
            "title": (
                "Filling Target (g per unit)"
            ),
            "domain": [
                0.07,
                0.78,
            ],
            "range": [
                float(filling.min())
                - x_padding,
                float(filling.max())
                + x_padding,
            ],
            "showgrid": True,
            "gridcolor": (
                "rgba(128,128,128,0.18)"
            ),
            "zeroline": False,
            "fixedrange": False,
        },
        yaxis={
            "title": {
                "text": "Filling Yield (%)",
                "font": {
                    "color": BLUE,
                },
            },
            "tickfont": {
                "color": BLUE,
            },
            "linecolor": BLUE,
            "range": _axis_range(
                yield_percentage,
                lower_padding=0.18,
                upper_padding=0.28,
            ),
            "showgrid": True,
            "gridcolor": (
                "rgba(128,128,128,0.18)"
            ),
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
            "range": [
                0,
                max(
                    1.0,
                    float(underweight.max())
                    * 1.18,
                ),
            ],
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
            "range": _axis_range(
                good_units,
                lower_padding=0.20,
                upper_padding=0.35,
            ),
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
                    "Mouse wheel or toolbar: zoom. "
                    "Drag: select an area. "
                    "Double-click: reset."
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
