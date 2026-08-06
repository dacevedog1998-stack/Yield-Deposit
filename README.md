# Filling Optimisation Model

This Streamlit application evaluates filling targets when current pastry is:

- Lighter than nominal
- Equal to nominal
- Heavier than nominal

The model can test filling targets below and above nominal.

## Main logic

```text
Nominal units = filling batch / nominal filling
Produced units = filling batch / tested filling
Filling yield = produced units / nominal units × 100
```

Underweight is calculated separately from simulated final product weight.

```text
Final product weight = pastry + filling + glaze
Good units = produced units - expected seconds
```

## Main inputs

- Nominal pastry, filling and glaze
- Current pastry average weight
- Pastry, filling and glaze process variation
- Filling batch size
- Permitted finished-product weight reduction
- Maximum acceptable underweight
- Maximum filling reduction to evaluate
- Maximum extra filling to evaluate

The Instructions tab explains what every input means and what value should be
entered.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Upload the complete folder to GitHub and deploy `app.py` through Streamlit
Community Cloud.
