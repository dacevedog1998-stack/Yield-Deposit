import numpy as np
import pandas as pd


SIMULATION_UNITS = 150_000
PASTRY_SAMPLE_SIZE = 30_000
RANDOM_SEED = 42

MAXIMUM_FILLING_REDUCTION_RATE = 0.07
FILLING_TARGET_STEP = 0.5

DEFAULT_FILLING_VARIATION_PERCENTAGE = 0.0
GLAZE_STANDARD_DEVIATION_RATE = 0.08

PASTRY_BETA_A = 2.5
PASTRY_BETA_B = 3.5
PASTRY_UPPER_ALLOWANCE_RATE = 0.40


def generate_pastry_sample(
    nominal_pastry_weight,
    minimum_pastry_weight,
):
    """Generate pastry weights mildly biased toward the low limit."""

    if minimum_pastry_weight > nominal_pastry_weight:
        raise ValueError(
            "Minimum pastry weight cannot be greater than "
            "nominal pastry weight."
        )

    if minimum_pastry_weight == nominal_pastry_weight:
        return np.full(
            PASTRY_SAMPLE_SIZE,
            nominal_pastry_weight,
        )

    pastry_range = (
        nominal_pastry_weight
        - minimum_pastry_weight
    )

    upper_pastry_weight = (
        nominal_pastry_weight
        + pastry_range
        * PASTRY_UPPER_ALLOWANCE_RATE
    )

    rng = np.random.default_rng(RANDOM_SEED)

    beta_values = rng.beta(
        PASTRY_BETA_A,
        PASTRY_BETA_B,
        size=PASTRY_SAMPLE_SIZE,
    )

    return (
        minimum_pastry_weight
        + beta_values
        * (
            upper_pastry_weight
            - minimum_pastry_weight
        )
    )


def create_filling_targets(
    nominal_filling_weight,
    maximum_extra_filling,
):
    """Create filling targets below, at and above nominal filling."""

    minimum_target = (
        nominal_filling_weight
        * (
            1
            - MAXIMUM_FILLING_REDUCTION_RATE
        )
    )

    maximum_target = (
        nominal_filling_weight
        + maximum_extra_filling
    )

    regular_targets = np.arange(
        minimum_target,
        maximum_target + FILLING_TARGET_STEP,
        FILLING_TARGET_STEP,
    )

    regular_targets = regular_targets[
        (
            regular_targets
            >= minimum_target - 1e-9
        )
        & (
            regular_targets
            <= maximum_target + 1e-9
        )
    ]

    all_targets = np.concatenate(
        [
            regular_targets,
            np.array(
                [
                    minimum_target,
                    nominal_filling_weight,
                    maximum_target,
                ]
            ),
        ]
    )

    return np.array(
        sorted(
            set(
                np.round(all_targets, 4)
            ),
            reverse=True,
        )
    )


def evaluate_filling_target(
    filling_target,
    pastry_sample,
    nominal_glaze_weight,
    filling_standard_deviation,
    glaze_standard_deviation,
    minimum_allowed_weight,
    filling_batch_grams,
    nominal_filling_weight,
    maximum_acceptable_underweight,
):
    """Evaluate one filling target."""

    rng = np.random.default_rng(RANDOM_SEED + 1)

    simulated_pastry = rng.choice(
        pastry_sample,
        size=SIMULATION_UNITS,
        replace=True,
    )

    if filling_standard_deviation == 0:
        simulated_filling = np.full(
            SIMULATION_UNITS,
            filling_target,
        )
    else:
        simulated_filling = rng.normal(
            loc=filling_target,
            scale=filling_standard_deviation,
            size=SIMULATION_UNITS,
        )

    if nominal_glaze_weight == 0:
        simulated_glaze = np.zeros(
            SIMULATION_UNITS
        )
    else:
        simulated_glaze = rng.normal(
            loc=nominal_glaze_weight,
            scale=glaze_standard_deviation,
            size=SIMULATION_UNITS,
        )

    final_weight = (
        simulated_pastry
        + simulated_filling
        + simulated_glaze
    )

    underweight_percentage = (
        np.mean(
            final_weight
            < minimum_allowed_weight
        )
        * 100
    )

    average_filling_used = float(
        simulated_filling.mean()
    )

    produced_units = (
        filling_batch_grams
        / average_filling_used
    )

    nominal_units = (
        filling_batch_grams
        / nominal_filling_weight
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

    return {
        "filling_target": filling_target,
        "filling_adjustment": (
            filling_target
            - nominal_filling_weight
        ),
        "yield_percentage": filling_yield_percentage,
        "nominal_units": nominal_units,
        "produced_units": produced_units,
        "underweight_percentage": underweight_percentage,
        "expected_seconds": expected_seconds,
        "good_units": good_units,
        "good_output_rate": (
            100
            - underweight_percentage
        ),
        "average_final_weight": float(
            final_weight.mean()
        ),
        "meets_underweight_limit": (
            underweight_percentage
            <= maximum_acceptable_underweight
            + 1e-12
        ),
    }


def run_optimisation(
    nominal_pastry_weight,
    minimum_pastry_weight,
    nominal_filling_weight,
    nominal_glaze_weight,
    filling_batch_kg,
    permitted_reduction_percentage,
    maximum_extra_filling,
    maximum_acceptable_underweight,
    filling_variation_percentage=(
        DEFAULT_FILLING_VARIATION_PERCENTAGE
    ),
):
    """Run the filling optimisation model."""

    if filling_batch_kg <= 0:
        raise ValueError(
            "Filling batch size must be greater than zero."
        )

    if filling_variation_percentage < 0:
        raise ValueError(
            "Filling variation percentage cannot be negative."
        )

    pastry_sample = generate_pastry_sample(
        nominal_pastry_weight=nominal_pastry_weight,
        minimum_pastry_weight=minimum_pastry_weight,
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

    filling_standard_deviation = (
        nominal_filling_weight
        * filling_variation_percentage
        / 100
    )

    glaze_standard_deviation = max(
        nominal_glaze_weight
        * GLAZE_STANDARD_DEVIATION_RATE,
        0.01,
    )

    filling_targets = create_filling_targets(
        nominal_filling_weight=nominal_filling_weight,
        maximum_extra_filling=maximum_extra_filling,
    )

    results = [
        evaluate_filling_target(
            filling_target=target,
            pastry_sample=pastry_sample,
            nominal_glaze_weight=nominal_glaze_weight,
            filling_standard_deviation=(
                filling_standard_deviation
            ),
            glaze_standard_deviation=(
                glaze_standard_deviation
            ),
            minimum_allowed_weight=minimum_allowed_weight,
            filling_batch_grams=filling_batch_grams,
            nominal_filling_weight=nominal_filling_weight,
            maximum_acceptable_underweight=(
                maximum_acceptable_underweight
            ),
        )
        for target in filling_targets
    ]

    results_df = pd.DataFrame(results)

    valid_results = results_df[
        results_df["meets_underweight_limit"]
    ]

    if not valid_results.empty:
        optimal_index = (
            valid_results["good_units"].idxmax()
        )
        constraint_met = True
        result_status = "Compliant recommendation"
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

    summary = {
        "nominal_filling_weight": nominal_filling_weight,
        "nominal_product_weight": nominal_product_weight,
        "minimum_allowed_weight": minimum_allowed_weight,
        "filling_batch_kg": filling_batch_kg,
        "minimum_pastry_weight": minimum_pastry_weight,
        "simulated_pastry_minimum": float(
            pastry_sample.min()
        ),
        "simulated_pastry_average": float(
            pastry_sample.mean()
        ),
        "simulated_pastry_maximum": float(
            pastry_sample.max()
        ),
        "average_pastry_deficit": max(
            0.0,
            nominal_pastry_weight
            - float(pastry_sample.mean())
        ),
        "direct_minimum_pastry_deficit": max(
            0.0,
            nominal_pastry_weight
            - minimum_pastry_weight
        ),
        "maximum_acceptable_underweight": (
            maximum_acceptable_underweight
        ),
        "maximum_tested_filling": float(
            results_df["filling_target"].max()
        ),
        "constraint_met": constraint_met,
        "result_status": result_status,
        "optimal_filling": float(
            optimal_result["filling_target"]
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
            optimal_result["underweight_percentage"]
        ),
        "optimal_good_units": float(
            optimal_result["good_units"]
        ),
        "filling_variation_percentage": (
            filling_variation_percentage
        ),
    }

    return {
        "results": results_df,
        "summary": summary,
    }
