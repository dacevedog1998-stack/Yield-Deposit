import streamlit as st


def show_instructions():
    """Display the complete model guide in clear production language."""

    st.header("Purpose of the model")

    st.write(
        """
        This model evaluates how pastry condition, filling target and process
        variation affect:

        - Production Yield.
        - Underweight percentage.
        - Good Units.

        It can recreate normal production conditions and deliberately unusual
        or extreme scenarios.
        """
    )

    st.info(
        """
        You can enter lighter or heavier pastry and less or extra filling.
        The model does not restrict a scenario simply because it is uncommon.
        It only requires the resulting pastry and filling weights to remain
        greater than zero.
        """
    )

    st.divider()

    st.header("Input structure")

    st.write(
        """
        Inputs are divided into three sections:

        1. **Product Targets**
        2. **Scenario Adjustments**
        3. **Process Variation**
        """
    )

    st.divider()

    st.header("1. Product Targets")

    st.subheader("Target pastry weight (g)")

    st.write(
        """
        **Meaning:** The approved pastry target in the product specification.

        **What to enter:** Enter the standard pastry weight, not the current
        measured production value.
        """
    )

    st.markdown("Example: **95 g**")

    st.subheader("Target filling weight (g)")

    st.write(
        """
        **Meaning:** The approved filling target in the product specification.

        **What to enter:** Enter the standard filling weight. This value is
        used to calculate Expected Units and stays fixed throughout the
        analysis.
        """
    )

    st.markdown("Example: **105 g**")

    st.subheader("Target glaze weight (g)")

    st.write(
        """
        **Meaning:** The approved glaze weight per unit.

        **What to enter:** Enter the target glaze weight. Enter **0 g** when the
        product has no glaze or glaze is excluded from the analysis.
        """
    )

    st.subheader("Filling batch size (kg)")

    st.write(
        """
        **Meaning:** Total filling available for the production run.

        **What to enter:** Enter the actual batch size in kilograms.
        """
    )

    st.markdown("Example: **257.675 kg**")

    st.subheader(
        "Permitted reduction below target product weight (%)"
    )

    st.write(
        """
        **Meaning:** The approved percentage by which finished-product weight
        may be below its target total weight.

        **What to enter:** Enter the approved product allowance. Enter **0%**
        when no reduction is permitted.
        """
    )

    st.latex(
        r"""
        \text{Minimum Allowed Weight}
        =
        \text{Target Product Weight}
        \times
        \left(
        1-
        \frac{\text{Permitted Reduction}}{100}
        \right)
        """
    )

    st.subheader("Maximum acceptable underweight (%)")

    st.write(
        """
        **Meaning:** The highest simulated underweight or seconds percentage
        allowed for a compliant recommendation.

        **What to enter:** Enter the quality limit used for the product, such
        as **0%, 1%, 2% or 5%**.
        """
    )

    st.warning(
        """
        A simulated result of 0.00% means none of the virtual units were below
        the minimum. It is not an absolute guarantee of zero real underweights.
        """
    )

    st.divider()

    st.header("2. Scenario Adjustments")

    st.write(
        """
        These inputs describe the production condition you want to recreate or
        test. Both fields accept negative and positive values.
        """
    )

    st.subheader("Pastry adjustment vs target (g)")

    st.write(
        """
        **Meaning:** How much lighter or heavier the actual pastry average is
        compared with the target pastry.

        **What to enter:**

        - Enter a negative value for lighter pastry.
        - Enter zero when pastry is at target.
        - Enter a positive value for heavier pastry.
        """
    )

    st.markdown(
        """
        Examples with a 95 g target:

        - `-7 g` → actual pastry average = **88 g**
        - `0 g` → actual pastry average = **95 g**
        - `+7 g` → actual pastry average = **102 g**
        """
    )

    st.latex(
        r"""
        \text{Actual Pastry Average}
        =
        \text{Target Pastry}
        +
        \text{Pastry Adjustment}
        """
    )

    st.subheader("Filling adjustment vs target (g)")

    st.write(
        """
        **Meaning:** How much less or extra filling is used in the input
        scenario compared with the target filling.

        **What to enter:**

        - Enter a negative value to test less filling.
        - Enter zero to use target filling.
        - Enter a positive value to test extra filling.
        """
    )

    st.markdown(
        """
        Examples with a 105 g target:

        - `-10 g` → actual filling target = **95 g**
        - `0 g` → actual filling target = **105 g**
        - `+15 g` → actual filling target = **120 g**
        """
    )

    st.latex(
        r"""
        \text{Actual Filling Target}
        =
        \text{Target Filling}
        +
        \text{Filling Adjustment}
        """
    )

    st.info(
        """
        These fields may be used for unusual scenarios. For example, you may
        deliberately enter very light pastry, excessive filling or a large
        filling reduction to see the effect on all three curves.
        """
    )

    st.divider()

    st.header("3. Process Variation")

    st.subheader("Variation input method")

    st.write(
        """
        Select how pastry and filling variation will be entered.
        """
    )

    st.markdown(
        """
        **Percentage (CV)**

        Use this when variation is known as coefficient of variation.
        """
    )

    st.latex(
        r"""
        \text{CV \%}
        =
        \frac{\text{Standard Deviation}}
        {\text{Average Weight}}
        \times 100
        """
    )

    st.markdown(
        """
        **Standard deviation (g)**

        Use this when standard deviation is already known in grams.
        """
    )

    st.subheader("Pastry variation")

    st.write(
        """
        **Meaning:** Natural spread of individual pastry weights around the
        actual pastry average.

        **What to enter:**

        - Enter **0** for an exact or deterministic scenario.
        - In CV mode, enter the measured percentage.
        - In SD mode, enter the measured standard deviation in grams.
        """
    )

    st.subheader("Filling variation")

    st.write(
        """
        **Meaning:** Natural depositor spread around every tested filling
        target.

        **What to enter:**

        - Enter **0** when every filling target should be treated as exact.
        - In CV mode, enter the measured percentage.
        - In SD mode, enter the measured standard deviation in grams.
        """
    )

    st.warning(
        """
        Variation cannot be negative. A negative average difference belongs in
        the signed pastry or filling adjustment field. Variation only measures
        spread around an average.
        """
    )

    st.divider()

    st.header("Expected Units remain fixed")

    st.write(
        """
        Expected Units are based only on the filling batch and the target
        filling specification.
        """
    )

    st.latex(
        r"""
        \text{Expected Units}
        =
        \frac{\text{Filling Batch in grams}}
        {\text{Target Filling}}
        """
    )

    st.write(
        """
        Expected Units do not change when pastry is lighter or heavier and do
        not change when a different filling scenario is tested.
        """
    )

    st.divider()

    st.header("Actual Units change with filling")

    st.latex(
        r"""
        \text{Actual Units}
        =
        \frac{\text{Filling Batch in grams}}
        {\text{Tested Filling Target}}
        """
    )

    st.write(
        """
        Extra filling reduces Actual Units. Less filling increases Actual
        Units.
        """
    )

    st.divider()

    st.header("Underweight calculation")

    st.latex(
        r"""
        \text{Final Product Weight}
        =
        \text{Simulated Pastry}
        +
        \text{Simulated Filling}
        +
        \text{Target Glaze}
        """
    )

    st.write(
        """
        A virtual product is underweight when its final weight is below the
        minimum allowed product weight.
        """
    )

    st.latex(
        r"""
        \text{Underweight \%}
        =
        \frac{\text{Virtual Units Below Minimum}}
        {\text{Total Virtual Units}}
        \times 100
        """
    )

    st.divider()

    st.header("Good Units")

    st.latex(
        r"""
        \text{Expected Seconds}
        =
        \text{Actual Units}
        \times
        \frac{\text{Underweight \%}}{100}
        """
    )

    st.latex(
        r"""
        \text{Good Units}
        =
        \text{Actual Units}
        -
        \text{Expected Seconds}
        """
    )

    st.divider()

    st.header("Production Yield")

    st.write(
        """
        Production Yield compares the expected good output from the tested
        scenario with the fixed Expected Units from the product target.
        """
    )

    st.latex(
        r"""
        \text{Production Yield}
        =
        \frac{\text{Good Units}}
        {\text{Expected Units}}
        \times 100
        """
    )

    st.write("This is equivalent to:")

    st.latex(
        r"""
        \text{Production Yield}
        =
        \left(
        \frac{\text{Actual Units}}
        {\text{Expected Units}}
        \times 100
        \right)
        \times
        \left(
        1-
        \frac{\text{Underweight \%}}{100}
        \right)
        """
    )

    st.info(
        """
        The blue Production Yield curve therefore changes for two reasons:

        - Actual Units change when the filling target changes.
        - Good output changes when underweights increase or decrease.
        """
    )

    st.divider()

    st.header("How the filling curve is created")

    st.write(
        """
        The horizontal axis remains **Filling Target (g per unit)**.

        The app automatically tests:

        - At least 15 g below target filling.
        - At least 15 g above target filling.
        - The exact input scenario.
        - The approximate compensation point for the pastry adjustment.

        The range expands automatically when an extreme scenario is entered.
        """
    )

    st.divider()

    st.header("How to read the three curves")

    st.markdown(
        """
        **Blue solid curve — Production Yield**

        Final yield after underweight units are removed.

        **Red curve — Underweight Percentage**

        Estimated percentage of units below minimum allowed product weight.

        **Green dashed curve — Good Units**

        Number of acceptable units expected from the filling batch.

        **Grey dotted line — Target Filling**

        Filling specification used to calculate fixed Expected Units.

        **Purple dashed line — Input Scenario**

        The filling adjustment entered in the Scenario section.

        **Orange dash-dot line — Optimum**

        The filling target with the highest Good Units inside the selected
        underweight limit.
        """
    )

    st.write(
        """
        Production Yield and Good Units are mathematically related, so their
        curves have the same general shape. They use different axes, line
        styles and markers so that both remain visible.
        """
    )

    st.subheader("Interactive controls")

    st.markdown(
        """
        - Move the mouse over the curves to inspect values.
        - Use the mouse wheel or toolbar to zoom.
        - Drag across the graph to zoom into an area.
        - Double-click the graph to reset.
        """
    )

    st.divider()

    st.header("Worked example: target condition")

    st.markdown(
        """
        - Target pastry: **95 g**
        - Target filling: **105 g**
        - Filling batch: **257 kg**
        - Pastry adjustment: **0 g**
        - Filling adjustment: **0 g**
        - Underweight: **0%**
        """
    )

    st.latex(
        r"""
        \text{Expected Units}
        =
        \frac{257000}{105}
        =
        2447.6
        """
    )

    st.latex(
        r"""
        \text{Production Yield}
        =
        \frac{2447.6}{2447.6}
        \times 100
        =
        100\%
        """
    )

    st.divider()

    st.header("Worked example: 5 g extra filling")

    st.latex(
        r"""
        \text{Actual Units}
        =
        \frac{257000}{110}
        =
        2336.4
        """
    )

    st.write(
        """
        If the simulated underweight result is 0%:
        """
    )

    st.latex(
        r"""
        \text{Production Yield}
        =
        \frac{2336.4}{2447.6}
        \times 100
        =
        95.45\%
        """
    )

    st.write(
        """
        If underweight is 2%, Good Units and Production Yield are reduced by
        that quality loss.
        """
    )

    st.divider()

    st.header("Worked example: light pastry")

    st.markdown(
        """
        - Target pastry: **95 g**
        - Pastry adjustment: **-7 g**
        - Actual pastry average: **88 g**
        - Target filling: **105 g**
        - Filling adjustment: **+7 g**
        - Actual filling target: **112 g**
        """
    )

    st.write(
        """
        The extra filling may compensate for missing pastry weight, but Actual
        Units fall because more filling is used in every product.
        """
    )

    st.divider()

    st.header("Worked example: heavy pastry")

    st.markdown(
        """
        - Target pastry: **95 g**
        - Pastry adjustment: **+7 g**
        - Actual pastry average: **102 g**
        - Target filling: **105 g**
        - Filling adjustment: **-7 g**
        - Actual filling target: **98 g**
        """
    )

    st.write(
        """
        Heavy pastry may permit less filling while keeping final product weight
        above the minimum. In this case Production Yield may exceed 100%.
        """
    )

    st.divider()

    st.header("Exact versus variable scenarios")

    st.write(
        """
        When both variations are 0, every virtual product has exactly the same
        pastry and filling weight. The red curve may therefore change sharply
        from 100% underweight to 0%.

        Enter measured pastry and filling variation to produce a gradual curve
        that better represents a variable production process.
        """
    )

    st.divider()

    st.header("Recommendation logic")

    st.markdown(
        """
        1. Every filling target in the automatic range is evaluated.
        2. Targets above the maximum acceptable underweight are excluded from
           the compliant set.
        3. The compliant target with the highest Good Units is selected.
        4. When no target complies, the app shows the highest-output option
           inside the tested range and displays a warning.
        """
    )

    st.divider()

    st.header("Important limitation")

    st.warning(
        """
        This is a decision-support simulation. It does not replace:

        - Actual checkweigher results.
        - Controlled production trials.
        - Quality approval.
        - Product specifications.
        - Process-capability studies.
        """
    )
