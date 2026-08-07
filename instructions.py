import streamlit as st


def show_instructions():
    st.header("Purpose of the model")
    st.write(
        """
This model evaluates how pastry condition, filling target, process losses and process variation affect three production results:

- **Yield**
- **Underweight percentage**
- **Good Units**

It can recreate normal production conditions and deliberately unusual or extreme scenarios.
"""
    )
    st.info(
        """
Yield is based on total units produced from the **usable part of the filling batch**. Underweight products are not subtracted from Yield. They are subtracted only when Good Units are calculated.
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
        """**Meaning:** Approved pastry target from the product specification.

**What to enter:** Enter the standard pastry target, not the measured production result."""
    )
    st.subheader("Target filling weight (g)")
    st.write(
        """**Meaning:** Approved filling target from the product specification.

**What to enter:** Enter the standard filling target. This value is used to calculate Expected Units and remains fixed during the complete analysis."""
    )
    st.subheader("Target glaze weight (g)")
    st.write(
        """**Meaning:** Approved glaze weight per finished product.

**What to enter:** Enter the target glaze weight. Enter **0 g** when glaze is not included in the analysis."""
    )
    st.subheader("Filling batch size (kg)")
    st.write(
        """**Meaning:** Total batch produced before any losses.

**What to enter:** Enter the total filling batch in kilograms."""
    )
    st.subheader("Actual usable filling batch (%)")
    st.write(
        """**Meaning:** Percentage of the total filling batch that is really available to produce units after process losses, hold-up, transfer loss or wastage.

**What to enter:** Enter values such as **100%, 98%, 95% or 90%** depending on the real usable portion of the batch."""
    )
    st.latex(r"""\text{Usable Filling Batch} = \text{Total Filling Batch} \times \frac{\text{Actual Usable Batch \%}}{100}""")
    st.info(
        """This new variable lets you model situations where the full filling batch is not actually available for production."""
    )
    st.subheader("Permitted reduction below target product weight (%)")
    st.write(
        """**Meaning:** Approved percentage by which the finished-product weight may be below its total target weight.

**What to enter:** Enter the approved allowance. Enter **0%** when no reduction is permitted."""
    )
    st.latex(r"""\text{Minimum Allowed Weight} = \text{Target Product Weight} \times \left(1-\frac{\text{Permitted Reduction}}{100}\right)""")
    st.subheader("Maximum acceptable underweight (%)")
    st.write(
        """**Meaning:** Highest simulated seconds percentage allowed for a compliant optimum.

**What to enter:** Enter the product or production quality limit, such as **0%, 1%, 2% or 5%**."""
    )

    st.divider()
    st.header("2. Scenario Adjustments")
    st.write(
        """These inputs describe the actual or hypothetical scenario being evaluated. Both inputs accept negative and positive values."""
    )
    st.subheader("Pastry adjustment vs target (g)")
    st.write(
        """**Meaning:** Difference between the current pastry average and the target pastry.

- Negative value: pastry is lighter than target.
- Zero: pastry is at target.
- Positive value: pastry is heavier than target."""
    )
    st.latex(r"""\text{Actual Pastry Average} = \text{Target Pastry} + \text{Pastry Adjustment}""")
    st.subheader("Filling adjustment vs target (g)")
    st.write(
        """**Meaning:** Difference between the filling used in the input scenario and the target filling.

- Negative value: less filling than target.
- Zero: filling is at target.
- Positive value: extra filling."""
    )
    st.latex(r"""\text{Input Filling Target} = \text{Target Filling} + \text{Filling Adjustment}""")

    st.divider()
    st.header("3. Process Variation")
    st.subheader("Variation input method")
    st.write(
        "Select whether pastry and filling variation will be entered as standard deviation in grams or as percentage coefficient of variation."
    )
    st.latex(r"""\text{CV \%} = \frac{\text{Standard Deviation}}{\text{Average Weight}} \times 100""")
    st.subheader("Pastry variation")
    st.write(
        """**Meaning:** Natural spread of individual pastry weights around the actual pastry average.

Enter **0** for an exact scenario. In Standard Deviation mode, enter SD in grams. In Percentage mode, enter CV%."""
    )
    st.subheader("Filling variation")
    st.write(
        """**Meaning:** Natural depositor spread around every tested filling target.

Enter **0** when each filling target should be treated as exact. In Standard Deviation mode, enter SD in grams. In Percentage mode, enter CV%."""
    )

    st.divider()
    st.header("Expected Units")
    st.write(
        "Expected Units are fixed and are calculated only from the **total filling batch** and the Target Filling specification."
    )
    st.latex(r"""\text{Expected Units} = \frac{\text{Total Filling Batch in grams}}{\text{Target Filling}}""")
    st.write(
        "This means the comparison baseline always remains the original target using **100% of the initial filling batch**."
    )

    st.divider()
    st.header("Actual Units")
    st.write(
        "Actual Units change for every filling target on the horizontal axis and are also affected by the usable-batch percentage."
    )
    st.latex(r"""\text{Actual Units} = \frac{\text{Usable Filling Batch in grams}}{\text{Tested Filling Target}}""")
    st.write(
        "Extra filling produces fewer units. Less filling produces more units. Lower usable-batch percentage also reduces units."
    )

    st.divider()
    st.header("Yield — blue curve")
    st.write(
        "Yield measures total units produced compared with Expected Units. Underweight products are not subtracted from Yield."
    )
    st.latex(r"""\text{Yield} = \frac{\text{Actual Units}}{\text{Expected Units}} \times 100""")
    st.write("This is equivalent to:")
    st.latex(r"""\text{Yield} = \frac{\text{Usable Filling Batch}}{\text{Total Filling Batch}} \times \frac{\text{Target Filling}}{\text{Tested Filling Target}} \times 100""")
    st.success(
        "The blue curve therefore reflects both the filling target and the percentage of batch that is actually usable."
    )

    st.divider()
    st.header("Underweight — red curve")
    st.latex(r"""\text{Final Product Weight} = \text{Simulated Pastry} + \text{Simulated Filling} + \text{Target Glaze}""")
    st.latex(r"""\text{Underweight \%} = \frac{\text{Virtual Units Below Minimum Weight}}{\text{Total Virtual Units}} \times 100""")

    st.divider()
    st.header("Good Units — green curve")
    st.latex(r"""\text{Expected Seconds} = \text{Actual Units} \times \frac{\text{Underweight \%}}{100}""")
    st.latex(r"""\text{Good Units} = \text{Actual Units} - \text{Expected Seconds}""")
    st.write(
        "Good Units combine the unit benefit of using less filling with the quality loss created by underweights."
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

Filling target with the highest Good Units inside the selected underweight limit.
"""
    )
    st.info(
        "The chart is static. It does not include zoom, pan or interactive controls. The old yellow result box has been removed."
    )

    st.divider()
    st.header("Recommendation logic")
    st.markdown(
        """
1. The app evaluates every filling target in the automatic range.
2. It removes scenarios above the maximum acceptable underweight.
3. It selects the compliant scenario with the highest Good Units.
4. When no scenario complies, it shows the highest Good Units inside the tested range and displays a warning.
"""
    )

    st.divider()
    st.header("Important limitation")
    st.warning(
        """This model supports production decisions but does not replace actual checkweigher data, controlled trials, quality approval, approved product specifications or process-capability studies."""
    )
