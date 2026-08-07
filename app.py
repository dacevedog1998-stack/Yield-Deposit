from __future__ import annotations

import matplotlib.pyplot as plt
import streamlit as st

from charts import chart_to_png_bytes, create_optimisation_chart
from instructions import show_instructions
from model import run_optimisation

st.set_page_config(page_title="Filling Optimisation Model", page_icon="📈", layout="wide")
st.title("Filling Optimisation Model")

optimisation_tab, instructions_tab = st.tabs(["Optimisation", "Instructions and model explanation"])


@st.cache_data(show_spinner=False)
def calculate_model(
    target_pastry_weight,
    target_filling_weight,
    target_glaze_weight,
    filling_batch_kg,
    actual_batch_usage_percentage,
    permitted_reduction_percentage,
    maximum_acceptable_underweight,
    pastry_adjustment,
    filling_adjustment,
    variation_method,
    pastry_variation_value,
    filling_variation_value,
):
    return run_optimisation(
        target_pastry_weight=target_pastry_weight,
        target_filling_weight=target_filling_weight,
        target_glaze_weight=target_glaze_weight,
        filling_batch_kg=filling_batch_kg,
        actual_batch_usage_percentage=actual_batch_usage_percentage,
        permitted_reduction_percentage=permitted_reduction_percentage,
        maximum_acceptable_underweight=maximum_acceptable_underweight,
        pastry_adjustment=pastry_adjustment,
        filling_adjustment=filling_adjustment,
        variation_method=variation_method,
        pastry_variation_value=pastry_variation_value,
        filling_variation_value=filling_variation_value,
    )


with optimisation_tab:
    st.caption(
        "Yield is based on total units produced from the usable filling batch. Underweights reduce Good Units, not Yield."
    )

    with st.sidebar:
        st.header("1. Product Targets")
        target_pastry_weight = st.number_input("Target pastry weight (g)", min_value=0.01, value=95.0, step=0.1)
        target_filling_weight = st.number_input("Target filling weight (g)", min_value=0.01, value=105.0, step=0.1)
        target_glaze_weight = st.number_input("Target glaze weight (g)", min_value=0.0, value=0.0, step=0.1)
        filling_batch_kg = st.number_input(
            "Filling batch size (kg)", min_value=0.001, value=257.675, step=0.001, format="%.3f"
        )
        actual_batch_usage_percentage = st.number_input(
            "Actual usable filling batch (%)",
            min_value=0.0,
            max_value=100.0,
            value=100.0,
            step=0.5,
            format="%.2f",
            help="Percentage of total batch that is really available after process losses.",
        )
        permitted_reduction_percentage = st.number_input(
            "Permitted reduction below target product weight (%)",
            min_value=0.0,
            max_value=99.99,
            value=0.0,
            step=0.1,
        )
        maximum_acceptable_underweight = st.number_input(
            "Maximum acceptable underweight (%)",
            min_value=0.0,
            max_value=100.0,
            value=5.0,
            step=0.1,
        )

        st.header("2. Scenario Adjustments")
        pastry_adjustment = st.number_input("Pastry adjustment vs target (g)", value=0.0, step=0.5, format="%.2f")
        filling_adjustment = st.number_input("Filling adjustment vs target (g)", value=0.0, step=0.5, format="%.2f")

        actual_pastry_average = target_pastry_weight + pastry_adjustment
        input_filling_target = target_filling_weight + filling_adjustment
        usable_batch_kg = filling_batch_kg * actual_batch_usage_percentage / 100

        st.caption(f"Actual pastry average: {actual_pastry_average:.2f} g")
        st.caption(f"Input filling target: {input_filling_target:.2f} g")
        st.caption(f"Usable filling batch: {usable_batch_kg:.3f} kg")

        st.header("3. Process Variation")
        variation_method = st.selectbox("Variation input method", options=["Standard deviation (g)", "Percentage (CV)"])
        pastry_variation_value = st.number_input("Pastry variation", min_value=0.0, value=2.0, step=0.1)
        filling_variation_value = st.number_input("Filling variation", min_value=0.0, value=1.0, step=0.1)

    try:
        output = calculate_model(
            target_pastry_weight,
            target_filling_weight,
            target_glaze_weight,
            filling_batch_kg,
            actual_batch_usage_percentage,
            permitted_reduction_percentage,
            maximum_acceptable_underweight,
            pastry_adjustment,
            filling_adjustment,
            variation_method,
            pastry_variation_value,
            filling_variation_value,
        )
    except ValueError as error:
        st.error(str(error))
        st.stop()

    results_df = output["results"]
    summary = output["summary"]

    st.subheader("Fixed production expectation")
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Target product weight", f"{summary['target_product_weight']:.2f} g")
    e2.metric("Minimum allowed weight", f"{summary['minimum_allowed_weight']:.2f} g")
    e3.metric(
        "Expected Units",
        f"{summary['expected_units']:,.0f}",
        help="Fixed value: total batch size divided by Target Filling.",
    )
    e4.metric(
        "Usable filling batch",
        f"{summary['usable_filling_batch_g'] / 1000:.3f} kg",
        delta=f"{summary['actual_batch_usage_percentage']:.1f}% of total batch",
    )

    st.subheader("Input scenario")
    a1, a2, a3 = st.columns(3)
    a4, a5, a6 = st.columns(3)
    a1.metric(
        "Actual pastry average",
        f"{summary['actual_pastry_average']:.2f} g",
        delta=f"{summary['pastry_adjustment']:+.2f} g vs target",
    )
    a2.metric(
        "Input filling target",
        f"{summary['input_filling_target']:.2f} g",
        delta=f"{summary['filling_adjustment']:+.2f} g vs target",
    )
    a3.metric("Actual Units", f"{summary['input_actual_units']:,.0f}")
    a4.metric("Yield", f"{summary['input_yield']:.1f}%")
    a5.metric("Underweight", f"{summary['input_underweight']:.2f}%")
    a6.metric("Good Units", f"{summary['input_good_units']:,.0f}")

    st.divider()
    st.subheader(summary["recommendation_status"])
    if summary["constraint_met"]:
        st.success("The optimum is inside the selected maximum underweight limit.")
    else:
        st.warning(
            "No scenario inside the automatic range meets the selected underweight limit. The result shown has the highest Good Units inside the tested range."
        )

    r1, r2, r3 = st.columns(3)
    r4, r5, r6 = st.columns(3)
    r1.metric("Optimum filling target", f"{summary['optimum_filling_target']:.2f} g")
    r2.metric("Adjustment vs target", f"{summary['optimum_filling_adjustment']:+.2f} g")
    r3.metric("Yield", f"{summary['optimum_yield']:.1f}%")
    r4.metric("Actual Units", f"{summary['optimum_actual_units']:,.0f}")
    r5.metric("Underweight", f"{summary['optimum_underweight']:.2f}%")
    r6.metric("Good Units", f"{summary['optimum_good_units']:,.0f}")

    chart_figure = create_optimisation_chart(results_df=results_df, summary=summary)
    chart_png = chart_to_png_bytes(chart_figure)
    st.pyplot(chart_figure, width="stretch", clear_figure=False)
    st.caption("Static chart. Zoom and interactive controls have been removed.")
    st.download_button(
        "Download chart as PNG",
        data=chart_png,
        file_name="filling_optimisation_chart.png",
        mime="image/png",
    )
    plt.close(chart_figure)

    with st.expander("Calculation check"):
        st.code(
            f"Expected Units = {filling_batch_kg * 1000:,.1f} g ÷ {target_filling_weight:.2f} g = {summary['expected_units']:,.1f}"
        )
        st.code(
            f"Usable Filling Batch = {filling_batch_kg * 1000:,.1f} g × {actual_batch_usage_percentage:.2f}% = {summary['usable_filling_batch_g']:,.1f} g"
        )
        st.code(
            f"Actual Units = {summary['usable_filling_batch_g']:,.1f} g ÷ {summary['input_filling_target']:.2f} g = {summary['input_actual_units']:,.1f}"
        )
        st.code(
            f"Yield = {summary['input_actual_units']:,.1f} ÷ {summary['expected_units']:,.1f} × 100 = {summary['input_yield']:.2f}%"
        )
        st.code(
            f"Good Units = {summary['input_actual_units']:,.1f} × (1 - {summary['input_underweight']:.2f}%) = {summary['input_good_units']:,.1f}"
        )

    with st.expander("Scenario and variation check"):
        st.write(f"Pastry condition: {summary['pastry_condition']}")
        st.write(f"Variation method: {summary['variation_method']}")
        st.write(f"Pastry standard deviation used: {summary['pastry_sd_g']:.3f} g")
        st.write(
            f"Automatic filling range: {summary['minimum_tested_filling']:.2f} g to {summary['maximum_tested_filling']:.2f} g"
        )

    st.subheader("All filling scenarios")
    display_df = results_df.rename(
        columns={
            "filling_target": "Filling Target (g)",
            "filling_adjustment": "Adjustment vs Target (g)",
            "expected_units": "Expected Units",
            "actual_units": "Actual Units",
            "yield_percentage": "Yield (%)",
            "underweight_percentage": "Underweight (%)",
            "expected_seconds": "Expected Seconds",
            "good_units": "Good Units",
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
        data=results_df.to_csv(index=False),
        file_name="filling_optimisation_results.csv",
        mime="text/csv",
    )

with instructions_tab:
    show_instructions()
