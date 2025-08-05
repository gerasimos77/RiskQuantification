import pytest
from main import perform_risk_register_quantification
from tools.files_excel_investigator import are_excel_files_identical

def test_bernoulli_run(
        number_of_scenarios=10000, number_of_steps=1,
        directory_of_risk_register_lite=
        r'C:\Users\g.varvounis\Documents\RiskQuantification\tests\inputs\scenario_testing\bernoulli_sampling_case',
        filename_of_risk_register_lite = r'risk register lite.xlsx',
        sheetname_of_risk_register_lite = r'RR Lite',
        save_intermediate_files_produced_during_run = False,
        desired_directory_for_code_outputs = r'C:\Users\g.varvounis\Documents\RiskQuantification\runner\outputs',
        replication_id = 50, materialization_of_risks_based_on_bernoulli_distro = True, use_cap = True,
        cap_val= 400000000):
    """Scenario test; testing module with bernoulli sampling."""
    df_results, _, df_horizon_summary, df_metrics = perform_risk_register_quantification(
        number_of_scenarios=number_of_scenarios, number_of_steps=number_of_steps,
        risk_register_lite_path=directory_of_risk_register_lite,
        risk_register_lite_filename=filename_of_risk_register_lite,
        risk_register_sheet_name=sheetname_of_risk_register_lite, output_path_folder=desired_directory_for_code_outputs,
        save_interim_outputs=save_intermediate_files_produced_during_run, seed_to_replicate_samples=replication_id,
        bernoulli_materialization_of_risks=materialization_of_risks_based_on_bernoulli_distro, apply_cap=use_cap,
        selected_cap=cap_val)

    df_results.to_excel(
        r'C:\Users\g.varvounis\Documents\RiskQuantification\tests\outputs\scenario_testing\bernoulli_sampling_case\df_results_bernoulli_test.xlsx')

    df_horizon_summary.to_excel(
        r'C:\Users\g.varvounis\Documents\RiskQuantification\tests\outputs\scenario_testing\bernoulli_sampling_case\df_horizon_summary_bernoulli_test.xlsx')

    df_metrics.to_excel(
        r'C:\Users\g.varvounis\Documents\RiskQuantification\tests\outputs\scenario_testing\bernoulli_sampling_case\df_metrics_bernoulli_test.xlsx')

    assert are_excel_files_identical(file1_path=r'C:\Users\g.varvounis\Documents\RiskQuantification\tests\outputs\scenario_testing\bernoulli_sampling_case\df_results_bernoulli_expected.xlsx',
                                     file2_path=r'C:\Users\g.varvounis\Documents\RiskQuantification\tests\outputs\scenario_testing\bernoulli_sampling_case\df_results_bernoulli_test.xlsx')

    assert are_excel_files_identical(
        file1_path=r'C:\Users\g.varvounis\Documents\RiskQuantification\tests\outputs\scenario_testing\bernoulli_sampling_case\df_horizon_summary_bernoulli_expected.xlsx',
        file2_path=r'C:\Users\g.varvounis\Documents\RiskQuantification\tests\outputs\scenario_testing\bernoulli_sampling_case\df_horizon_summary_bernoulli_test.xlsx')

    assert are_excel_files_identical(
        file1_path=r'C:\Users\g.varvounis\Documents\RiskQuantification\tests\outputs\scenario_testing\bernoulli_sampling_case\df_metrics_bernoulli_expected.xlsx',
        file2_path=r'C:\Users\g.varvounis\Documents\RiskQuantification\tests\outputs\scenario_testing\bernoulli_sampling_case\df_metrics_bernoulli_test.xlsx')