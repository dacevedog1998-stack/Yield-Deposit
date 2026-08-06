from __future__ import annotations

import numpy as np
import pandas as pd


SIMULATION_UNITS = 150_000
RANDOM_SEED = 42
DEFAULT_TARGET_STEP_G = 0.5


def generate_weight_sample(
    average_weight: float,
    variation_percentage: float,
    seed: int,
) -> np.ndarray:
    """
    Generate a normally distributed weight sample.

    variation_percentage is treated as the coefficient of variation:

        standard deviation / average × 100

    A value of 0% treats the weight as exact.
    """

    if average_weight < 0:
        raise ValueError("Average weight cannot be negative.")

    if variation_percentage < 0:
        raise ValueError("Variation percentage cannot be negative.")

    if variation_percentage == 0 or average_weight == 0:
        return np.full(
            SIMULATION_UNITS,
            average_weight,
            dtype=float,
        )

    standard_deviation = (
        average_weight
        * variation_percentage
        / 100
    )

    rng = np.random.default_rng(seed)

    sample = rng.normal(
        loc=average_weight,
        scale=standard_deviation,
        size=SIMULATION_UNITS,
    )

    return np.clip(
        sample,
        a_min=0.0,
        a_max=None,
    )


def create_filling_targets(
    nominal_filling_weight: float,
    maximum_filling_reduction: float,
    maximum_extra_filling: float,
    target_step_g: float = DEFAULT_TARGET_STEP_G,
) -> np.ndarray:
    """
    Create filling targets below, at and above nominal.

    A lower target is useful when current pastry is heavier than nominal.
    A higher target is useful when current pastry is lighter than nominal.
    """

    if nominal_filling_weight <= 0:
        raise ValueError(
            "Nominal filling weight must be greater than zero."
        )

    if maximum_filling_reduction < 0:
        raise ValueError(
            "Maximum filling reduction cannot be negative."
        )

    if maximum_extra_filling < 0:
        raise ValueError(
            "Maximum extra filling cannot be negative."
        )

    if target_step_g <= 0:
        raise ValueError(
            "Target step must be greater than zero."
        )

    minimum_target = max(
        0.01,
        nominal_filling_weight
        - maximum_filling_reduction,
    )

    maximum_target = (
        nominal_filling_weight
        + maximum_extra_filling
    )

    regular_targets = np.arange(
        minimum_target,
        maximum_target + target_step_g / 2,
        target_step_g,
    )

    exact_targets = np.array(
        [
            minimum_target,
            nominal_filling_weight,
            maximum_target,
        ],
        dtype=float,
    )

    all_targets = np.concatenate(
        [
            regular_targets,
            exact_targets,
        ]
    )

    return np.array(
        sorted(
            set(
                np.round(
                    all_targets,
                    4,
                )
            )
        ),
        dtype=float,
    )


def evaluate_filling_target(
    filling_target: float,
    pastry_sample: np.ndarray,
    glaze_sample: np.ndarray,
    filling_variation_percentage: float,
    minimum_allowed_weight: float,
    filling_batch_grams: float,
    nominal_filling_weight: float,
    maximum_acceptable_underweight: float,
) -> dict:
    """
    Evaluate one filling target.

    Filling yield is based only on the filling target:

        produced units / nominal units × 100

    Underweight is calculated separately from final product weight.
    """

    filling_sample = generate_weight_sample(
        average_weight=filling_target,
        variation_percentage=filling_variation_percentage,
        seed=RANDOM_SEED + 2,
    )

    final_weight = (
        pastry_sample
        + filling_sample
        + glaze_sample
    )

    underweight_percentage = float(
        np.mean(
            final_weight
            < minimum_allowed_weight
        )
        * 100
    )

    nominal_units = (
        filling_batch_grams
        / nominal_filling_weight
    )

    produced_units = (
        filling_batch_grams
        / filling_target
    )

    filling_yield_percentage = (
        produced_units
        / nominal_units
        * 100
    )

    expected_seconds = (
        produced_units
        * underweight_percentage
        / 100
    )

    good_units = (
        produced_units
        - expected_seconds
    )

    average_final_weight = float(
        final_weight.mean()
    )

    minimum_simulated_weight = float(
        final_weight.min()
    )

    return {
        "filling_target": filling_target,
        "filling_adjustment": (
            filling_target
            - nominal_filling_weight
        ),
        "yield_percentage": (
            filling_yield_percentage
        ),
        "nominal_units": nominal_units,
        "produced_units": produced_units,
        "underweight_percentage": (
            underweight_percentage
        ),
        "expected_seconds": expected_seconds,
        "good_units": good_units,
        "good_output_rate": (
            100
            - underweight_percentage
        ),
        "average_final_weight": (
            average_final_weight
        ),
        "minimum_simulated_weight": (
            minimum_simulated_weight
        ),
        "average_weight_buffer": (
            average_final_weight
            - minimum_allowed_weight
        ),
        "meets_underweight_limit": (
            underweight_percentage
            <= maximum_acceptable_underweight
            + 1e-12
        ),
    }


def run_optimisation(
    nominal_pastry_weight: float,
    current_pastry_weight: float,
    nominal_filling_weight: float,
    nominal_glaze_weight: float,
    filling_batch_kg: float,
    permitted_reduction_percentage: float,
    maximum_filling_reduction: float,
    maximum_extra_filling: float,
    maximum_acceptable_underweight: float,
    pastry_variation_percentage: float = 0.0,
    filling_variation_percentage: float = 0.0,
    glaze_variation_percentage: float = 0.0,
    target_step_g: float = DEFAULT_TARGET_STEP_G,
) -> dict:
    """Run the complete filling optimisation model."""

    if nominal_pastry_weight <= 0:
        raise ValueError(
            "Nominal pastry weight must be greater than zero."
        )

    if current_pastry_weight <= 0:
        raise ValueError(
            "Current pastry average weight must be greater than zero."
        )

    if nominal_filling_weight <= 0:
        raise ValueError(
            "Nominal filling weight must be greater than zero."
        )

    if nominal_glaze_weight < 0:
        raise ValueError(
            "Nominal glaze weight cannot be negative."
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

    pastry_sample = generate_weight_sample(
        average_weight=current_pastry_weight,
        variation_percentage=(
            pastry_variation_percentage
        ),
        seed=RANDOM_SEED,
    )

    glaze_sample = generate_weight_sample(
        average_weight=nominal_glaze_weight,
        variation_percentage=(
            glaze_variation_percentage
        ),
        seed=RANDOM_SEED + 1,
    )

    nominal_product_weight = (
        nominal_pastry_weight
        + nominal_filling_weight
        + nominal_glaze_weight
    )

    minimum_allowed_weight = (
        nominal_product_weight
        * (
            1
            - permitted_reduction_percentage
            / 100
        )
    )

    filling_batch_grams = (
        filling_batch_kg
        * 1000
    )

    filling_targets = create_filling_targets(
        nominal_filling_weight=(
            nominal_filling_weight
        ),
        maximum_filling_reduction=(
            maximum_filling_reduction
        ),
        maximum_extra_filling=(
            maximum_extra_filling
        ),
        target_step_g=target_step_g,
    )

    results = [
        evaluate_filling_target(
            filling_target=target,
            pastry_sample=pastry_sample,
            glaze_sample=glaze_sample,
            filling_variation_percentage=(
                filling_variation_percentage
            ),
            minimum_allowed_weight=(
                minimum_allowed_weight
            ),
            filling_batch_grams=(
                filling_batch_grams
            ),
            nominal_filling_weight=(
                nominal_filling_weight
            ),
            maximum_acceptable_underweight=(
                maximum_acceptable_underweight
            ),
        )
        for target in filling_targets
    ]

    results_df = pd.DataFrame(results)

    compliant_results = results_df[
        results_df["meets_underweight_limit"]
    ]

    if not compliant_results.empty:
        optimal_index = (
            compliant_results["good_units"].idxmax()
        )

        constraint_met = True
        result_status = (
            "Compliant recommendation"
        )

    else:
        minimum_underweight = (
            results_df["underweight_percentage"].min()
        )

        lowest_risk_results = results_df[
            np.isclose(
                results_df["underweight_percentage"],
                minimum_underweight,
            )
        ]

        optimal_index = (
            lowest_risk_results["good_units"].idxmax()
        )

        constraint_met = False
        result_status = (
            "Best available within the tested range"
        )

    optimal_result = results_df.loc[
        optimal_index
    ]

    pastry_difference = (
        current_pastry_weight
        - nominal_pastry_weight
    )

    if pastry_difference < -1e-9:
        pastry_condition = (
            "Lighter than nominal"
        )

        suggested_direction = (
            "Test extra filling"
        )

        suggested_starting_adjustment = abs(
            pastry_difference
        )

        condition_message = (
            "Current pastry is lighter than nominal. "
            "Extra filling may be required to replace "
            "the missing pastry weight."
        )

    elif pastry_difference > 1e-9:
        pastry_condition = (
            "Heavier than nominal"
        )

        suggested_direction = (
            "Test a filling reduction"
        )

        suggested_starting_adjustment = (
            pastry_difference
        )

        condition_message = (
            "Current pastry is heavier than nominal. "
            "A lower filling target may still keep the "
            "finished product within specification."
        )

    else:
        pastry_condition = "At nominal"

        suggested_direction = (
            "Start at nominal filling"
        )

        suggested_starting_adjustment = 0.0

        condition_message = (
            "Current pastry matches the nominal pastry weight."
        )

    summary = {
        "nominal_pastry_weight": (
            nominal_pastry_weight
        ),
        "current_pastry_weight": (
            current_pastry_weight
        ),
        "pastry_difference": (
            pastry_difference
        ),
        "pastry_condition": (
            pastry_condition
        ),
        "suggested_direction": (
            suggested_direction
        ),
        "suggested_starting_adjustment": (
            suggested_starting_adjustment
        ),
        "condition_message": (
            condition_message
        ),
        "nominal_filling_weight": (
            nominal_filling_weight
        ),
        "nominal_glaze_weight": (
            nominal_glaze_weight
        ),
        "nominal_product_weight": (
            nominal_product_weight
        ),
        "minimum_allowed_weight": (
            minimum_allowed_weight
        ),
        "filling_batch_kg": (
            filling_batch_kg
        ),
        "simulated_pastry_minimum": float(
            pastry_sample.min()
        ),
        "simulated_pastry_average": float(
            pastry_sample.mean()
        ),
        "simulated_pastry_maximum": float(
            pastry_sample.max()
        ),
        "pastry_variation_percentage": (
            pastry_variation_percentage
        ),
        "filling_variation_percentage": (
            filling_variation_percentage
        ),
        "glaze_variation_percentage": (
            glaze_variation_percentage
        ),
        "maximum_filling_reduction": (
            maximum_filling_reduction
        ),
        "maximum_extra_filling": (
            maximum_extra_filling
        ),
        "maximum_acceptable_underweight": (
            maximum_acceptable_underweight
        ),
        "minimum_tested_filling": float(
            results_df["filling_target"].min()
        ),
        "maximum_tested_filling": float(
            results_df["filling_target"].max()
        ),
        "constraint_met": (
            constraint_met
        ),
        "result_status": (
            result_status
        ),
        "optimal_filling": float(
            optimal_result["filling_target"]
        ),
        "optimal_filling_adjustment": float(
            optimal_result["filling_adjustment"]
        ),
        "optimal_yield": float(
            optimal_result["yield_percentage"]
        ),
        "optimal_nominal_units": float(
            optimal_result["nominal_units"]
        ),
        "optimal_produced_units": float(
            optimal_result["produced_units"]
        ),
        "optimal_underweight": float(
            optimal_result[
                "underweight_percentage"
            ]
        ),
        "optimal_seconds": float(
            optimal_result["expected_seconds"]
        ),
        "optimal_good_units": float(
            optimal_result["good_units"]
        ),
        "optimal_average_final_weight": float(
            optimal_result[
                "average_final_weight"
            ]
        ),
        "optimal_average_weight_buffer": float(
            optimal_result[
                "average_weight_buffer"
            ]
        ),
    }

    return {
        "results": results_df,
        "summary": summary,
    }
