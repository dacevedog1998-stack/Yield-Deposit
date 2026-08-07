from __future__ import annotations

import numpy as np
import pandas as pd

SIMULATION_UNITS = 80_000
RANDOM_SEED = 42
MINIMUM_CURVE_RANGE_G = 15.0
CURVE_MARGIN_G = 5.0
MINIMUM_FILLING_TARGET_G = 0.5
TARGET_STEP_G = 0.5
MAXIMUM_CURVE_POINTS = 161


def variation_to_standard_deviation(
    average_weight: float,
    variation_value: float,
    variation_method: str,
) -> float:
    if variation_value < 0:
        raise ValueError(
            "Variation cannot be negative. Use the signed pastry or filling adjustment fields for values below target."
        )

    if variation_method == "Percentage (CV)":
        return average_weight * variation_value / 100

    if variation_method == "Standard deviation (g)":
        return variation_value

    raise ValueError("Unknown variation input method.")


def create_filling_targets(
    target_filling_weight: float,
    filling_adjustment: float,
    pastry_adjustment: float,
) -> np.ndarray:
    input_filling_target = target_filling_weight + filling_adjustment
    simple_compensation_target = target_filling_weight - pastry_adjustment

    minimum_target = min(
        target_filling_weight - MINIMUM_CURVE_RANGE_G,
        input_filling_target - CURVE_MARGIN_G,
        simple_compensation_target - CURVE_MARGIN_G,
    )
    maximum_target = max(
        target_filling_weight + MINIMUM_CURVE_RANGE_G,
        input_filling_target + CURVE_MARGIN_G,
        simple_compensation_target + CURVE_MARGIN_G,
    )
    minimum_target = max(MINIMUM_FILLING_TARGET_G, minimum_target)

    span = maximum_target - minimum_target
    step = max(TARGET_STEP_G, span / (MAXIMUM_CURVE_POINTS - 1))

    regular_targets = np.arange(minimum_target, maximum_target + step / 2, step)
    exact_targets = np.array(
        [
            minimum_target,
            maximum_target,
            target_filling_weight,
            input_filling_target,
            simple_compensation_target,
        ],
        dtype=float,
    )

    targets = np.concatenate([regular_targets, exact_targets])
    targets = np.array(sorted(set(np.round(targets, 4))), dtype=float)
    return targets[targets > 0]


def run_optimisation(
    target_pastry_weight: float,
    target_filling_weight: float,
    target_glaze_weight: float,
    filling_batch_kg: float,
    actual_batch_usage_percentage: float,
    permitted_reduction_percentage: float,
    maximum_acceptable_underweight: float,
    pastry_adjustment: float,
    filling_adjustment: float,
    variation_method: str,
    pastry_variation_value: float,
    filling_variation_value: float,
) -> dict:
    if target_pastry_weight <= 0:
        raise ValueError("Target pastry weight must be greater than zero.")
    if target_filling_weight <= 0:
        raise ValueError("Target filling weight must be greater than zero.")
    if target_glaze_weight < 0:
        raise ValueError("Target glaze weight cannot be negative.")
    if filling_batch_kg <= 0:
        raise ValueError("Filling batch size must be greater than zero.")
    if not 0 <= actual_batch_usage_percentage <= 100:
        raise ValueError("Actual batch usage percentage must be between 0% and 100%.")
    if not 0 <= permitted_reduction_percentage < 100:
        raise ValueError("Permitted reduction must be between 0% and less than 100%.")
    if not 0 <= maximum_acceptable_underweight <= 100:
        raise ValueError("Maximum acceptable underweight must be between 0% and 100%.")

    actual_pastry_average = target_pastry_weight + pastry_adjustment
    input_filling_target = target_filling_weight + filling_adjustment

    if actual_pastry_average <= 0:
        raise ValueError("Target pastry plus pastry adjustment must be greater than zero.")
    if input_filling_target <= 0:
        raise ValueError("Target filling plus filling adjustment must be greater than zero.")

    pastry_sd_g = variation_to_standard_deviation(
        average_weight=actual_pastry_average,
        variation_value=pastry_variation_value,
        variation_method=variation_method,
    )

    target_product_weight = target_pastry_weight + target_filling_weight + target_glaze_weight
    minimum_allowed_weight = target_product_weight * (1 - permitted_reduction_percentage / 100)

    total_filling_batch_g = filling_batch_kg * 1000
    usable_filling_batch_g = total_filling_batch_g * actual_batch_usage_percentage / 100
    expected_units = total_filling_batch_g / target_filling_weight

    rng = np.random.default_rng(RANDOM_SEED)
    pastry_z = rng.standard_normal(SIMULATION_UNITS)
    filling_z = rng.standard_normal(SIMULATION_UNITS)
    pastry_sample = actual_pastry_average + pastry_z * pastry_sd_g
    pastry_sample = np.clip(pastry_sample, a_min=0.01, a_max=None)

    filling_targets = create_filling_targets(
        target_filling_weight=target_filling_weight,
        filling_adjustment=filling_adjustment,
        pastry_adjustment=pastry_adjustment,
    )

    rows = []
    for tested_filling_target in filling_targets:
        filling_sd_g = variation_to_standard_deviation(
            average_weight=tested_filling_target,
            variation_value=filling_variation_value,
            variation_method=variation_method,
        )
        filling_sample = tested_filling_target + filling_z * filling_sd_g
        filling_sample = np.clip(filling_sample, a_min=0.01, a_max=None)
        final_weight = pastry_sample + filling_sample + target_glaze_weight
        underweight_percentage = float(np.mean(final_weight < minimum_allowed_weight) * 100)
        actual_units = usable_filling_batch_g / tested_filling_target
        yield_percentage = actual_units / expected_units * 100
        expected_seconds = actual_units * underweight_percentage / 100
        good_units = actual_units - expected_seconds

        rows.append(
            {
                "filling_target": tested_filling_target,
                "filling_adjustment": tested_filling_target - target_filling_weight,
                "expected_units": expected_units,
                "actual_units": actual_units,
                "yield_percentage": yield_percentage,
                "underweight_percentage": underweight_percentage,
                "expected_seconds": expected_seconds,
                "good_units": good_units,
                "average_final_weight": float(final_weight.mean()),
                "minimum_simulated_weight": float(final_weight.min()),
                "meets_underweight_limit": underweight_percentage <= maximum_acceptable_underweight + 1e-12,
            }
        )

    results_df = pd.DataFrame(rows)
    input_index = results_df["filling_target"].sub(input_filling_target).abs().idxmin()
    input_result = results_df.loc[input_index]

    compliant_results = results_df[results_df["meets_underweight_limit"]]
    if not compliant_results.empty:
        optimum_index = compliant_results["good_units"].idxmax()
        constraint_met = True
        recommendation_status = "Compliant optimum"
    else:
        optimum_index = results_df["good_units"].idxmax()
        constraint_met = False
        recommendation_status = "Best output inside the tested range"

    optimum_result = results_df.loc[optimum_index]

    if pastry_adjustment < 0:
        pastry_condition = f"{abs(pastry_adjustment):.2f} g lighter than target"
    elif pastry_adjustment > 0:
        pastry_condition = f"{pastry_adjustment:.2f} g heavier than target"
    else:
        pastry_condition = "At target"

    summary = {
        "target_pastry_weight": target_pastry_weight,
        "target_filling_weight": target_filling_weight,
        "target_glaze_weight": target_glaze_weight,
        "target_product_weight": target_product_weight,
        "minimum_allowed_weight": minimum_allowed_weight,
        "filling_batch_kg": filling_batch_kg,
        "total_filling_batch_g": total_filling_batch_g,
        "actual_batch_usage_percentage": actual_batch_usage_percentage,
        "usable_filling_batch_g": usable_filling_batch_g,
        "expected_units": expected_units,
        "pastry_adjustment": pastry_adjustment,
        "actual_pastry_average": actual_pastry_average,
        "filling_adjustment": filling_adjustment,
        "input_filling_target": input_filling_target,
        "pastry_condition": pastry_condition,
        "variation_method": variation_method,
        "pastry_variation_value": pastry_variation_value,
        "filling_variation_value": filling_variation_value,
        "pastry_sd_g": pastry_sd_g,
        "constraint_met": constraint_met,
        "recommendation_status": recommendation_status,
        "input_actual_units": float(input_result["actual_units"]),
        "input_yield": float(input_result["yield_percentage"]),
        "input_underweight": float(input_result["underweight_percentage"]),
        "input_seconds": float(input_result["expected_seconds"]),
        "input_good_units": float(input_result["good_units"]),
        "optimum_filling_target": float(optimum_result["filling_target"]),
        "optimum_filling_adjustment": float(optimum_result["filling_adjustment"]),
        "optimum_actual_units": float(optimum_result["actual_units"]),
        "optimum_yield": float(optimum_result["yield_percentage"]),
        "optimum_underweight": float(optimum_result["underweight_percentage"]),
        "optimum_seconds": float(optimum_result["expected_seconds"]),
        "optimum_good_units": float(optimum_result["good_units"]),
        "minimum_tested_filling": float(results_df["filling_target"].min()),
        "maximum_tested_filling": float(results_df["filling_target"].max()),
    }
    return {"results": results_df, "summary": summary}
