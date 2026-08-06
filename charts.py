import plotly.graph_objects as go


BLUE = "#0B5ED7"
RED = "#D91E18"
GREEN = "#157A22"
PURPLE = "#6F1AB1"
GREY = "#666666"


def _axis_range(values, lower_padding=0.15, upper_padding=0.25):
    """Return a readable axis range with proportional padding."""

    minimum = float(values.min())
    maximum = float(values.max())
    spread = maximum - minimum

    if spread == 0:
        spread = max(abs(maximum) * 0.10, 1.0)

    return [
        max(0, minimum - spread * lower_padding),
        maximum + spread * upper_padding,
    ]


def create_optimisation_chart(
    results_df,
    summary,
):
    """
    Create an interactive Plotly chart.

    The chart supports:
    - Mouse-wheel zoom
    - Drag-to-zoom
    - Zoom-in and zoom-out buttons
    - Pan
    - Autoscale
    - Reset axes
    - Hover details
    """

    filling = results_df["filling_target"].to_numpy()
    yield_percentage = results_df["yield_percentage"].to_numpy()
    underweight = results_df["underweight_percentage"].to_numpy()
    good_units = results_df["good_units"].to_numpy()

    optimal_filling = summary["optimal_filling"]
    optimal_yield = summary["optimal_yield"]
    optimal_underweight = summary["optimal_underweight"]
    optimal_good_units = summary["optimal_good_units"]
    nominal_filling = summary["nominal_filling_weight"]

    figure = go.Figure()

    # Smaller markers keep the chart clear when many scenarios are tested.
    figure.add_trace(
        go.Scatter(
            x=filling,
            y=yield_percentage,
            name="Filling Yield (%)",
            mode="lines+markers",
            line={
                "color": BLUE,
                "width": 2.3,
            },
            marker={
                "color": BLUE,
                "size": 5,
                "symbol": "circle",
            },
            yaxis="y",
            customdata=results_df[
                [
                    "filling_adjustment",
                    "underweight_percentage",
                    "good_units",
                ]
            ].to_numpy(),
            hovertemplate=(
                "<b>Filling target:</b> %{x:.2f} g"
                "<br><b>Filling yield:</b> %{y:.2f}%"
                "<br><b>Adjustment vs nominal:</b> %{customdata[0]:+.2f} g"
                "<br><b>Underweight:</b> %{customdata[1]:.2f}%"
                "<br><b>Good units:</b> %{customdata[2]:,.1f}"
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
                "width": 2.3,
            },
            marker={
                "color": RED,
                "size": 5,
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
                "width": 2.3,
            },
            marker={
                "color": GREEN,
                "size": 6,
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

    # Nominal and selected filling reference lines.
    figure.add_vline(
        x=nominal_filling,
        line={
            "color": GREY,
            "width": 1.7,
            "dash": "dot",
        },
        annotation_text="Nominal filling",
        annotation_position="top left",
        annotation_font={
            "color": GREY,
            "size": 11,
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
            "size": 11,
        },
    )

    # Highlight the selected yield point without using a large marker.
    figure.add_trace(
        go.Scatter(
            x=[optimal_filling],
            y=[optimal_yield],
            name="Selected Yield",
            mode="markers+text",
            marker={
                "color": BLUE,
                "size": 9,
                "line": {
                    "color": "white",
                    "width": 1.5,
                },
            },
            text=[f"Yield: {optimal_yield:.1f}%"],
            textposition="top center",
            textfont={
                "color": BLUE,
                "size": 12,
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

    # Highlight the selected good-units point with a small open marker.
    figure.add_trace(
        go.Scatter(
            x=[optimal_filling],
            y=[optimal_good_units],
            name="Selected Good Units",
            mode="markers",
            marker={
                "color": "rgba(0,0,0,0)",
                "size": 11,
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
                f"<br><b>Underweight:</b> {optimal_underweight:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    x_padding = max(
        0.5,
        (float(filling.max()) - float(filling.min())) * 0.04,
    )

    figure.update_layout(
        title={
            "text": (
                "Filling Target, Production Yield, "
                "Underweight and Good Units"
            ),
            "x": 0.5,
            "xanchor": "center",
            "font": {
                "size": 22,
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
            "title": "Filling Target (g per unit)",
            "domain": [0.07, 0.78],
            "range": [
                float(filling.max()) + x_padding,
                float(filling.min()) - x_padding,
            ],
            "showgrid": True,
            "gridcolor": "rgba(128,128,128,0.18)",
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
            "range": [
                0,
                max(
                    1.0,
                    float(underweight.max()) * 1.18,
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
                    "Use the mouse wheel or the toolbar to zoom. "
                    "Drag to select an area. Double-click to reset."
                ),
                "showarrow": False,
                "font": {
                    "size": 11,
                    "color": GREY,
                },
            }
        ],
    )

    return figure
