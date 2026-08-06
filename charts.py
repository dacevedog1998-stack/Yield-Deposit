from __future__ import annotations

import io

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch


BLUE = "#0757C9"
RED = "#D91E18"
GREEN = "#087A20"
PURPLE = "#6F1AB1"
ORANGE = "#E67E00"
GREY = "#777777"
LIGHT_GRID = "#D8D8D8"
SUMMARY_BACKGROUND = "#FFF9E8"
SUMMARY_BORDER = "#C8B98A"


def _representative_indices(
    total_points: int,
    requested_labels: int = 8,
) -> np.ndarray:
    """Return evenly spaced indices for readable data labels."""

    number_of_labels = min(
        requested_labels,
        total_points,
    )

    return np.unique(
        np.linspace(
            0,
            total_points - 1,
            number_of_labels,
            dtype=int,
        )
    )


def create_optimisation_chart(
    results_df,
    summary,
):
    """
    Create a static chart matching the approved preview format.

    Curves:
    - Blue: Yield based on Actual Units / Expected Units.
    - Red: Underweight percentage.
    - Green: Good Units after expected seconds are removed.
    """

    x = results_df[
        "filling_target"
    ].to_numpy()

    yield_values = results_df[
        "yield_percentage"
    ].to_numpy()

    underweight_values = results_df[
        "underweight_percentage"
    ].to_numpy()

    good_units_values = results_df[
        "good_units"
    ].to_numpy()

    figure, yield_axis = plt.subplots(
        figsize=(14.5, 9.2),
        dpi=120,
    )

    figure.subplots_adjust(
        left=0.08,
        right=0.80,
        top=0.82,
        bottom=0.25,
    )

    underweight_axis = (
        yield_axis.twinx()
    )

    good_units_axis = (
        yield_axis.twinx()
    )

    good_units_axis.spines[
        "right"
    ].set_position(
        (
            "axes",
            1.12,
        )
    )

    yield_line = yield_axis.plot(
        x,
        yield_values,
        color=BLUE,
        linewidth=2.4,
        marker="o",
        markersize=4.5,
        label="Yield (%)",
        zorder=4,
    )[0]

    underweight_line = (
        underweight_axis.plot(
            x,
            underweight_values,
            color=RED,
            linewidth=2.3,
            marker="s",
            markersize=4.5,
            label="% Underweight (Seconds)",
            zorder=3,
        )[0]
    )

    good_units_line = (
        good_units_axis.plot(
            x,
            good_units_values,
            color=GREEN,
            linewidth=2.3,
            marker="^",
            markersize=5,
            label="Good Units",
            zorder=2,
        )[0]
    )

    yield_axis.set_title(
        (
            "Relationship between Filling Target, Yield, "
            "% Underweight and Good Units"
        ),
        fontsize=20,
        fontweight="bold",
        pad=78,
    )

    yield_axis.set_xlabel(
        "Filling Target (g per unit)",
        fontsize=12,
        labelpad=12,
    )

    yield_axis.set_ylabel(
        "Yield (%)",
        color=BLUE,
        fontsize=13,
        fontweight="bold",
    )

    underweight_axis.set_ylabel(
        "% Underweight (Seconds)",
        color=RED,
        fontsize=13,
        fontweight="bold",
        labelpad=12,
    )

    good_units_axis.set_ylabel(
        "Good Units",
        color=GREEN,
        fontsize=13,
        fontweight="bold",
        labelpad=16,
    )

    yield_axis.tick_params(
        axis="y",
        colors=BLUE,
    )

    underweight_axis.tick_params(
        axis="y",
        colors=RED,
    )

    good_units_axis.tick_params(
        axis="y",
        colors=GREEN,
    )

    yield_axis.spines[
        "left"
    ].set_color(
        BLUE
    )

    underweight_axis.spines[
        "right"
    ].set_color(
        RED
    )

    good_units_axis.spines[
        "right"
    ].set_color(
        GREEN
    )

    yield_axis.grid(
        True,
        linestyle="--",
        linewidth=0.8,
        color=LIGHT_GRID,
        alpha=0.9,
    )

    yield_axis.set_axisbelow(
        True
    )

    yield_min = float(
        yield_values.min()
    )

    yield_max = float(
        yield_values.max()
    )

    yield_padding = max(
        3.0,
        (
            yield_max
            - yield_min
        )
        * 0.18,
    )

    yield_axis.set_ylim(
        max(
            0,
            yield_min
            - yield_padding,
        ),
        yield_max
        + yield_padding,
    )

    underweight_axis.set_ylim(
        0,
        max(
            1.0,
            float(
                underweight_values.max()
            )
            * 1.14,
        ),
    )

    good_min = float(
        good_units_values.min()
    )

    good_max = float(
        good_units_values.max()
    )

    good_padding = max(
        20.0,
        (
            good_max
            - good_min
        )
        * 0.18,
    )

    good_units_axis.set_ylim(
        max(
            0,
            good_min
            - good_padding,
        ),
        good_max
        + good_padding,
    )

    x_padding = max(
        0.5,
        (
            float(x.max())
            - float(x.min())
        )
        * 0.025,
    )

    yield_axis.set_xlim(
        float(x.min())
        - x_padding,
        float(x.max())
        + x_padding,
    )

    target_filling = summary[
        "target_filling_weight"
    ]

    input_filling = summary[
        "input_filling_target"
    ]

    optimum_filling = summary[
        "optimum_filling_target"
    ]

    yield_axis.axvline(
        target_filling,
        color=GREY,
        linewidth=1.7,
        linestyle="--",
        alpha=0.85,
        zorder=1,
    )

    yield_axis.text(
        target_filling,
        yield_axis.get_ylim()[1],
        "Target Filling",
        color=GREY,
        fontsize=10,
        ha="center",
        va="bottom",
    )

    if not np.isclose(
        input_filling,
        target_filling,
    ):
        yield_axis.axvline(
            input_filling,
            color=PURPLE,
            linewidth=1.8,
            linestyle=":",
            alpha=0.9,
            zorder=1,
        )

        yield_axis.text(
            input_filling,
            yield_axis.get_ylim()[0],
            "Input Scenario",
            color=PURPLE,
            fontsize=9,
            ha="center",
            va="top",
        )

    yield_axis.axvline(
        optimum_filling,
        color=ORANGE,
        linewidth=1.9,
        linestyle="--",
        alpha=0.95,
        zorder=1,
    )

    optimum_y = summary[
        "optimum_yield"
    ]

    yield_axis.scatter(
        [optimum_filling],
        [optimum_y],
        s=68,
        color=ORANGE,
        edgecolor="white",
        linewidth=1.2,
        zorder=7,
    )

    yield_axis.annotate(
        "Optimum\n(maximum Good Units)",
        xy=(
            optimum_filling,
            optimum_y,
        ),
        xytext=(
            optimum_filling,
            yield_axis.get_ylim()[1]
            - (
                yield_axis.get_ylim()[1]
                - yield_axis.get_ylim()[0]
            )
            * 0.05,
        ),
        color=ORANGE,
        fontsize=11,
        fontweight="bold",
        ha="center",
        va="top",
        arrowprops={
            "arrowstyle": "-|>",
            "color": ORANGE,
            "linewidth": 1.7,
        },
    )

    label_indices = (
        _representative_indices(
            len(x),
            requested_labels=8,
        )
    )

    for index in label_indices:
        yield_axis.annotate(
            f"{yield_values[index]:.1f}%",
            (
                x[index],
                yield_values[index],
            ),
            textcoords="offset points",
            xytext=(
                0,
                10,
            ),
            ha="center",
            fontsize=8.5,
            color=BLUE,
            fontweight="bold",
        )

        underweight_axis.annotate(
            f"{underweight_values[index]:.1f}%",
            (
                x[index],
                underweight_values[index],
            ),
            textcoords="offset points",
            xytext=(
                0,
                -16,
            ),
            ha="center",
            fontsize=8,
            color=RED,
            fontweight="bold",
        )

        good_units_axis.annotate(
            f"{good_units_values[index]:,.0f}",
            (
                x[index],
                good_units_values[index],
            ),
            textcoords="offset points",
            xytext=(
                0,
                10,
            ),
            ha="center",
            fontsize=8,
            color=GREEN,
            fontweight="bold",
        )

    legend_handles = [
        Line2D(
            [0],
            [0],
            color=BLUE,
            marker="o",
            linewidth=2.4,
            markersize=6,
            label="Yield (%)",
        ),
        Line2D(
            [0],
            [0],
            color=RED,
            marker="s",
            linewidth=2.3,
            markersize=6,
            label="% Underweight (Seconds)",
        ),
        Line2D(
            [0],
            [0],
            color=GREEN,
            marker="^",
            linewidth=2.3,
            markersize=6,
            label="Good Units",
        ),
    ]

    yield_axis.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(
            0.5,
            1.17,
        ),
        ncol=3,
        frameon=False,
        fontsize=11,
        columnspacing=3.0,
        handlelength=2.7,
    )

    summary_box = FancyBboxPatch(
        (
            0.10,
            0.035,
        ),
        0.70,
        0.145,
        transform=figure.transFigure,
        boxstyle=(
            "round,pad=0.012,"
            "rounding_size=0.012"
        ),
        facecolor=SUMMARY_BACKGROUND,
        edgecolor=SUMMARY_BORDER,
        linewidth=1.0,
    )

    figure.patches.append(
        summary_box
    )

    figure.text(
        0.12,
        0.155,
        (
            "Best compliant result:"
            if summary[
                "constraint_met"
            ]
            else
            "Best result inside the tested range:"
        ),
        fontsize=11,
        color="#222222",
        fontweight="bold",
        va="top",
    )

    figure.text(
        0.13,
        0.120,
        (
            f"• Filling Target: "
            f"{summary['optimum_filling_target']:.2f} g"
        ),
        fontsize=10.5,
        color="#222222",
    )

    figure.text(
        0.13,
        0.092,
        (
            f"• Yield: "
            f"{summary['optimum_yield']:.1f}%"
        ),
        fontsize=10.5,
        color=BLUE,
        fontweight="bold",
    )

    figure.text(
        0.13,
        0.064,
        (
            f"• Underweight: "
            f"{summary['optimum_underweight']:.2f}%"
        ),
        fontsize=10.5,
        color=RED,
        fontweight="bold",
    )

    figure.text(
        0.37,
        0.092,
        (
            f"• Good Units: "
            f"{summary['optimum_good_units']:,.0f}"
        ),
        fontsize=10.5,
        color=GREEN,
        fontweight="bold",
    )

    figure.text(
        0.55,
        0.120,
        (
            "Yield is based on units produced before seconds are removed."
        ),
        fontsize=9.5,
        color="#333333",
    )

    figure.text(
        0.55,
        0.086,
        (
            "Underweights affect the green Good Units curve only."
        ),
        fontsize=9.5,
        color="#333333",
    )

    return figure


def chart_to_png_bytes(
    figure,
) -> bytes:
    """Convert the static Matplotlib figure into PNG bytes."""

    buffer = io.BytesIO()

    figure.savefig(
        buffer,
        format="png",
        dpi=150,
        bbox_inches="tight",
        facecolor="white",
    )

    buffer.seek(0)

    return buffer.getvalue()
