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
        "The model evaluates filling targets below, at and above "
        "the nominal filling weight."
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
        )

        summary = output["summary"]
        results_df = output["results"]

        if summary["constraint_met"]:
            st.success(
                "A compliant filling target was found within the "
                "selected underweight limit."
            )
        else:
            st.warning(
                "No tested filling target met the selected underweight "
                "limit. The result shown is only the best available "
                "inside the tested range. Increase 'Maximum extra filling' "
                "to test a wider range."
            )

        st.subheader(summary["result_status"])

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Selected filling",
            f"{summary['optimal_filling']:.2f} g",
        )

        filling_difference = (
            summary["optimal_filling"]
            - summary["nominal_filling_weight"]
        )

        col2.metric(
            "Filling adjustment",
            f"{filling_difference:+.2f} g",
        )

        col3.metric(
            "Expected production yield",
            f"{summary['optimal_yield']:.1f}%",
        )

        col4.metric(
            "Expected underweight",
            f"{summary['optimal_underweight']:.2f}%",
        )

        col5.metric(
            "Expected good units",
            f"{summary['optimal_good_units']:,.0f}",
        )

        st.caption(
            "Expected production yield includes the 98% recovery factor, "
            "the filling adjustment and the estimated good-product rate."
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

        st.caption(
            "Chart controls: use the mouse wheel to zoom, drag to zoom into "
            "an area, use the toolbar buttons to zoom in or out, and "
            "double-click the chart to reset."
        )

        with st.expander("Pastry simulation assumptions"):
            st.write(
                "Pastry weights are generated randomly between the "
                "selected minimum and an upper value slightly above nominal. "
                "The distribution is mildly biased toward the selected "
                "minimum pastry weight."
            )

            p1, p2, p3 = st.columns(3)

            p1.metric(
                "Minimum generated",
                f"{summary['simulated_pastry_minimum']:.2f} g",
            )

            p2.metric(
                "Average generated",
                f"{summary['simulated_pastry_average']:.2f} g",
            )

            p3.metric(
                "Maximum generated",
                f"{summary['simulated_pastry_maximum']:.2f} g",
            )

        st.subheader("Scenario results")

        display_df = results_df.rename(
            columns={
                "filling_target": "Filling Target (g)",
                "filling_adjustment": "Adjustment vs Nominal (g)",
                "theoretical_filling_yield": "Filling Yield (%)",
                "yield_percentage": "Expected Production Yield (%)",
                "underweight_percentage": "Underweight (%)",
                "produced_units": "Produced Units",
                "expected_seconds": "Expected Seconds",
                "good_units": "Good Units",
                "meets_underweight_limit": "Meets Limit",
            }
        )

        st.dataframe(
            display_df.style.format(
                {
                    "Filling Target (g)": "{:.2f}",
                    "Adjustment vs Nominal (g)": "{:+.2f}",
                    "Filling Yield (%)": "{:.2f}",
                    "Expected Production Yield (%)": "{:.2f}",
                    "Underweight (%)": "{:.2f}",
                    "Produced Units": "{:,.0f}",
                    "Expected Seconds": "{:,.1f}",
                    "Good Units": "{:,.1f}",
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
            "Enter the values in the sidebar and click "
            "'Run optimisation'."
        )

    st.caption(
        "Internal assumptions: 98% filling recovery, simulated pastry "
        "variation, simulated filling variation and simulated glaze variation."
    )


with instructions_tab:
    show_instructions()
