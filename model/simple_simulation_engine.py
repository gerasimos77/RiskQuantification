import os
import numpy as np
from scipy import stats as st
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler and set level to info
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter and add it to the handler
formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

def define_unique_risk_factors(df_with_risk_factors: pd.DataFrame, risk_id_column: str = 'Risk'):
    """Extracts & Returns the unique IDs of risk factors."""

    return df_with_risk_factors[risk_id_column].values.tolist()

def sample_risk_impact(steps: int = 5, scenarios: int = 1000, distribution: str = 'Normal',
                       mean: float = 0.0, std: float = 1.0, mode: float = 0, median: float = 0,
                       left_tail_impact: float = 0.0, right_tail_impact: float = 1.0, risk_likelihood: float = 0.05,
                       min_impact: float = 0.0, max_impact: float = 1.0,
                       cap_impact_per_risk: bool = True, cap_value: float = 400000000.00,
                       seed: int = 110, independent_risk_sampling: bool = True, risk_id: int = 0):
    """Samples the impact of a certain risk from a given distribution (in case risk materialises)."""
    # Initialize a DataFrame to store results of the simulation
    df_rv_sim = pd.DataFrame(columns=range(scenarios))
    df_risk_realization_map = pd.DataFrame(columns=range(scenarios))

    # per risk factor; each row is a step and each column a scenario-simulation
    for i in range(0, steps):
        # Set a random seed to replicate identical results
        np.random.seed(seed=seed + risk_id + i)

        # Initialize an empty series for sample per step
        data = pd.Series()

        # Define whether risk materializes from a Bernoulli distribution with prob.of success equal to risk likelihood
        sample = np.random.binomial(n=1, p=risk_likelihood, size=scenarios)

        if distribution.lower() == "normal":
            data = np.random.normal(loc=mean, scale=std, size=scenarios)

            if independent_risk_sampling:
                data = data * sample

            # Cap impact value to the pre-defined maximum value (optional)
            if cap_impact_per_risk:
                data = np.minimum(data, cap_value)

        elif distribution.lower() == "lognormal":
            estimated_mean = (np.log(left_tail_impact) + np.log(right_tail_impact)) / 2
            estimated_sigma = (np.log(right_tail_impact) - np.log(left_tail_impact)) / 3.29

            data = np.random.lognormal(mean=estimated_mean, sigma=estimated_sigma, size=scenarios)

            if independent_risk_sampling:
                data = data * sample

            # Cap impact value to the pre-defined maximum value (optional)
            if cap_impact_per_risk:
                data = np.minimum(data, cap_value)

        elif distribution.lower() == "uniform":
            data = np.random.uniform(low=min_impact, high=max_impact, size=scenarios)

            if independent_risk_sampling:
                data = data * sample

            # Cap impact value to the pre-defined maximum value (optional)
            if cap_impact_per_risk:
                data = np.minimum(data, cap_value)

        elif distribution == "Deterministic Trend":
            data = [mean * i] * scenarios

        df_rv_sim.loc[len(df_rv_sim)] = data
        df_risk_realization_map.loc[len(df_risk_realization_map)] = sample

    return df_rv_sim, df_risk_realization_map

def perform_simulation(df_lite_rr: pd.DataFrame, num_steps: int, num_scenarios: int, independent_sampling: bool,
                       interim_files_dir: str,  save_interim_files: bool = True, selected_seed: int = 110,
                       cap_apply: bool = True, max_cap: float = 400000000.00):
    """Performs the simulation for multiple risk factors."""
    # Create a list containing all risks factors
    list_of_risks = define_unique_risk_factors(df_with_risk_factors=df_lite_rr)

    # Create a DataFrame to store total results of the simulation (for all risk factors)
    #df_total_simulated_impacts = pd.DataFrame(columns=range(num_scenarios))
    df_total_simulated_impacts = pd.DataFrame(np.zeros((num_steps, num_scenarios)))

    # Create a Dictionary to store per risk factor results
    dict_total_results = {}

    for risk in list_of_risks:
        # Define parameters of each risk factor / risk in the risk register
        likelihood_value = df_lite_rr['Converted Likelihood'][df_lite_rr['Risk'] == risk].values[0]
        min_impact_value = df_lite_rr['Converted Lower Impact'][df_lite_rr['Risk'] == risk].values[0]
        max_impact_value = df_lite_rr['Converted Max Impact'][df_lite_rr['Risk'] == risk].values[0]
        distribution_value = df_lite_rr['Distribution'][df_lite_rr['Risk'] == risk].values[0]
        mean_value = df_lite_rr['Mean'][df_lite_rr['Risk'] == risk].values[0]
        std_value = df_lite_rr['Std'][df_lite_rr['Risk'] == risk].values[0]
        # Placeholder(s): values for mean and median are not yet utilized
        mode_value = 0
        median_value = 0

        logger.info(f"Simulating impact of risk factor {str(risk)}...")

        df_risk_sims, df_risk_real_map = sample_risk_impact(
            steps=num_steps, scenarios=num_scenarios, distribution=distribution_value,
            mean=mean_value, std=std_value, mode=mode_value, median=median_value, risk_likelihood=likelihood_value,
            left_tail_impact=min_impact_value, right_tail_impact=max_impact_value,
            min_impact=min_impact_value, max_impact=max_impact_value,
            seed=selected_seed, independent_risk_sampling=independent_sampling, risk_id=risk,
            cap_value=max_cap, cap_impact_per_risk=cap_apply)

        # Update total simulation results DataFrame with the just-simulated risk factor
        df_total_simulated_impacts = df_total_simulated_impacts + df_risk_sims

        # Update Dictionary with results per risk factor
        dict_total_results[str(risk)] = df_risk_sims.copy()

        if save_interim_files:
            temp_alias_results = "simulation_of_impacts_risk_" + str(risk) + ".xlsx"
            temp_alias_materialization = "materialization_risk_" + str(risk) + ".xlsx"

            df_risk_sims.to_excel(os.path.join(interim_files_dir, temp_alias_results))
            df_risk_real_map.to_excel(os.path.join(interim_files_dir, temp_alias_materialization))

        logger.info(f"Simulation of impact for risk factor {str(risk)} completed successfully!")

    if save_interim_files:
        temp_alias_total_results = "Total Simulated Impacts.xlsx"
        df_total_simulated_impacts.to_excel(os.path.join(interim_files_dir, temp_alias_total_results))

    logger.info(f"Simulation of impact for all risk factors completed successfully!")

    return df_total_simulated_impacts,dict_total_results

def extract_simulation_statistics(risk_factor_df_dict, df_rr_lite: pd.DataFrame, df_total_impact_results: pd.DataFrame,
                                  interim_files_dir: str,  save_interim_files: bool = True):
    """Extracts statistics based on simulation results."""
    # 1- Per Risk Factor Statistics
    # Create a list containing all risks factors
    list_of_risks = define_unique_risk_factors(df_with_risk_factors=df_rr_lite)

    # Create a DataFrame to store results at simulation's horizon for each risk factor
    df_horizon_values_per_rf = pd.DataFrame()

    # Create a list to store risk factor titles
    rf_titles = []

    # Create a list to store risk taxonomies
    risk_taxonomies = []

    logger.info(f"Aggregating simulation results per risk factor at horizon...")

    for risk in list_of_risks:
        simulation_horizon_results = risk_factor_df_dict[str(risk)].iloc[-1, :].copy()
        simulation_horizon_results = pd.DataFrame([simulation_horizon_results])
        df_horizon_values_per_rf = pd.concat([df_horizon_values_per_rf, simulation_horizon_results],
                                             axis=0, ignore_index=True)
        rf_titles.append(df_rr_lite['Risk Title'][df_rr_lite['Risk'] == risk].values[0])
        risk_taxonomies.append(df_rr_lite['Taxonomy Level I'][df_rr_lite['Risk'] == risk].values[0])

    # Update Risk Title & Risk taxonomy Information
    df_horizon_values_per_rf['Taxonomy'] = risk_taxonomies.copy()
    df_horizon_values_per_rf['Title'] = rf_titles.copy()

    df_horizon_values_per_rf.index = list_of_risks.copy()
    # ---------------------------------------------------
    # 2- Total Impact Statistics
    df_total_impact_results = df_total_impact_results.iloc[-1,:].copy()

    per_90 = np.percentile(df_total_impact_results.T, 90)
    per_95 = np.percentile(df_total_impact_results.T, 95)
    per_99 = np.percentile(df_total_impact_results.T, 99)
    per_99999 = np.percentile(df_total_impact_results.T, 99.999)

    es_90 = np.mean(df_total_impact_results.T[
                        df_total_impact_results.T >= np.percentile(df_total_impact_results.T, 90)])
    es_95 = np.mean(df_total_impact_results.T[
                        df_total_impact_results.T >= np.percentile(df_total_impact_results.T, 95)])
    es_99 = np.mean(df_total_impact_results.T[
                        df_total_impact_results.T >= np.percentile(df_total_impact_results.T, 99)])

    average_value = np.mean(df_total_impact_results.T)
    median_value = np.median(df_total_impact_results.T)
    mode_value = st.mode(df_total_impact_results.T)[0]

    horizon_stats = {"90%-Percentile Impact": per_90, "95%-Percentile Impact": per_95,
                     "99%-Percentile Impact": per_99, "99.999%-Percentile Impact": per_99999,
                     "90% ES": es_90, "95% ES": es_95, "99% ES": es_99,
                     "Expected Impact": average_value, "Median Impact": median_value, "Mode Impact": mode_value}
    df_impact_total_at_horizon_metrics = pd.DataFrame(horizon_stats, index=["Horizon"])
    # ---------------------------------------------------

    if save_interim_files:
        temp_alias_total_results = "Horizon Results.xlsx"
        df_horizon_values_per_rf.to_excel(os.path.join(interim_files_dir, temp_alias_total_results))

        temp_alias_total_results_total_impact = "Total Impact Metrics at Horizon.xlsx"
        df_impact_total_at_horizon_metrics.to_excel(
            os.path.join(interim_files_dir, temp_alias_total_results_total_impact))

    logger.info(f"Simulation results per risk factor at horizon aggregated successfully!")

    return df_horizon_values_per_rf, df_impact_total_at_horizon_metrics
