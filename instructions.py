import streamlit as st


def show_instructions():
    """Display the complete model instructions."""

    st.header("Filling yield")

    st.latex(
        r"""
        \text{Nominal Units}
        =
        \frac{\text{Filling Batch}}
        {\text{Nominal Filling}}
        """
    )

    st.latex(
        r"""
        \text{Produced Units}
        =
        \frac{\text{Filling Batch}}
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

    st.markdown(
        """
        Example:

        - Batch: 257 kg
        - Nominal filling: 105 g
        - Tested filling: 110 g

        Nominal units = 257,000 ÷ 105 = approximately 2,448.

        Produced units = 257,000 ÷ 110 = approximately 2,336.

        Filling yield = 2,336 ÷ 2,448 = approximately **95.5%**.
        """
    )

    st.divider()

    st.header("How pastry affects the decision")

    st.write(
        """
        Pastry does not directly change filling yield. It changes the risk of
        the finished product becoming underweight.
        """
    )

    st.markdown(
        """
        If nominal pastry is 95 g and minimum pastry is 88 g, the pastry deficit
        is 7 g. Production may need approximately 7 g of extra filling to
        replace the missing pastry weight.

        This extra filling reduces filling yield because fewer units can be
        produced from the same filling batch.
        """
    )

    st.divider()

    st.header("Underweight and good units")

    st.write(
        """
        Underweight is calculated separately. It does not reduce the filling
        yield percentage.
        """
    )

    st.latex(
        r"""
        \text{Good Units}
        =
        \text{Produced Units}
        -
        \text{Expected Underweight Products}
        """
    )

    st.divider()

    st.header("Interactive chart")

    st.markdown(
        """
        - Blue: filling yield.
        - Red: underweight percentage.
        - Green: good units.
        - Grey dotted line: nominal filling.
        - Purple dashed line: selected filling.
        - Use the mouse wheel or toolbar to zoom.
        - Double-click to reset.
        """
    )

    st.warning(
        """
        Confirm the result through normal quality checks and a controlled
        production trial.
        """
    )
