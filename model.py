import numpy as np
import pandas as pd


FILLING_RECOVERY_FACTOR = 0.98

SIMULATION_UNITS = 150_000
PASTRY_SAMPLE_SIZE = 30_000
RANDOM_SEED = 42

MAXIMUM_FILLING_REDUCTION_RATE = 0.07
FILLING_TARGET_STEP = 0.5

FILLING_STANDARD_DEVIATION_RATE = 0.01
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

    distance_to_minimum = (
        nominal_pastry_weight
        - minimum_pastry_weight
    )

    upper_pastry_weight = (
        nominal_pastry_weight
        + distance_to_minimum
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
    """
    Create filling targets below, at and above nominal.

    The exact minimum, nominal and maximum targets are always included.
    No target is allowed to exceed the selected maximum extra filling.
    """

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
    usable_filling_grams,
    nominal_filling_weight,
    maximum_acceptable_underweight,
):
    """Simulate one filling target."""

    rng = np.random.default_rng(RANDOM_SEED + 1)

    simulated_pastry = rng.choice(
        pastry_sample,
        size=SIMULATION_UNITS,
        replace=True,
    )

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

    average_simulated_filling = (
        simulated_filling.mean()
    )

    produced_units = int(
        usable_filling_grams
        / average_simulated_filling
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

    theoretical_filling_yield = (
        nominal_filling_weight
        / filling_target
        * 100
    )

    good_product_rate = (
        1
        - underweight_percentage
        / 100
    )

    expected_production_yield = (
        FILLING_RECOVERY_FACTOR
        * (
            nominal_filling_weight
            / filling_target
        )
        * good_product_rate
        * 100
    )

    return {
        "filling_target": filling_target,
        "filling_adjustment": (
            filling_target
            - nominal_filling_weight
        ),
        "theoretical_filling_yield": (
            theoretical_filling_yield
        ),
        "yield_percentage": (
            expected_production_yield
        ),
        "produced_units": produced_units,
        "underweight_percentage": (
            underweight_percentage
        ),
        "expected_seconds": expected_seconds,
        "good_units": good_units,
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
):
    """Run the filling optimisation model."""

    if filling_batch_kg <= 0:
        raise ValueError(
            "Filling batch size must be greater than zero."
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

    usable_filling_grams = (
        filling_batch_kg
        * 1000
        * FILLING_RECOVERY_FACTOR
    )

    filling_standard_deviation = max(
        nominal_filling_weight
        * FILLING_STANDARD_DEVIATION_RATE,
        0.01,
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
            usable_filling_grams=usable_filling_grams,
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
        "nominal_filling_weight": (
            nominal_filling_weight
        ),
        "nominal_product_weight": (
            nominal_product_weight
        ),
        "minimum_allowed_weight": (
            minimum_allowed_weight
        ),
        "filling_batch_kg": filling_batch_kg,
        "minimum_pastry_weight": (
            minimum_pastry_weight
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
        "optimal_theoretical_filling_yield": float(
            optimal_result[
                "theoretical_filling_yield"
            ]
        ),
        "optimal_yield": float(
            optimal_result["yield_percentage"]
        ),
        "optimal_underweight": float(
            optimal_result[
                "underweight_percentage"
            ]
        ),
        "optimal_good_units": float(
            optimal_result["good_units"]
        ),
    }

    return {
        "results": results_df,
        "summary": summary,
    }
