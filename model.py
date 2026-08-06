from __future__ import annotations

import numpy as np
import pandas as pd


SIMULATION_UNITS = 120_000
RANDOM_SEED = 42

MINIMUM_CURVE_RANGE_G = 15.0
CURVE_MARGIN_G = 5.0
MAXIMUM_CURVE_POINTS = 241


def variation_to_sd(
    average_weight: float,
    variation_value: float,
    variation_method: str,
) -> float:
    """
    Convert the selected variation input into standard deviation in grams.

    Percentage (CV):
        SD = average × CV / 100

    Standard deviation (g):
        The entered value is already the SD in grams.
    """

    if variation_value < 0:
        raise ValueError(
            "Variation cannot be negative. Use the signed pastry or filling "
            "adjustment fields to represent weights below target."
        )

    if variation_method == "Percentage (CV)":
        return average_weight * variation_value / 100

    if variation_method == "Standard deviation (g)":
        return variation_value

    raise ValueError("Unknown variation input method.")


def create_filling_targets(
    target_filling_weight: float,
    actual_filling_adjustment: float,
    pastry_adjustment: float,
) -> np.ndarray:
    """
    Create a full filling-target curve.

    The curve always includes:
    - target filling;
    - actual filling;
    - the simple pastry-compensation point;
    - at least target filling ±15 g.

    The range expands automatically for unusual or extreme scenarios.
    """

    actual_filling_target = (
        target_filling_weight
        + actual_filling_adjustment
    )

    simple_compensation_target = (
        target_filling_weight
        - pastry_adjustment
    )

    minimum_target = min(
        target_filling_weight - MINIMUM_CURVE_RANGE_G,
        actual_filling_target - CURVE_MARGIN_G,
        simple_compensation_target - CURVE_MARGIN_G,
    )

    maximum_target = max(
        target_filling_weight + MINIMUM_CURVE_RANGE_G,
        actual_filling_target + CURVE_MARGIN_G,
        simple_compensation_target + CURVE_MARGIN_G,
    )

    minimum_target = max(0.5, minimum_target)

    span = maximum_target - minimum_target
    step = max(0.5, span / (MAXIMUM_CURVE_POINTS - 1))

    regular_targets = np.arange(
        minimum_target,
        maximum_target + step / 2,
        step,
    )

    exact_targets = np.array(
        [
            minimum_target,
            maximum_target,
            target_filling_weight,
            actual_filling_target,
            simple_compensation_target,
        ],
        dtype=float,
    )

    targets = np.concatenate(
        [regular_targets, exact_targets]
    )

    targets = np.array(
        sorted(set(np.round(targets, 4))),
        dtype=float,
    )

    return targets[targets > 0]


def run_optimisation(
    target_pastry_weight: float,
    target_filling_weight: float,
    target_glaze_weight: float,
    filling_batch_kg: float,
    permitted_reduction_percentage: float,
    maximum_acceptable_underweight: float,
    pastry_adjustment: float,
    actual_filling_adjustment: float,
    variation_method: str,
    pastry_variation_value: float,
    filling_variation_value: float,
) -> dict:
    """
    Evaluate production yield over a complete filling-target curve.

    Expected Units remain fixed:
        batch / target filling

    Actual Units vary:
        batch / tested filling

    Good Units:
        actual units × (1 - underweight rate)

    Production Yield:
        good units / expected units × 100
    """

    if target_pastry_weight <= 0:
        raise ValueError(
            "Target pastry weight must be greater than zero."
        )

    if target_filling_weight <= 0:
        raise ValueError(
            "Target filling weight must be greater than zero."
        )

    if target_glaze_weight < 0:
        raise ValueError(
            "Target glaze weight cannot be negative."
        )

    if filling_batch_kg <= 0:
        raise ValueError(
            "Filling batch size must be greater than zero."
        )

    if not 0 <= permitted_reduction_percentage < 100:
        raise ValueError(
            "Permitted reduction must be between 0% and less than 100%."
        )

    if not 0 <= maximum_acceptable_underweight <= 100:
        raise ValueError(
            "Maximum acceptable underweight must be between 0% and 100%."
        )

    actual_pastry_average = (
        target_pastry_weight
        + pastry_adjustment
    )

    actual_filling_target = (
        target_filling_weight
        + actual_filling_adjustment
    )

    if actual_pastry_average <= 0:
        raise ValueError(
            "Target pastry plus pastry adjustment must be greater than zero."
        )

    if actual_filling_target <= 0:
        raise ValueError(
            "Target filling plus filling adjustment must be greater than zero."
        )

    pastry_sd_g = variation_to_sd(
        average_weight=actual_pastry_average,
        variation_value=pastry_variation_value,
        variation_method=variation_method,
    )

    target_product_weight = (
        target_pastry_weight
        + target_filling_weight
        + target_glaze_weight
    )

    minimum_allowed_weight = (
        target_product_weight
        * (
            1
            - permitted_reduction_percentage / 100
        )
    )

    filling_batch_g = filling_batch_kg * 1000

    expected_units = (
        filling_batch_g
        / target_filling_weight
    )

    rng = np.random.default_rng(RANDOM_SEED)

    pastry_z = rng.standard_normal(
        SIMULATION_UNITS
    )

    filling_z = rng.standard_normal(
        SIMULATION_UNITS
    )

    pastry_sample = (
        actual_pastry_average
        + pastry_z * pastry_sd_g
    )

    pastry_sample = np.clip(
        pastry_sample,
        a_min=0.01,
        a_max=None,
    )

    filling_targets = create_filling_targets(
        target_filling_weight=target_filling_weight,
        actual_filling_adjustment=actual_filling_adjustment,
        pastry_adjustment=pastry_adjustment,
    )

    rows: list[dict] = []

    for tested_filling_target in filling_targets:
        filling_sd_g = variation_to_sd(
            average_weight=tested_filling_target,
            variation_value=filling_variation_value,
            variation_method=variation_method,
        )

        filling_sample = (
            tested_filling_target
            + filling_z * filling_sd_g
        )

        filling_sample = np.clip(
            filling_sample,
            a_min=0.01,
            a_max=None,
        )

        final_weight = (
            pastry_sample
            + filling_sample
            + target_glaze_weight
        )

        underweight_percentage = float(
            np.clip(
                np.mean(
                    final_weight
                    < minimum_allowed_weight
                )
                * 100,
                0.0,
                100.0,
            )
        )

        actual_units = (
            filling_batch_g
            / tested_filling_target
        )

        expected_seconds = (
            actual_units
            * underweight_percentage
            / 100
        )

        good_units = max(
            0.0,
            actual_units
            - expected_seconds,
        )

        production_yield = (
            good_units
            / expected_units
            * 100
        )

        theoretical_filling_yield = (
            actual_units
            / expected_units
            * 100
        )

        rows.append(
            {
                "filling_target": tested_filling_target,
                "filling_adjustment": (
                    tested_filling_target
                    - target_filling_weight
                ),
                "expected_units": expected_units,
                "actual_units": actual_units,
                "underweight_percentage": (
                    underweight_percentage
                ),
                "expected_seconds": expected_seconds,
                "good_units": good_units,
                "production_yield": production_yield,
                "theoretical_filling_yield": (
                    theoretical_filling_yield
                ),
                "average_final_weight": float(
                    final_weight.mean()
                ),
                "minimum_simulated_weight": float(
                    final_weight.min()
                ),
                "meets_underweight_limit": (
                    underweight_percentage
                    <= maximum_acceptable_underweight
                    + 1e-12
                ),
            }
        )

    results_df = pd.DataFrame(rows)

    actual_index = (
        results_df["filling_target"]
        .sub(actual_filling_target)
        .abs()
        .idxmin()
    )

    actual_result = results_df.loc[
        actual_index
    ]

    compliant_results = results_df[
        results_df["meets_underweight_limit"]
    ]

    if not compliant_results.empty:
        recommended_index = (
            compliant_results["good_units"].idxmax()
        )
        constraint_met = True
        recommendation_status = (
            "Compliant optimum"
        )
    else:
        recommended_index = (
            results_df["good_units"].idxmax()
        )
        constraint_met = False
        recommendation_status = (
            "Best output inside the tested range"
        )

    recommended_result = results_df.loc[
        recommended_index
    ]

    if pastry_adjustment < 0:
        pastry_condition = (
            f"{abs(pastry_adjustment):.2f} g lighter than target"
        )
    elif pastry_adjustment > 0:
        pastry_condition = (
            f"{pastry_adjustment:.2f} g heavier than target"
        )
    else:
        pastry_condition = "At target"

    summary = {
        "target_pastry_weight": target_pastry_weight,
        "target_filling_weight": target_filling_weight,
        "target_glaze_weight": target_glaze_weight,
        "target_product_weight": target_product_weight,
        "minimum_allowed_weight": minimum_allowed_weight,
        "filling_batch_kg": filling_batch_kg,
        "expected_units": expected_units,
        "pastry_adjustment": pastry_adjustment,
        "actual_pastry_average": actual_pastry_average,
        "actual_filling_adjustment": (
            actual_filling_adjustment
        ),
        "actual_filling_target": actual_filling_target,
        "pastry_condition": pastry_condition,
        "variation_method": variation_method,
        "pastry_variation_value": pastry_variation_value,
        "filling_variation_value": filling_variation_value,
        "pastry_sd_g": pastry_sd_g,
        "constraint_met": constraint_met,
        "recommendation_status": recommendation_status,
        "actual_units": float(
            actual_result["actual_units"]
        ),
        "actual_underweight": float(
            actual_result["underweight_percentage"]
        ),
        "actual_seconds": float(
            actual_result["expected_seconds"]
        ),
        "actual_good_units": float(
            actual_result["good_units"]
        ),
        "actual_production_yield": float(
            actual_result["production_yield"]
        ),
        "actual_theoretical_filling_yield": float(
            actual_result["theoretical_filling_yield"]
        ),
        "recommended_filling_target": float(
            recommended_result["filling_target"]
        ),
        "recommended_filling_adjustment": float(
            recommended_result["filling_adjustment"]
        ),
        "recommended_actual_units": float(
            recommended_result["actual_units"]
        ),
        "recommended_underweight": float(
            recommended_result["underweight_percentage"]
        ),
        "recommended_seconds": float(
            recommended_result["expected_seconds"]
        ),
        "recommended_good_units": float(
            recommended_result["good_units"]
        ),
        "recommended_production_yield": float(
            recommended_result["production_yield"]
        ),
        "minimum_tested_filling": float(
            results_df["filling_target"].min()
        ),
        "maximum_tested_filling": float(
            results_df["filling_target"].max()
        ),
    }

    return {
        "results": results_df,
        "summary": summary,
    }
