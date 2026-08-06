# Filling Optimisation Model — Complete V2

## Final model logic

### Expected Units remain fixed

```text
Expected Units = Filling Batch / Target Filling
```

### Actual Units vary with every tested filling target

```text
Actual Units = Filling Batch / Tested Filling Target
```

### Underweight units are removed

```text
Good Units = Actual Units × (1 - Underweight Rate)
```

### Final Production Yield

```text
Production Yield = Good Units / Expected Units × 100
```

## Inputs

### 1. Product Targets

- Target pastry
- Target filling
- Target glaze
- Filling batch
- Permitted finished-weight reduction
- Maximum acceptable underweight

### 2. Scenario Adjustments

- Pastry adjustment vs target: accepts negative and positive values
- Filling adjustment vs target: accepts negative and positive values

### 3. Process Variation

Choose:

- Standard deviation in grams, or
- Percentage coefficient of variation

Then enter pastry and filling variation.

## Graph

The graph always contains:

- Blue solid curve: Production Yield
- Red curve: Underweight %
- Green dashed curve: Good Units
- Grey line: Target Filling
- Purple line: Input Scenario
- Orange line: Optimum

The x-axis remains Filling Target and is reversed to match the original graph:
higher filling is on the left and lower filling is on the right.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```
