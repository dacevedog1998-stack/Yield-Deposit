from __future__ import annotations

import streamlit as st

from charts import create_optimisation_chart
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


with optimisation_tab:
    st.caption(
        "Test normal, unusual or extreme pastry and filling scenarios. "
        "The three curves are always displayed."
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

        actual_filling_adjustment = st.number_input(
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

        actual_filling_target = (
            target_filling_weight
            + actual_filling_adjustment
        )

        st.caption(
            f"Actual pastry average: "
            f"{actual_pastry_average:.2f} g"
        )

        st.caption(
            f"Input filling target: "
            f"{actual_filling_target:.2f} g"
        )

        st.header("3. Process Variation")

        variation_method = st.selectbox(
            "Variation input method",
            options=[
                "Standard deviation (g)",
                "Percentage (CV)",
            ],
            help=(
                "Choose whether pastry and filling variation are entered "
                "in grams or as CV percentage."
            ),
        )

        pastry_variation_value = st.number_input(
            "Pastry variation",
            min_value=0.0,
            value=2.0,
            step=0.1,
            help=(
                "Enter 0 for an exact scenario. The unit depends on the "
                "selected variation method."
            ),
        )

        filling_variation_value = st.number_input(
            "Filling variation",
            min_value=0.0,
            value=1.0,
            step=0.1,
            help=(
                "Enter 0 for an exact scenario. The unit depends on the "
                "selected variation method."
            ),
        )

    try:
        output = run_optimisation(
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
            actual_filling_adjustment=(
                actual_filling_adjustment
            ),
            variation_method=variation_method,
            pastry_variation_value=(
                pastry_variation_value
            ),
            filling_variation_value=(
                filling_variation_value
            ),
        )

    except ValueError as error:
        st.error(str(error))
        st.stop()

    results_df = output["results"]
    summary = output["summary"]

    st.subheader("Fixed production expectation")

    e1, e2, e3 = st.columns(3)

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
            "Fixed value calculated from batch size ÷ target filling."
        ),
    )

    st.subheader("Input scenario")

    a1, a2, a3 = st.columns(3)
    a4, a5, a6 = st.columns(3)

    a1.metric(
        "Actual pastry average",
        f"{summary['actual_pastry_average']:.2f} g",
        delta=(
            f"{summary['pastry_adjustment']:+.2f} g vs target"
        ),
    )

    a2.metric(
        "Input filling target",
        f"{summary['actual_filling_target']:.2f} g",
        delta=(
            f"{summary['actual_filling_adjustment']:+.2f} g vs target"
        ),
    )

    a3.metric(
        "Actual Units",
        f"{summary['actual_units']:,.0f}",
    )

    a4.metric(
        "Underweight",
        f"{summary['actual_underweight']:.2f}%",
    )

    a5.metric(
        "Good Units",
        f"{summary['actual_good_units']:,.0f}",
    )

    a6.metric(
        "Production Yield",
        f"{summary['actual_production_yield']:.1f}%",
    )

    st.divider()

    st.subheader(summary["recommendation_status"])

    if summary["constraint_met"]:
        st.success(
            "The optimum is inside the selected maximum underweight limit."
        )
    else:
        st.warning(
            "No point in the tested range meets the selected underweight "
            "limit. The result shown is the highest-output option in the "
            "automatic range."
        )

    r1, r2, r3 = st.columns(3)
    r4, r5, r6 = st.columns(3)

    r1.metric(
        "Optimum filling target",
        f"{summary['recommended_filling_target']:.2f} g",
    )

    r2.metric(
        "Adjustment vs target",
        f"{summary['recommended_filling_adjustment']:+.2f} g",
    )

    r3.metric(
        "Production Yield",
        f"{summary['recommended_production_yield']:.1f}%",
    )

    r4.metric(
        "Actual Units",
        f"{summary['recommended_actual_units']:,.0f}",
    )

    r5.metric(
        "Underweight",
        f"{summary['recommended_underweight']:.2f}%",
    )

    r6.metric(
        "Good Units",
        f"{summary['recommended_good_units']:,.0f}",
    )

    figure = create_optimisation_chart(
        results_df=results_df,
        summary=summary,
    )

    st.plotly_chart(
        figure,
        width="stretch",
        theme=None,
        config={
            "scrollZoom": True,
            "displayModeBar": True,
            "displaylogo": False,
            "responsive": True,
            "modeBarButtonsToRemove": [
                "lasso2d",
                "select2d",
            ],
        },
    )

    with st.expander("Calculation check"):
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
                f"{summary['actual_filling_target']:.2f} g = "
                f"{summary['actual_units']:,.1f}"
            )
        )

        st.code(
            (
                f"Good Units = "
                f"{summary['actual_units']:,.1f} × "
                f"(1 - {summary['actual_underweight']:.2f}%) = "
                f"{summary['actual_good_units']:,.1f}"
            )
        )

        st.code(
            (
                f"Production Yield = "
                f"{summary['actual_good_units']:,.1f} ÷ "
                f"{summary['expected_units']:,.1f} × 100 = "
                f"{summary['actual_production_yield']:.2f}%"
            )
        )

    with st.expander("Scenario and variation check"):
        st.write(
            f"Pastry condition: {summary['pastry_condition']}"
        )

        st.write(
            f"Variation method: {summary['variation_method']}"
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

    st.subheader("All filling scenarios")

    display_df = results_df.rename(
        columns={
            "filling_target": "Filling Target (g)",
            "filling_adjustment": "Adjustment vs Target (g)",
            "expected_units": "Expected Units",
            "actual_units": "Actual Units",
            "underweight_percentage": "Underweight (%)",
            "expected_seconds": "Expected Seconds",
            "good_units": "Good Units",
            "production_yield": "Production Yield (%)",
            "theoretical_filling_yield": "Yield Before Seconds (%)",
            "average_final_weight": "Average Final Weight (g)",
            "minimum_simulated_weight": "Minimum Simulated Weight (g)",
            "meets_underweight_limit": "Meets Limit",
        }
    )

    st.dataframe(
        display_df[
            [
                "Filling Target (g)",
                "Adjustment vs Target (g)",
                "Expected Units",
                "Actual Units",
                "Underweight (%)",
                "Expected Seconds",
                "Good Units",
                "Production Yield (%)",
                "Yield Before Seconds (%)",
                "Average Final Weight (g)",
                "Meets Limit",
            ]
        ].style.format(
            {
                "Filling Target (g)": "{:.2f}",
                "Adjustment vs Target (g)": "{:+.2f}",
                "Expected Units": "{:,.1f}",
                "Actual Units": "{:,.1f}",
                "Underweight (%)": "{:.2f}",
                "Expected Seconds": "{:,.1f}",
                "Good Units": "{:,.1f}",
                "Production Yield (%)": "{:.2f}",
                "Yield Before Seconds (%)": "{:.2f}",
                "Average Final Weight (g)": "{:.2f}",
            }
        ),
        width="stretch",
        hide_index=True,
    )

    st.download_button(
        "Download all scenarios as CSV",
        data=results_df.to_csv(index=False),
        file_name="filling_optimisation_results.csv",
        mime="text/csv",
    )


with instructions_tab:
    show_instructions()
