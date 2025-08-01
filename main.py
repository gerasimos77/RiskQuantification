from tools.register_reader import read_risk_register_lite
from tools.directory_creator import create_output_dir
from model.simple_simulation_engine import perform_simulation, extract_simulation_statistics

def perform_risk_register_quantification(
        number_of_scenarios: int, number_of_steps: int,
        risk_register_lite_path: str = r'C:\Users\g.varvounis\Documents\RiskQuantification\runner\inputs',
        risk_register_lite_filename: str = r'risk register lite.xlsx',
        risk_register_sheet_name: str = r'RR Lite',
        output_path_folder: str = r'C:\Users\g.varvounis\Documents\RiskQuantification\runner\outputs',
        save_interim_outputs: bool = True, seed_to_replicate_samples: int = 110,
        bernoulli_materialization_of_risks:bool = True,
        apply_cap: bool = True, selected_cap: float = 400000000.00):
    """Orchestrator function for performing the risk register quantification exercise."""

    # Create output Directory
    output_path_part = create_output_dir(model_dir=output_path_folder)

    # Import risk register lite from respective folder
    df_risk_register = read_risk_register_lite(file_name=risk_register_lite_filename,
                                               register_dir=risk_register_lite_path, sheet=risk_register_sheet_name)

    # Perform the simulation of impact for all risk factors / risks in the risk register
    df_total_risk_factors, dictionary_paths_per_risk_factor = perform_simulation(
            df_lite_rr=df_risk_register, save_interim_files=save_interim_outputs,
            interim_files_dir=output_path_part, num_steps=number_of_steps,
            num_scenarios=number_of_scenarios, selected_seed=seed_to_replicate_samples,
            independent_sampling=bernoulli_materialization_of_risks, cap_apply=apply_cap, max_cap=selected_cap)

    # Extract useful statistics based on simulation's results
    df_horizon_summary_per_rf_per_scenario, df_metrics_total_impact_horizon = extract_simulation_statistics(
            risk_factor_df_dict=dictionary_paths_per_risk_factor, df_rr_lite=df_risk_register,
            save_interim_files=save_interim_outputs, interim_files_dir=output_path_part,
        df_total_impact_results=df_total_risk_factors)

    return (df_total_risk_factors, dictionary_paths_per_risk_factor, df_horizon_summary_per_rf_per_scenario,
            df_metrics_total_impact_horizon)


if __name__ == "__main__":

    df_temporary,_, _,_ = perform_risk_register_quantification(5, 4)

    #print(df_temporary)
    #print(df_temporary.info())
    #print(df_temporary.shape)