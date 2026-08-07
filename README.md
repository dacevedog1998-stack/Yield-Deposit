# Filling Optimisation Model — Static Three-Curve Version with Batch Usage

## Main updates

- The yellow result box behind the chart has been removed.
- A new input has been added: **Actual usable filling batch (%)**.
- Expected Units still compare against the original total batch at 100% target filling.
- Actual Units now use only the usable part of the batch.

## Core logic

### Expected Units

```text
Expected Units = Total Filling Batch / Target Filling
```

### Usable batch

```text
Usable Filling Batch = Total Filling Batch × Actual Usable Filling Batch (%)
```

### Actual Units

```text
Actual Units = Usable Filling Batch / Tested Filling Target
```

### Yield — blue line

```text
Yield = Actual Units / Expected Units × 100
```

Underweights are not subtracted from Yield.

### Good Units — green line

```text
Expected Seconds = Actual Units × Underweight Rate
Good Units = Actual Units - Expected Seconds
```

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```
