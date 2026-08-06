from __future__ import annotations

import matplotlib.pyplot as plt
import streamlit as st

from charts import (
    chart_to_png_bytes,
    create_optimisation_chart,
)
from instructions import show_instructions
from model import run_optimisation


st.set_page_config(
    page_title="Filling Optimisation Model",
    page_icon="📈",
    layout="wide",
)

st.title("Filling Optimisation Model")

optimisation_tab, instructions_tab = st.tabs(
    [
        "Optimisation",
        "Instructions and model explanation",
    ]
)


@st.cache_data(
    show_spinner=False,
)
def calculate_model(
    target_pastry_weight,
    target_filling_weight,
    target_glaze_weight,
    filling_batch_kg,
    permitted_reduction_percentage,
    maximum_acceptable_underweight,
    pastry_adjustment,
    filling_adjustment,
    variation_method,
    pastry_variation_value,
    filling_variation_value,
):
    """Cache repeated model calculations."""

    return run_optimisation(
        target_pastry_weight=target_pastry_weight,
        target_filling_weight=target_filling_weight,
        target_glaze_weight=target_glaze_weight,
        filling_batch_kg=filling_batch_kg,
        permitted_reduction_percentage=(
            permitted_reduction_percentage
        ),
        maximum_acceptable_underweight=(
            maximum_acceptable_underweight
        ),
        pastry_adjustment=pastry_adjustment,
        filling_adjustment=filling_adjustment,
        variation_method=variation_method,
        pastry_variation_value=(
            pastry_variation_value
        ),
        filling_variation_value=(
            filling_variation_value
        ),
    )


with optimisation_tab:
    st.caption(
        "Yield is based on total units produced. Underweights reduce "
        "Good Units, not Yield."
    )

    with st.sidebar:
        st.header("1. Product Targets")

        target_pastry_weight = st.number_input(
            "Target pastry weight (g)",
            min_value=0.01,
            value=95.0,
            step=0.1,
            help=(
                "Approved pastry target from the product specification."
            ),
        )

        target_filling_weight = st.number_input(
            "Target filling weight (g)",
            min_value=0.01,
            value=105.0,
            step=0.1,
            help=(
                "Approved filling target used to calculate fixed "
                "Expected Units."
            ),
        )

        target_glaze_weight = st.number_input(
            "Target glaze weight (g)",
            min_value=0.0,
            value=0.0,
            step=0.1,
            help=(
                "Enter 0 g when glaze is not included."
            ),
        )

        filling_batch_kg = st.number_input(
            "Filling batch size (kg)",
            min_value=0.001,
            value=257.675,
            step=0.001,
            format="%.3f",
            help=(
                "Total filling available for the production run."
            ),
        )

        permitted_reduction_percentage = st.number_input(
            "Permitted reduction below target product weight (%)",
            min_value=0.0,
            max_value=99.99,
            value=0.0,
            step=0.1,
            help=(
                "Approved finished-product weight allowance."
            ),
        )

        maximum_acceptable_underweight = st.number_input(
            "Maximum acceptable underweight (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.1,
            help=(
                "Highest simulated seconds percentage allowed for a "
                "compliant optimum."
            ),
        )

        st.header("2. Scenario Adjustments")

        pastry_adjustment = st.number_input(
            "Pastry adjustment vs target (g)",
            value=0.0,
            step=0.5,
            format="%.2f",
            help=(
                "Negative = lighter pastry. Positive = heavier pastry."
            ),
        )

        filling_adjustment = st.number_input(
            "Filling adjustment vs target (g)",
            value=0.0,
            step=0.5,
            format="%.2f",
            help=(
                "Negative = less filling. Positive = extra filling."
            ),
        )

        actual_pastry_average = (
            target_pastry_weight
            + pastry_adjustment
        )

        input_filling_target = (
            target_filling_weight
            + filling_adjustment
        )

        st.caption(
            f"Actual pastry average: "
            f"{actual_pastry_average:.2f} g"
        )

        st.caption(
            f"Input filling target: "
            f"{input_filling_target:.2f} g"
        )

        st.header("3. Process Variation")

        variation_method = st.selectbox(
            "Variation input method",
            options=[
                "Standard deviation (g)",
                "Percentage (CV)",
            ],
            help=(
                "Choose whether variation is entered in grams or as CV%."
            ),
        )

        pastry_variation_value = st.number_input(
            "Pastry variation",
            min_value=0.0,
            value=2.0,
            step=0.1,
            help=(
                "Enter 0 for an exact scenario."
            ),
        )

        filling_variation_value = st.number_input(
            "Filling variation",
            min_value=0.0,
            value=1.0,
            step=0.1,
            help=(
                "Enter 0 for an exact scenario."
            ),
        )

    try:
        output = calculate_model(
            target_pastry_weight,
            target_filling_weight,
            target_glaze_weight,
            filling_batch_kg,
            permitted_reduction_percentage,
            maximum_acceptable_underweight,
            pastry_adjustment,
            filling_adjustment,
            variation_method,
            pastry_variation_value,
            filling_variation_value,
        )

    except ValueError as error:
        st.error(
            str(error)
        )
        st.stop()

    results_df = output[
        "results"
    ]

    summary = output[
        "summary"
    ]

    st.subheader(
        "Fixed production expectation"
    )

    e1, e2, e3 = st.columns(
        3
    )

    e1.metric(
        "Target product weight",
        f"{summary['target_product_weight']:.2f} g",
    )

    e2.metric(
        "Minimum allowed weight",
        f"{summary['minimum_allowed_weight']:.2f} g",
    )

    e3.metric(
        "Expected Units",
        f"{summary['expected_units']:,.0f}",
        help=(
            "Fixed value: batch size divided by Target Filling."
        ),
    )

    st.subheader(
        "Input scenario"
    )

    a1, a2, a3 = st.columns(
        3
    )

    a4, a5, a6 = st.columns(
        3
    )

    a1.metric(
        "Actual pastry average",
        f"{summary['actual_pastry_average']:.2f} g",
        delta=(
            f"{summary['pastry_adjustment']:+.2f} g vs target"
        ),
    )

    a2.metric(
        "Input filling target",
        f"{summary['input_filling_target']:.2f} g",
        delta=(
            f"{summary['filling_adjustment']:+.2f} g vs target"
        ),
    )

    a3.metric(
        "Actual Units",
        f"{summary['input_actual_units']:,.0f}",
    )

    a4.metric(
        "Yield",
        f"{summary['input_yield']:.1f}%",
    )

    a5.metric(
        "Underweight",
        f"{summary['input_underweight']:.2f}%",
    )

    a6.metric(
        "Good Units",
        f"{summary['input_good_units']:,.0f}",
    )

    st.divider()

    st.subheader(
        summary[
            "recommendation_status"
        ]
    )

    if summary[
        "constraint_met"
    ]:
        st.success(
            "The optimum is inside the selected maximum "
            "underweight limit."
        )
    else:
        st.warning(
            "No scenario inside the automatic range meets the selected "
            "underweight limit. The result shown has the highest Good Units "
            "inside the tested range."
        )

    r1, r2, r3 = st.columns(
        3
    )

    r4, r5, r6 = st.columns(
        3
    )

    r1.metric(
        "Optimum filling target",
        f"{summary['optimum_filling_target']:.2f} g",
    )

    r2.metric(
        "Adjustment vs target",
        f"{summary['optimum_filling_adjustment']:+.2f} g",
    )

    r3.metric(
        "Yield",
        f"{summary['optimum_yield']:.1f}%",
    )

    r4.metric(
        "Actual Units",
        f"{summary['optimum_actual_units']:,.0f}",
    )

    r5.metric(
        "Underweight",
        f"{summary['optimum_underweight']:.2f}%",
    )

    r6.metric(
        "Good Units",
        f"{summary['optimum_good_units']:,.0f}",
    )

    chart_figure = (
        create_optimisation_chart(
            results_df=results_df,
            summary=summary,
        )
    )

    chart_png = chart_to_png_bytes(
        chart_figure
    )

    st.pyplot(
        chart_figure,
        width="stretch",
        clear_figure=False,
    )

    st.caption(
        "Static chart. Zoom and interactive controls have been removed."
    )

    st.download_button(
        "Download chart as PNG",
        data=chart_png,
        file_name=(
            "filling_optimisation_chart.png"
        ),
        mime="image/png",
    )

    plt.close(
        chart_figure
    )

    with st.expander(
        "Calculation check"
    ):
        st.code(
            (
                f"Expected Units = "
                f"{filling_batch_kg * 1000:,.1f} g ÷ "
                f"{target_filling_weight:.2f} g = "
                f"{summary['expected_units']:,.1f}"
            )
        )

        st.code(
            (
                f"Actual Units = "
                f"{filling_batch_kg * 1000:,.1f} g ÷ "
                f"{summary['input_filling_target']:.2f} g = "
                f"{summary['input_actual_units']:,.1f}"
            )
        )

        st.code(
            (
                f"Yield = "
                f"{summary['input_actual_units']:,.1f} ÷ "
                f"{summary['expected_units']:,.1f} × 100 = "
                f"{summary['input_yield']:.2f}%"
            )
        )

        st.code(
            (
                f"Good Units = "
                f"{summary['input_actual_units']:,.1f} × "
                f"(1 - {summary['input_underweight']:.2f}%) = "
                f"{summary['input_good_units']:,.1f}"
            )
        )

    with st.expander(
        "Scenario and variation check"
    ):
        st.write(
            f"Pastry condition: "
            f"{summary['pastry_condition']}"
        )

        st.write(
            f"Variation method: "
            f"{summary['variation_method']}"
        )

        st.write(
            f"Pastry standard deviation used: "
            f"{summary['pastry_sd_g']:.3f} g"
        )

        st.write(
            f"Automatic filling range: "
            f"{summary['minimum_tested_filling']:.2f} g to "
            f"{summary['maximum_tested_filling']:.2f} g"
        )

    st.subheader(
        "All filling scenarios"
    )

    display_df = (
        results_df.rename(
            columns={
                "filling_target": (
                    "Filling Target (g)"
                ),
                "filling_adjustment": (
                    "Adjustment vs Target (g)"
                ),
                "expected_units": (
                    "Expected Units"
                ),
                "actual_units": (
                    "Actual Units"
                ),
                "yield_percentage": (
                    "Yield (%)"
                ),
                "underweight_percentage": (
                    "Underweight (%)"
                ),
                "expected_seconds": (
                    "Expected Seconds"
                ),
                "good_units": (
                    "Good Units"
                ),
                "average_final_weight": (
                    "Average Final Weight (g)"
                ),
                "minimum_simulated_weight": (
                    "Minimum Simulated Weight (g)"
                ),
                "meets_underweight_limit": (
                    "Meets Limit"
                ),
            }
        )
    )

    st.dataframe(
        display_df[
            [
                "Filling Target (g)",
                "Adjustment vs Target (g)",
                "Expected Units",
                "Actual Units",
                "Yield (%)",
                "Underweight (%)",
                "Expected Seconds",
                "Good Units",
                "Average Final Weight (g)",
                "Meets Limit",
            ]
        ].style.format(
            {
                "Filling Target (g)": "{:.2f}",
                "Adjustment vs Target (g)": "{:+.2f}",
                "Expected Units": "{:,.1f}",
                "Actual Units": "{:,.1f}",
                "Yield (%)": "{:.2f}",
                "Underweight (%)": "{:.2f}",
                "Expected Seconds": "{:,.1f}",
                "Good Units": "{:,.1f}",
                "Average Final Weight (g)": "{:.2f}",
            }
        ),
        width="stretch",
        hide_index=True,
    )

    st.download_button(
        "Download all scenarios as CSV",
        data=results_df.to_csv(
            index=False
        ),
        file_name=(
            "filling_optimisation_results.csv"
        ),
        mime="text/csv",
    )


with instructions_tab:
    show_instructions()
