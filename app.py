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
        "The model evaluates how pastry weight and filling target affect "
        "filling yield, underweight products and good units."
    )

    with st.sidebar:
        st.header("Inputs")

        nominal_pastry_weight = st.number_input(
            "Nominal pastry weight (g)",
            min_value=0.01,
            value=95.0,
            step=0.1,
        )

        minimum_pastry_weight = st.number_input(
            "Minimum pastry weight (g)",
            min_value=0.01,
            value=88.0,
            step=0.1,
        )

        nominal_filling_weight = st.number_input(
            "Nominal filling weight (g)",
            min_value=0.01,
            value=105.0,
            step=0.1,
        )

        nominal_glaze_weight = st.number_input(
            "Nominal glaze weight (g)",
            min_value=0.0,
            value=0.0,
            step=0.1,
        )

        filling_batch_kg = st.number_input(
            "Filling batch size (kg)",
            min_value=0.001,
            value=257.675,
            step=0.001,
            format="%.3f",
        )

        permitted_reduction_percentage = st.number_input(
            "Permitted reduction below nominal weight (%)",
            min_value=0.0,
            max_value=99.99,
            value=0.0,
            step=0.1,
        )

        maximum_extra_filling = st.number_input(
            "Maximum extra filling to evaluate (g)",
            min_value=0.0,
            value=15.0,
            step=0.5,
        )

        maximum_acceptable_underweight = st.number_input(
            "Maximum acceptable underweight (%)",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
        )

        filling_variation_percentage = st.number_input(
            "Filling process variation (%)",
            min_value=0.0,
            value=0.0,
            step=0.1,
            help=(
                "Use 0% when the filling target should be treated as exact."
            ),
        )

        run_button = st.button(
            "Run optimisation",
            type="primary",
            use_container_width=True,
        )

    if run_button:
        if minimum_pastry_weight > nominal_pastry_weight:
            st.error(
                "Minimum pastry weight cannot be greater than "
                "nominal pastry weight."
            )
            st.stop()

        output = run_optimisation(
            nominal_pastry_weight=nominal_pastry_weight,
            minimum_pastry_weight=minimum_pastry_weight,
            nominal_filling_weight=nominal_filling_weight,
            nominal_glaze_weight=nominal_glaze_weight,
            filling_batch_kg=filling_batch_kg,
            permitted_reduction_percentage=(
                permitted_reduction_percentage
            ),
            maximum_extra_filling=maximum_extra_filling,
            maximum_acceptable_underweight=(
                maximum_acceptable_underweight
            ),
            filling_variation_percentage=(
                filling_variation_percentage
            ),
        )

        summary = output["summary"]
        results_df = output["results"]

        if summary["constraint_met"]:
            st.success(
                "A compliant filling target was found."
            )
        else:
            st.warning(
                "No tested filling target met the selected underweight "
                "limit. Increase the maximum extra filling."
            )

        st.subheader(summary["result_status"])

        c1, c2, c3 = st.columns(3)
        c4, c5, c6 = st.columns(3)

        filling_adjustment = (
            summary["optimal_filling"]
            - summary["nominal_filling_weight"]
        )

        c1.metric(
            "Selected filling",
            f"{summary['optimal_filling']:.2f} g",
        )

        c2.metric(
            "Filling adjustment",
            f"{filling_adjustment:+.2f} g",
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
            "Filling yield compares units at the tested filling target "
            "against units at the nominal filling target. Underweight is "
            "reported separately."
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
                    f"Nominal units = "
                    f"{filling_batch_kg * 1000:,.1f} ÷ "
                    f"{nominal_filling_weight:.2f} = "
                    f"{summary['optimal_nominal_units']:,.1f}"
                )
            )

            st.code(
                (
                    f"Produced units = "
                    f"{filling_batch_kg * 1000:,.1f} ÷ "
                    f"{summary['optimal_filling']:.2f} = "
                    f"{summary['optimal_produced_units']:,.1f}"
                )
            )

            st.code(
                (
                    f"Yield = "
                    f"{summary['optimal_produced_units']:,.1f} ÷ "
                    f"{summary['optimal_nominal_units']:,.1f} × 100 = "
                    f"{summary['optimal_yield']:.1f}%"
                )
            )

        with st.expander("Pastry compensation explanation"):
            st.write(
                (
                    "Minimum pastry deficit: "
                    f"{summary['direct_minimum_pastry_deficit']:.2f} g"
                )
            )

            st.write(
                (
                    "Simulated average pastry deficit: "
                    f"{summary['average_pastry_deficit']:.2f} g"
                )
            )

            st.info(
                "When pastry is lighter, extra filling may be required "
                "to replace the missing pastry weight."
            )

        st.subheader("Scenario results")

        display_df = results_df.rename(
            columns={
                "filling_target": "Filling Target (g)",
                "filling_adjustment": "Adjustment vs Nominal (g)",
                "yield_percentage": "Filling Yield (%)",
                "nominal_units": "Nominal Units",
                "produced_units": "Produced Units",
                "underweight_percentage": "Underweight (%)",
                "expected_seconds": "Expected Seconds",
                "good_units": "Good Units",
                "good_output_rate": "Good Output Rate (%)",
                "average_final_weight": "Average Final Weight (g)",
                "meets_underweight_limit": "Meets Limit",
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
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "Download results as CSV",
            data=results_df.to_csv(index=False),
            file_name="filling_optimisation_results.csv",
            mime="text/csv",
        )

    else:
        st.info(
            "Enter the values and click Run optimisation."
        )


with instructions_tab:
    show_instructions()
