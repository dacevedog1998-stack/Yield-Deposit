# Filling Optimisation Model — Corrected Yield

This complete Streamlit project evaluates filling targets below, at and above
nominal.

## Main correction

The blue curve now displays **Expected Production Yield**:

```text
98% recovery
× nominal filling / tested filling
× good-product rate
```

The scenario table also shows **Filling Yield** separately.

## Other corrections

- The exact maximum extra filling is included and never exceeded.
- If the underweight constraint is not met, the output is labelled
  **Best available within the tested range**, not a compliant recommendation.
- The yield percentage is shown above the selected point.
- Full instructions are stored in `instructions.py`.

## Files

- `app.py`
- `model.py`
- `charts.py`
- `instructions.py`
- `requirements.txt`
- `README.md`
- `.streamlit/config.toml`

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```


## Interactive chart

The chart now uses Plotly and supports:

- Mouse-wheel zoom
- Drag-to-zoom
- Zoom-in and zoom-out toolbar buttons
- Pan
- Autoscale
- Reset axes
- Hover values

The regular curve markers have been reduced to 5–6 pixels to improve clarity.
