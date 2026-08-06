import streamlit as st


def show_instructions():
    """Display the complete model instructions and input guide."""

    st.header("Purpose of the model")

    st.write(
        """
        This model evaluates how pastry weight, filling target and process
        variation affect three separate production results:

        - **Yield**
        - **Underweight percentage**
        - **Good Units**

        It can recreate normal production conditions and deliberately unusual
        or extreme scenarios.
        """
    )

    st.info(
        """
        Yield is based on total units produced. Underweight products are not
        subtracted from Yield. They are subtracted only when Good Units are
        calculated.
        """
    )

    st.divider()

    st.header("Input structure")

    st.write(
        """
        Inputs are organised into three sections:

        1. Product Targets
        2. Scenario Adjustments
        3. Process Variation
        """
    )

    st.divider()

    st.header("1. Product Targets")

    st.subheader("Target pastry weight (g)")

    st.write(
        """
        **Meaning:** Approved pastry target from the product specification.

        **What to enter:** Enter the standard pastry target, not the measured
        production result.
        """
    )

    st.markdown("Example: **95 g**")

    st.subheader("Target filling weight (g)")

    st.write(
        """
        **Meaning:** Approved filling target from the product specification.

        **What to enter:** Enter the standard filling target.

        This value is used to calculate Expected Units and remains fixed during
        the complete analysis.
        """
    )

    st.markdown("Example: **105 g**")

    st.subheader("Target glaze weight (g)")

    st.write(
        """
        **Meaning:** Approved glaze weight per finished product.

        **What to enter:** Enter the target glaze weight. Enter **0 g** when
        glaze is not included in the analysis.
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
        **Meaning:** Approved percentage by which the finished-product weight
        may be below its total target weight.

        **What to enter:** Enter the approved allowance. Enter **0%** when no
        reduction is permitted.
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
        **Meaning:** Highest simulated seconds percentage allowed for a
        compliant optimum.

        **What to enter:** Enter the product or production quality limit, such
        as **0%, 1%, 2% or 5%**.
        """
    )

    st.warning(
        """
        A simulated 0.00% result means none of the virtual products were below
        the minimum weight. It is not an absolute guarantee of zero real
        underweights.
        """
    )

    st.divider()

    st.header("2. Scenario Adjustments")

    st.write(
        """
        These two inputs describe the actual or hypothetical scenario being
        evaluated.

        Both inputs accept negative and positive values.
        """
    )

    st.subheader("Pastry adjustment vs target (g)")

    st.write(
        """
        **Meaning:** Difference between the current pastry average and the
        target pastry.

        **What to enter:**

        - Negative value: pastry is lighter than target.
        - Zero: pastry is at target.
        - Positive value: pastry is heavier than target.
        """
    )

    st.markdown(
        """
        Examples with a target of 95 g:

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
        **Meaning:** Difference between the filling used in the input scenario
        and the target filling.

        **What to enter:**

        - Negative value: less filling than target.
        - Zero: filling is at target.
        - Positive value: extra filling.
        """
    )

    st.markdown(
        """
        Examples with a target of 105 g:

        - `-10 g` → input filling target = **95 g**
        - `0 g` → input filling target = **105 g**
        - `+15 g` → input filling target = **120 g**
        """
    )

    st.latex(
        r"""
        \text{Input Filling Target}
        =
        \text{Target Filling}
        +
        \text{Filling Adjustment}
        """
    )

    st.info(
        """
        Unusual scenarios are allowed. You may deliberately enter very light
        pastry, heavy pastry, excessive filling or a large filling reduction to
        observe what happens to all three curves.
        """
    )

    st.divider()

    st.header("3. Process Variation")

    st.subheader("Variation input method")

    st.write(
        """
        Select whether pastry and filling variation will be entered as:

        - Standard deviation in grams, or
        - Percentage coefficient of variation.
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

    st.subheader("Pastry variation")

    st.write(
        """
        **Meaning:** Natural spread of individual pastry weights around the
        actual pastry average.

        **What to enter:**

        - Enter **0** for an exact scenario.
        - In Standard Deviation mode, enter SD in grams.
        - In Percentage mode, enter CV%.
        """
    )

    st.subheader("Filling variation")

    st.write(
        """
        **Meaning:** Natural depositor spread around every tested filling
        target.

        **What to enter:**

        - Enter **0** when each filling target should be treated as exact.
        - In Standard Deviation mode, enter SD in grams.
        - In Percentage mode, enter CV%.
        """
    )

    st.warning(
        """
        Variation cannot be negative. A negative average difference belongs in
        Pastry Adjustment or Filling Adjustment. Variation measures spread
        around an average, not direction.
        """
    )

    st.divider()

    st.header("Expected Units")

    st.write(
        """
        Expected Units are fixed and are calculated only from the filling batch
        and the Target Filling specification.
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
        not change when different filling targets are tested.
        """
    )

    st.divider()

    st.header("Actual Units")

    st.write(
        """
        Actual Units change for every filling target on the horizontal axis.
        """
    )

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
        Extra filling produces fewer units. Less filling produces more units.
        """
    )

    st.divider()

    st.header("Yield — blue curve")

    st.write(
        """
        Yield measures total units produced compared with Expected Units.

        Underweight products are not subtracted from Yield.
        """
    )

    st.latex(
        r"""
        \text{Yield}
        =
        \frac{\text{Actual Units}}
        {\text{Expected Units}}
        \times 100
        """
    )

    st.write("This is equivalent to:")

    st.latex(
        r"""
        \text{Yield}
        =
        \frac{\text{Target Filling}}
        {\text{Tested Filling Target}}
        \times 100
        """
    )

    st.markdown(
        """
        Example with target filling of 105 g:

        - Tested target 105 g → **100% Yield**
        - Tested target 110 g → **95.45% Yield**
        - Tested target 98 g → **107.14% Yield**
        """
    )

    st.success(
        """
        The blue curve therefore decreases as the filling target increases.
        It no longer rises and falls with the Good Units curve.
        """
    )

    st.divider()

    st.header("Underweight — red curve")

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

    st.latex(
        r"""
        \text{Underweight \%}
        =
        \frac{\text{Virtual Units Below Minimum Weight}}
        {\text{Total Virtual Units}}
        \times 100
        """
    )

    st.write(
        """
        Underweight normally decreases when more filling is added.
        """
    )

    st.divider()

    st.header("Good Units — green curve")

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

    st.write(
        """
        Good Units combine the unit benefit of using less filling with the
        quality loss created by underweights.

        This curve normally rises, reaches an optimum and then falls.
        """
    )

    st.divider()

    st.header("How the chart is generated")

    st.write(
        """
        The horizontal axis is Filling Target in grams per unit.

        The app automatically evaluates:

        - At least 15 g below Target Filling.
        - At least 15 g above Target Filling.
        - The exact input filling scenario.
        - The approximate filling value that compensates for the pastry
          adjustment.

        The range expands when an extreme scenario is entered.
        """
    )

    st.divider()

    st.header("How to read the static chart")

    st.markdown(
        """
        **Blue line — Yield**

        Total units produced compared with fixed Expected Units.

        **Red line — Underweight Percentage**

        Simulated percentage below the minimum permitted finished weight.

        **Green line — Good Units**

        Actual Units remaining after expected seconds are removed.

        **Grey dashed line — Target Filling**

        Approved filling specification.

        **Purple dotted line — Input Scenario**

        Filling adjustment entered by the user.

        **Orange dashed line — Optimum**

        Filling target with the highest Good Units inside the selected
        underweight limit.
        """
    )

    st.info(
        """
        The chart is now static. It does not include zoom, pan or interactive
        controls.
        """
    )

    st.divider()

    st.header("Worked example: 5 g extra filling")

    st.markdown(
        """
        - Target filling = **105 g**
        - Filling adjustment = **+5 g**
        - Input filling target = **110 g**
        - Filling batch = **257 kg**
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
        \text{Actual Units}
        =
        \frac{257000}{110}
        =
        2336.4
        """
    )

    st.latex(
        r"""
        \text{Yield}
        =
        \frac{2336.4}{2447.6}
        \times 100
        =
        95.45\%
        """
    )

    st.write(
        """
        This Yield remains 95.45% regardless of the underweight percentage.
        Underweights reduce Good Units, not Yield.
        """
    )

    st.divider()

    st.header("Worked example: light pastry")

    st.markdown(
        """
        - Target pastry = **95 g**
        - Pastry adjustment = **-7 g**
        - Actual pastry average = **88 g**
        - Target filling = **105 g**
        - Filling adjustment = **+7 g**
        - Input filling target = **112 g**
        """
    )

    st.write(
        """
        Extra filling may compensate for missing pastry weight. Yield falls
        because fewer total units are produced, while the red curve shows
        whether the extra filling sufficiently reduces underweights.
        """
    )

    st.divider()

    st.header("Worked example: heavy pastry")

    st.markdown(
        """
        - Target pastry = **95 g**
        - Pastry adjustment = **+7 g**
        - Actual pastry average = **102 g**
        - Target filling = **105 g**
        - Filling adjustment = **-7 g**
        - Input filling target = **98 g**
        """
    )

    st.write(
        """
        Heavy pastry may permit a lower filling target. Yield may exceed 100%
        because more total units can be produced from the same filling batch.
        """
    )

    st.divider()

    st.header("Recommendation logic")

    st.markdown(
        """
        1. The app evaluates every filling target in the automatic range.
        2. It removes scenarios above the maximum acceptable underweight.
        3. It selects the compliant scenario with the highest Good Units.
        4. When no scenario complies, it shows the highest Good Units inside
           the tested range and displays a warning.
        """
    )

    st.divider()

    st.header("Important limitation")

    st.warning(
        """
        This model supports production decisions but does not replace actual
        checkweigher data, controlled trials, quality approval, approved
        product specifications or process-capability studies.
        """
    )
