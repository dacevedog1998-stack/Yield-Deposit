# Filling Optimisation Model — Correct Filling Yield

## Yield definition

```text
Nominal units = filling batch / nominal filling
Produced units = filling batch / tested filling
Filling yield = produced units / nominal units × 100
```

Underweight is calculated separately and only affects Good Units.

## Pastry compensation

If pastry is below nominal, extra filling may be required to replace the
missing pastry weight.

Example:

- Nominal pastry: 95 g
- Minimum pastry: 88 g
- Pastry deficit: 7 g

Testing approximately 7 g of extra filling shows the trade-off between
finished-product compliance and filling yield.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```
