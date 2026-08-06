import streamlit as st


def show_instructions():
    """Display the complete user guide and model explanation."""

    st.header("Purpose of this model")

    st.write(
        """
        This model helps production teams evaluate the most suitable filling
        target when pastry is lighter, equal to or heavier than its nominal
        weight.

        It compares:

        - Filling yield.
        - Expected underweight percentage.
        - Expected seconds.
        - Expected good units.
        """
    )

    st.info(
        """
        Light pastry may require extra filling.

        Heavy pastry may allow a lower filling target.

        The model tests both directions.
        """
    )

    st.divider()

    st.header("Quick guide: what value should I enter?")

    st.markdown(
        """
        | Input | What it means | What value should be entered? |
        |---|---|---|
        | **Nominal pastry weight** | Standard pastry weight in the product specification | Enter the approved target, for example **95 g** |
        | **Nominal filling weight** | Standard filling target | Enter the approved target, for example **105 g** |
        | **Nominal glaze weight** | Standard glaze per unit | Enter the approved value, or **0 g** when glaze is not included |
        | **Current pastry average weight** | Average pastry currently being produced | Weigh a sample and enter its average; it may be below, equal to or above nominal |
        | **Pastry process variation** | Natural spread around the current pastry average | Use **0%** for an exact scenario; use measured coefficient of variation when available |
        | **Filling process variation** | Depositor inconsistency around each filling target | Use **0%** for an exact scenario; use measured variation when available |
        | **Glaze process variation** | Natural glaze inconsistency | Use **0%** when glaze is exact or excluded; otherwise use measured variation |
        | **Filling batch size** | Total filling available for the run | Enter the actual batch quantity in kilograms |
        | **Permitted reduction below nominal weight** | Allowed reduction from nominal finished-product weight | Enter the approved product allowance, including **0%** when no reduction is allowed |
        | **Maximum acceptable underweight** | Highest seconds percentage production will accept | Enter the quality limit, for example **0%, 1% or 2%** |
        | **Maximum filling reduction to evaluate** | How far below nominal filling the model may test | Use this when pastry is heavier; a good starting value is the pastry excess |
        | **Maximum extra filling to evaluate** | How far above nominal filling the model may test | Use this when pastry is lighter; a good starting value is the pastry deficit |
        """
    )

    st.divider()

    st.header("Product specification inputs")

    st.subheader("Nominal pastry weight")

    st.write(
        """
        This is the standard pastry weight defined in the approved product
        specification.

        Enter the target, not the current measured value.
        """
    )

    st.markdown(
        """
        Example:

        **Nominal pastry = 95 g**
        """
    )

    st.subheader("Nominal filling weight")

    st.write(
        """
        This is the normal filling target defined in the product specification.

        It represents 100% filling yield.
        """
    )

    st.markdown(
        """
        Example:

        **Nominal filling = 105 g**
        """
    )

    st.subheader("Nominal glaze weight")

    st.write(
        """
        Enter the standard glaze weight per unit.

        Use 0 g when:

        - The product has no glaze.
        - Glaze is not part of the analysis.
        """
    )

    st.divider()

    st.header("Current production condition")

    st.subheader("Current pastry average weight")

    st.write(
        """
        This input represents the average pastry weight currently being
        produced.

        It is different from nominal pastry.
        """
    )

    st.markdown(
        """
        Examples:

        - Nominal 95 g, current 88 g → pastry is **7 g light**
        - Nominal 95 g, current 95 g → pastry is **at nominal**
        - Nominal 95 g, current 102 g → pastry is **7 g heavy**
        """
    )

    st.write(
        """
        Recommended method:

        1. Weigh a representative pastry sample.
        2. Calculate the average.
        3. Enter that average in this field.
        """
    )

    st.subheader("Pastry process variation (%)")

    st.write(
        """
        This represents how much individual pastry weights vary around the
        current average.

        The model treats this value as a coefficient of variation:
        """
    )

    st.latex(
        r"""
        \text{Variation \%}
        =
        \frac{\text{Standard Deviation}}
        {\text{Average Weight}}
        \times 100
        """
    )

    st.markdown(
        """
        Use:

        - **0%** for a simple exact-weight scenario.
        - A measured value when actual sample data is available.

        Example:

        - Average pastry = 95 g
        - Standard deviation = 2 g
        - Variation = 2 ÷ 95 × 100 = **2.1%**
        """
    )

    st.subheader("Filling process variation (%)")

    st.write(
        """
        This represents natural depositor inconsistency around each tested
        filling target.

        It does not change the target deliberately.
        """
    )

    st.markdown(
        """
        Use:

        - **0%** when the filling target should be treated as exact.
        - A measured value when depositor data is available.

        Example:

        Target = 110 g with variation may produce individual values such as
        109.5 g, 110.2 g and 110.7 g.
        """
    )

    st.subheader("Glaze process variation (%)")

    st.write(
        """
        This represents natural glaze variation around the nominal glaze
        weight.

        Use 0% when glaze is exact, negligible or excluded from the analysis.
        """
    )

    st.divider()

    st.header("Production and quality inputs")

    st.subheader("Filling batch size")

    st.write(
        """
        Enter the total filling available for the production run in kilograms.

        The model converts it to grams before calculating units.
        """
    )

    st.markdown(
        """
        Example:

        **257.675 kg = 257,675 g**
        """
    )

    st.subheader("Permitted reduction below nominal weight")

    st.write(
        """
        This is the approved percentage by which the finished product may be
        below nominal weight.
        """
    )

    st.latex(
        r"""
        \text{Minimum Allowed Weight}
        =
        \text{Nominal Product Weight}
        \times
        \left(
        1-
        \frac{\text{Permitted Reduction}}{100}
        \right)
        """
    )

    st.markdown(
        """
        Example:

        - Nominal finished weight = 200 g
        - Permitted reduction = 5%
        - Minimum allowed weight = 190 g

        Enter **0%** when the product may not be below nominal.
        """
    )

    st.subheader("Maximum acceptable underweight (%)")

    st.write(
        """
        This is the highest percentage of products below the minimum allowed
        weight that the model may accept as compliant.
        """
    )

    st.markdown(
        """
        Typical examples:

        - **0%** → search for no simulated underweights.
        - **1%** → allow up to 1% simulated underweights.
        - **2%** → allow up to 2% simulated underweights.

        Use the actual quality requirement approved for the product.
        """
    )

    st.warning(
        """
        A simulated 0.00% result means that none of the virtual products were
        underweight. It is not an absolute guarantee of zero real defects.
        """
    )

    st.divider()

    st.header("Filling range inputs")

    st.subheader("Maximum filling reduction to evaluate")

    st.write(
        """
        This allows the model to test filling targets below nominal.

        It is useful when current pastry is heavier than nominal.
        """
    )

    st.markdown(
        """
        Example:

        - Nominal pastry = 95 g
        - Current pastry = 102 g
        - Pastry excess = 7 g

        A reasonable starting value is:

        **Maximum filling reduction = 7 g**

        With nominal filling of 105 g, the lowest tested target will be 98 g.
        """
    )

    st.subheader("Maximum extra filling to evaluate")

    st.write(
        """
        This allows the model to test filling targets above nominal.

        It is useful when current pastry is lighter than nominal.
        """
    )

    st.markdown(
        """
        Example:

        - Nominal pastry = 95 g
        - Current pastry = 88 g
        - Pastry deficit = 7 g

        A reasonable starting value is:

        **Maximum extra filling = at least 7 g**

        With nominal filling of 105 g, the model should test at least up to
        112 g.
        """
    )

    st.subheader(
        "Difference between filling range and process variation"
    )

    st.markdown(
        """
        **Maximum filling reduction / maximum extra filling**

        - Deliberately changes the target.
        - Represents an engineering or production decision.

        **Filling process variation**

        - Does not deliberately change the target.
        - Represents natural depositor inconsistency around the target.
        """
    )

    st.divider()

    st.header("How the model works")

    st.write(
        """
        The model uses Monte Carlo simulation.

        It creates thousands of virtual products for every tested filling
        target.
        """
    )

    st.markdown(
        """
        For each target, the model:

        1. Generates pastry weights around the current pastry average.
        2. Generates filling weights around the tested filling target.
        3. Generates glaze weights when glaze is included.
        4. Adds pastry, filling and glaze.
        5. Compares final weight with the minimum allowed weight.
        6. Calculates underweight percentage.
        7. Calculates produced units from the filling batch.
        8. Calculates filling yield.
        9. Calculates expected seconds.
        10. Calculates expected good units.
        """
    )

    st.latex(
        r"""
        \text{Final Product Weight}
        =
        \text{Pastry}
        +
        \text{Filling}
        +
        \text{Glaze}
        """
    )

    st.divider()

    st.header("Filling yield calculation")

    st.latex(
        r"""
        \text{Nominal Units}
        =
        \frac{\text{Filling Batch in grams}}
        {\text{Nominal Filling}}
        """
    )

    st.latex(
        r"""
        \text{Produced Units}
        =
        \frac{\text{Filling Batch in grams}}
        {\text{Tested Filling}}
        """
    )

    st.latex(
        r"""
        \text{Filling Yield}
        =
        \frac{\text{Produced Units}}
        {\text{Nominal Units}}
        \times 100
        """
    )

    st.write(
        """
        Filling yield depends on filling used per unit.

        Pastry weight affects underweight risk, but it does not directly enter
        the filling-yield formula.
        """
    )

    st.divider()

    st.header("Underweight, seconds and good units")

    st.latex(
        r"""
        \text{Underweight Percentage}
        =
        \frac{\text{Virtual Products Below Minimum Weight}}
        {\text{Total Virtual Products}}
        \times 100
        """
    )

    st.latex(
        r"""
        \text{Expected Seconds}
        =
        \text{Produced Units}
        \times
        \frac{\text{Underweight Percentage}}{100}
        """
    )

    st.latex(
        r"""
        \text{Good Units}
        =
        \text{Produced Units}
        -
        \text{Expected Seconds}
        """
    )

    st.info(
        """
        Underweight affects expected seconds and good units.

        It does not directly reduce the filling-yield percentage because the
        filling has already been used.
        """
    )

    st.divider()

    st.header("How the recommendation is selected")

    st.markdown(
        """
        1. The model tests every filling target inside the selected lower and
           upper range.
        2. It identifies targets within the acceptable underweight limit.
        3. Among compliant targets, it selects the target with the highest
           expected good units.
        4. If none comply, it shows the lowest-risk option inside the tested
           range and displays a warning.
        """
    )

    st.warning(
        """
        “Best available within the tested range” is not a compliant result.

        Increase the range or review the process assumptions.
        """
    )

    st.divider()

    st.header("Worked example: pastry is light")

    st.markdown(
        """
        - Nominal pastry = 95 g
        - Current pastry = 88 g
        - Nominal filling = 105 g
        - Filling batch = 257 kg
        - Pastry deficit = 7 g
        """
    )

    st.write(
        """
        A sensible starting point is to test at least 7 g of extra filling.
        """
    )

    st.latex(
        r"""
        \text{Nominal Units}
        =
        \frac{257000}{105}
        =
        2447.6
        """
    )

    st.latex(
        r"""
        \text{Units at 112 g Filling}
        =
        \frac{257000}{112}
        =
        2294.6
        """
    )

    st.latex(
        r"""
        \text{Yield}
        =
        \frac{2294.6}{2447.6}
        \times 100
        =
        93.75\%
        """
    )

    st.write(
        """
        Extra filling protects final weight, but filling yield decreases.
        """
    )

    st.divider()

    st.header("Worked example: pastry is heavy")

    st.markdown(
        """
        - Nominal pastry = 95 g
        - Current pastry = 102 g
        - Nominal filling = 105 g
        - Pastry excess = 7 g
        """
    )

    st.write(
        """
        A sensible starting point is to test a filling reduction of up to 7 g.
        """
    )

    st.latex(
        r"""
        \text{Units at 98 g Filling}
        =
        \frac{257000}{98}
        =
        2622.4
        """
    )

    st.latex(
        r"""
        \text{Yield}
        =
        \frac{2622.4}{2447.6}
        \times 100
        =
        107.14\%
        """
    )

    st.write(
        """
        Heavy pastry may allow a lower filling target while the final product
        remains within specification.
        """
    )

    st.divider()

    st.header("How to read the chart")

    st.markdown(
        """
        **Blue line — Filling Yield**

        Shows the yield impact of each tested filling target.

        **Red line — Underweight Percentage**

        Shows the estimated percentage below minimum allowed weight.

        **Green line — Good Units**

        Shows produced units after expected seconds are removed.

        **Grey dotted line — Nominal Filling**

        Shows the standard filling target.

        **Purple dashed line — Selected Filling**

        Shows the target selected by the model.
        """
    )

    st.subheader("Interactive controls")

    st.markdown(
        """
        - Move the mouse over a point to view its values.
        - Use the mouse wheel or toolbar to zoom in and out.
        - Drag across the chart to zoom into an area.
        - Double-click to reset the axes.
        """
    )

    st.divider()

    st.header("Important limitations")

    st.warning(
        """
        This is a decision-support simulation. It does not replace:

        - Quality checks.
        - Checkweigher results.
        - Controlled production trials.
        - Actual process-capability studies.
        - Approved product specifications.
        """
    )

    st.write(
        """
        Model accuracy improves when real measurements are entered for pastry,
        filling and glaze variation.
        """
    )

    st.success(
        """
        The model does not simply maximise yield.

        It searches for the highest expected good units while respecting the
        selected underweight requirement.
        """
    )
