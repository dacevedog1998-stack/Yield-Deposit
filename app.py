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
    st.write(
        "Analyse pastry that is lighter, equal to or heavier than nominal "
        "and test filling targets below or above the standard target."
    )

    with st.sidebar:
        st.header("Product specification")

        nominal_pastry_weight = st.number_input(
            "Nominal pastry weight (g)",
            min_value=0.01,
            value=95.0,
            step=0.1,
            help=(
                "Approved pastry target from the product specification."
            ),
        )

        nominal_filling_weight = st.number_input(
            "Nominal filling weight (g)",
            min_value=0.01,
            value=105.0,
            step=0.1,
            help=(
                "Approved filling target. This represents 100% filling yield."
            ),
        )

        nominal_glaze_weight = st.number_input(
            "Nominal glaze weight (g)",
            min_value=0.0,
            value=0.0,
            step=0.1,
            help=(
                "Enter 0 g when glaze is not included."
            ),
        )

        st.header("Current production condition")

        current_pastry_weight = st.number_input(
            "Current pastry average weight (g)",
            min_value=0.01,
            value=95.0,
            step=0.1,
            help=(
                "Average measured pastry weight. It may be below, equal to "
                "or above nominal."
            ),
        )

        pastry_variation_percentage = st.number_input(
            "Pastry process variation (%)",
            min_value=0.0,
            value=0.0,
            step=0.1,
            help=(
                "Use 0% for an exact scenario. When measured, enter "
                "standard deviation ÷ average × 100."
            ),
        )

        filling_variation_percentage = st.number_input(
            "Filling process variation (%)",
            min_value=0.0,
            value=0.0,
            step=0.1,
            help=(
                "Use 0% to treat each tested filling target as exact."
            ),
        )

        glaze_variation_percentage = st.number_input(
            "Glaze process variation (%)",
            min_value=0.0,
            value=0.0,
            step=0.1,
            help=(
                "Use 0% when glaze is exact or excluded."
            ),
        )

        pastry_difference = (
            current_pastry_weight
            - nominal_pastry_weight
        )

        if pastry_difference < 0:
            st.info(
                f"Pastry is {abs(pastry_difference):.2f} g light. "
                f"Start by testing at least "
                f"{abs(pastry_difference):.2f} g extra filling."
            )

        elif pastry_difference > 0:
            st.info(
                f"Pastry is {pastry_difference:.2f} g heavy. "
                f"Start by testing a filling reduction of up to "
                f"{pastry_difference:.2f} g."
            )

        else:
            st.info(
                "Pastry is currently at its nominal weight."
            )

        st.header("Production and quality")

        filling_batch_kg = st.number_input(
            "Filling batch size (kg)",
            min_value=0.001,
            value=257.675,
            step=0.001,
            format="%.3f",
            help=(
                "Enter the actual filling available for the run."
            ),
        )

        permitted_reduction_percentage = st.number_input(
            "Permitted reduction below nominal weight (%)",
            min_value=0.0,
            max_value=99.99,
            value=0.0,
            step=0.1,
            help=(
                "Enter the approved finished-product weight allowance. "
                "Use 0% when no reduction is permitted."
            ),
        )

        maximum_acceptable_underweight = st.number_input(
            "Maximum acceptable underweight (%)",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            help=(
                "Highest simulated seconds percentage allowed for a "
                "compliant recommendation."
            ),
        )

        st.header("Filling range to evaluate")

        maximum_filling_reduction = st.number_input(
            "Maximum filling reduction to evaluate (g)",
            min_value=0.0,
            value=15.0,
            step=0.5,
            help=(
                "How far below nominal filling the model may test. "
                "Useful when pastry is heavy."
            ),
        )

        maximum_extra_filling = st.number_input(
            "Maximum extra filling to evaluate (g)",
            min_value=0.0,
            value=15.0,
            step=0.5,
            help=(
                "How far above nominal filling the model may test. "
                "Useful when pastry is light."
            ),
        )

        run_button = st.button(
            "Run optimisation",
            type="primary",
            use_container_width=True,
        )

    if run_button:
        try:
            output = run_optimisation(
                nominal_pastry_weight=(
                    nominal_pastry_weight
                ),
                current_pastry_weight=(
                    current_pastry_weight
                ),
                nominal_filling_weight=(
                    nominal_filling_weight
                ),
                nominal_glaze_weight=(
                    nominal_glaze_weight
                ),
                filling_batch_kg=(
                    filling_batch_kg
                ),
                permitted_reduction_percentage=(
                    permitted_reduction_percentage
                ),
                maximum_filling_reduction=(
                    maximum_filling_reduction
                ),
                maximum_extra_filling=(
                    maximum_extra_filling
                ),
                maximum_acceptable_underweight=(
                    maximum_acceptable_underweight
                ),
                pastry_variation_percentage=(
                    pastry_variation_percentage
                ),
                filling_variation_percentage=(
                    filling_variation_percentage
                ),
                glaze_variation_percentage=(
                    glaze_variation_percentage
                ),
            )

        except ValueError as error:
            st.error(str(error))
            st.stop()

        summary = output["summary"]
        results_df = output["results"]

        st.info(
            summary["condition_message"]
        )

        if summary["constraint_met"]:
            st.success(
                "A compliant filling target was found."
            )
        else:
            st.warning(
                "No tested target met the selected underweight limit. "
                "Increase the filling range or review the process inputs."
            )

        st.subheader(
            summary["result_status"]
        )

        c1, c2, c3 = st.columns(3)
        c4, c5, c6 = st.columns(3)

        c1.metric(
            "Selected filling",
            f"{summary['optimal_filling']:.2f} g",
        )

        c2.metric(
            "Filling adjustment",
            f"{summary['optimal_filling_adjustment']:+.2f} g",
        )

        c3.metric(
            "Filling yield",
            f"{summary['optimal_yield']:.1f}%",
        )

        c4.metric(
            "Produced units",
            f"{summary['optimal_produced_units']:,.0f}",
        )

        c5.metric(
            "Expected underweight",
            f"{summary['optimal_underweight']:.2f}%",
        )

        c6.metric(
            "Expected good units",
            f"{summary['optimal_good_units']:,.0f}",
        )

        st.caption(
            "Filling yield compares units at the selected target with units "
            "at nominal filling. Underweight is calculated separately."
        )

        figure = create_optimisation_chart(
            results_df=results_df,
            summary=summary,
        )

        st.plotly_chart(
            figure,
            use_container_width=True,
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

        with st.expander(
            "Calculation check"
        ):
            st.code(
                (
                    f"Nominal units = "
                    f"{filling_batch_kg * 1000:,.1f} g ÷ "
                    f"{nominal_filling_weight:.2f} g = "
                    f"{summary['optimal_nominal_units']:,.1f}"
                )
            )

            st.code(
                (
                    f"Produced units = "
                    f"{filling_batch_kg * 1000:,.1f} g ÷ "
                    f"{summary['optimal_filling']:.2f} g = "
                    f"{summary['optimal_produced_units']:,.1f}"
                )
            )

            st.code(
                (
                    f"Filling yield = "
                    f"{summary['optimal_produced_units']:,.1f} ÷ "
                    f"{summary['optimal_nominal_units']:,.1f} × 100 = "
                    f"{summary['optimal_yield']:.1f}%"
                )
            )

        with st.expander(
            "Pastry condition explanation"
        ):
            p1, p2, p3 = st.columns(3)

            p1.metric(
                "Nominal pastry",
                f"{summary['nominal_pastry_weight']:.2f} g",
            )

            p2.metric(
                "Current pastry average",
                f"{summary['current_pastry_weight']:.2f} g",
            )

            p3.metric(
                "Difference",
                f"{summary['pastry_difference']:+.2f} g",
            )

            st.write(
                f"**Condition:** {summary['pastry_condition']}"
            )

            st.write(
                f"**Suggested direction:** "
                f"{summary['suggested_direction']}"
            )

            st.write(
                f"**Suggested starting adjustment:** "
                f"{summary['suggested_starting_adjustment']:.2f} g"
            )

            st.write(
                f"**Simulated pastry range:** "
                f"{summary['simulated_pastry_minimum']:.2f} g to "
                f"{summary['simulated_pastry_maximum']:.2f} g"
            )

        with st.expander(
            "Product weight limits"
        ):
            st.write(
                f"Nominal product weight: "
                f"{summary['nominal_product_weight']:.2f} g"
            )

            st.write(
                f"Minimum allowed weight: "
                f"{summary['minimum_allowed_weight']:.2f} g"
            )

            st.write(
                f"Selected scenario average final weight: "
                f"{summary['optimal_average_final_weight']:.2f} g"
            )

            st.write(
                f"Average buffer above the minimum: "
                f"{summary['optimal_average_weight_buffer']:+.2f} g"
            )

        st.subheader("Scenario results")

        display_df = results_df.rename(
            columns={
                "filling_target": (
                    "Filling Target (g)"
                ),
                "filling_adjustment": (
                    "Adjustment vs Nominal (g)"
                ),
                "yield_percentage": (
                    "Filling Yield (%)"
                ),
                "nominal_units": (
                    "Nominal Units"
                ),
                "produced_units": (
                    "Produced Units"
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
                "good_output_rate": (
                    "Good Output Rate (%)"
                ),
                "average_final_weight": (
                    "Average Final Weight (g)"
                ),
                "minimum_simulated_weight": (
                    "Minimum Simulated Weight (g)"
                ),
                "average_weight_buffer": (
                    "Average Weight Buffer (g)"
                ),
                "meets_underweight_limit": (
                    "Meets Limit"
                ),
            }
        )

        st.dataframe(
            display_df.style.format(
                {
                    "Filling Target (g)": "{:.2f}",
                    "Adjustment vs Nominal (g)": "{:+.2f}",
                    "Filling Yield (%)": "{:.2f}",
                    "Nominal Units": "{:,.1f}",
                    "Produced Units": "{:,.1f}",
                    "Underweight (%)": "{:.2f}",
                    "Expected Seconds": "{:,.1f}",
                    "Good Units": "{:,.1f}",
                    "Good Output Rate (%)": "{:.2f}",
                    "Average Final Weight (g)": "{:.2f}",
                    "Minimum Simulated Weight (g)": "{:.2f}",
                    "Average Weight Buffer (g)": "{:+.2f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "Download results as CSV",
            data=results_df.to_csv(
                index=False
            ),
            file_name=(
                "filling_optimisation_results.csv"
            ),
            mime="text/csv",
        )

    else:
        st.info(
            "Enter the product and process values in the sidebar, "
            "then select Run optimisation."
        )


with instructions_tab:
    show_instructions()
