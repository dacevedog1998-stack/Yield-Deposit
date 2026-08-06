import streamlit as st


def show_instructions():
    """Display the complete model instructions in simple language."""

    st.header("Purpose of this model")

    st.write(
        """
        This model helps production teams compare filling targets below,
        at and above the nominal filling weight.

        It can analyse normal production and situations where extra filling
        is deliberately added because the pastry is lighter than expected.
        """
    )

    st.divider()

    st.header("How to use it")

    st.markdown(
        """
        1. Enter the nominal pastry weight.
        2. Enter the minimum pastry weight expected in production.
        3. Enter nominal filling and glaze weights.
        4. Enter the filling batch size.
        5. Enter the permitted reduction below nominal product weight.
        6. Enter the maximum extra filling to test.
        7. Enter the maximum acceptable underweight percentage.
        8. Select **Run optimisation**.
        """
    )

    st.divider()

    st.header("How the simulation works")

    st.write(
        """
        The model creates thousands of virtual products. Pastry values are
        randomly generated and mildly biased toward the selected minimum.
        Filling and glaze also receive small random variations.
        """
    )

    st.write(
        """
        For each filling target, the model estimates final product weight,
        underweight percentage, produced units, expected seconds, good units
        and yield.
        """
    )

    st.divider()

    st.header("Two yield calculations")

    st.subheader("Filling yield")

    st.latex(
        r"""
        \text{Filling Yield}
        =
        \frac{\text{Nominal Filling}}
        {\text{Tested Filling}}
        \times 100
        """
    )

    st.write(
        """
        This only measures the effect of changing filling weight.
        Nominal filling equals 100%.
        """
    )

    st.subheader("Expected production yield")

    st.latex(
        r"""
        \text{Expected Production Yield}
        =
        \text{Recovery}
        \times
        \frac{\text{Nominal Filling}}
        {\text{Tested Filling}}
        \times
        \text{Good Product Rate}
        \times 100
        """
    )

    st.write(
        """
        This is the blue curve. It includes the fixed 98% recovery assumption,
        the filling adjustment and the estimated underweight loss.
        It is therefore closer to the operational yield than filling yield
        alone.
        """
    )

    st.divider()

    st.header("Why a result may repeat")

    st.write(
        """
        When the requested underweight limit cannot be reached inside the
        selected extra-filling range, the model chooses the lowest-risk target
        available. This is often the highest tested filling target.

        It is not presented as a compliant recommendation. The app displays
        **Best available within the tested range** and asks you to increase
        the maximum extra filling.
        """
    )

    st.divider()

    st.header("Recommendation logic")

    st.markdown(
        """
        - If one or more targets meet the underweight limit, the model selects
          the valid target with the most good units.
        - If no target meets the limit, the model selects the lowest-risk
          scenario available and displays a warning.
        """
    )

    st.divider()

    st.header("How to read the chart")

    st.markdown(
        """
        - **Blue:** expected production yield.
        - **Red:** expected underweight percentage.
        - **Green:** expected good units.
        - **Grey dotted line:** nominal filling.
        - **Purple dashed line:** selected filling.
        - The yield percentage is displayed above the selected point.
        - Move the mouse over a point to see its values.
        - Use the mouse wheel or the toolbar to zoom in and out.
        - Drag across the chart to zoom into a selected area.
        - Double-click the chart or use Reset Axes to return to the full view.
        """
    )

    st.divider()

    st.header("Important limitation")

    st.warning(
        """
        This is a simplified decision-support simulation. It does not replace
        quality checks, controlled production trials or real process data.
        A simulated 0.00% underweight means that none of the simulated products
        were underweight; it is not an absolute guarantee.
        """
    )
