import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd


def plot_simulation(simulation_df: pd.DataFrame, use_grid: bool = True):
    """Plots all paths (scenarios) of performed simulation."""
    plt.plot(simulation_df)
    plt.title("Simulated Scenarios (Paths)", fontweight="bold", fontsize=12)
    plt.xlabel("Time", fontweight="bold", fontsize=10)
    plt.ylabel("Values", fontweight="bold", fontsize=10)
    plt.grid(use_grid)

    plt.show()


def plot_simulated_distribution(risk_factor_dictionary, risk_factor: str, bins: int = 50,
                                step_index: int = -1, use_grid: bool = True):
    """Plots distribution (histogram) of a selected random variable in a step of simulated process."""
    plt.hist(risk_factor_dictionary[risk_factor].iloc[step_index, :], bins=bins)

    plt.xlabel("Values", fontweight="bold", fontsize=10)
    plt.ylabel("Frequency", fontweight="bold", fontsize=10)
    plt.grid(use_grid)

    plt.show()


def plot_path(risk_factor_dictionary, risk_factor: str, scenario_index: int = 0, used_color: str = "green",
              use_grid: bool = True):
    """Plots a specific path (Scenario) out of the performed simulation."""
    plt.plot(risk_factor_dictionary[risk_factor].iloc[:, scenario_index], color=used_color)
    plt.title("Path (scenario): {}".format(scenario_index), fontweight="bold", fontsize=12)
    plt.xlabel("Time", fontweight="bold", fontsize=10)
    plt.ylabel("Values", fontweight="bold", fontsize=10)
    plt.grid(use_grid)

    plt.show()

def plot_final_impact_distribution(df_impact_results: pd.DataFrame, used_bins: int = 50, use_grid: bool = True):
    """Creates the histogram of simulated distribution of impact."""
    # Format final figure
    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(25e6))  # Tick every 1 million
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    plt.xticks(rotation=30)

    # Create figure
    plt.hist(df_impact_results.iloc[-1,:].T, bins=used_bins)

    # Format axes' labels
    #plt.xlabel("Impact Values", fontweight="bold", fontsize=10)
    plt.xlabel("Aggregated Annual Loss Values", fontweight="bold", fontsize=12)
    plt.ylabel("Frequency", fontweight="bold", fontsize=12)
    plt.title("Aggregated Annual Loss Distribution at Horizon", fontweight="bold", fontsize=10)
    plt.grid(use_grid)

    plt.show()

def plot_loss_curve(df_impact_results: pd.DataFrame, use_grid: bool = True, curve_color: str = "green"):
    """Creates the loss excedance of simulated distribution of impact."""
    # Create DataFrame with data transformed for the curve
    df_new = df_impact_results.T.copy()
    df_new.columns = ['Impact']
    df_new = df_new.sort_values(by='Impact', ascending=False)

    # Add sequential row number starting from 1 (like =ROW(C2)-ROW(C$2)+1)
    df_new['Calculation'] = range(1, len(df_new['Impact']) + 1)

    # Add normalized row number (like =((ROW(C2)-ROW(C$2)+1)/COUNT(C:C)))
    df_new['Normalized Calculation'] = df_new['Calculation'] / len(df_new['Calculation'])

    # Format final figure
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # Set logarithmic scale for x-axis
    ax.set_xscale('log')

    # Add more x-axis ticks and format with commas
    ax.xaxis.set_major_locator(ticker.LogLocator(base=10.0, subs=(1.0, 2.0, 5.0), numticks=20))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    # Set y-axis ticks every 0.1 and format as percentages
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{int(y * 100)}%'))

    # Plot the data from df_new
    #plt.plot(df_new['Impact'], df_new['Normalized Calculation'], marker='o')
    plt.plot(df_new['Impact'], df_new['Normalized Calculation'], color=curve_color)

    # Add labels and title
    #plt.xlabel("Impact Values", fontweight="bold", fontsize=12)
    plt.xlabel("Simulated Aggregated Annual Losses", fontweight="bold", fontsize=12)
    plt.ylabel("Probability", fontweight="bold", fontsize=12)
    plt.title("Loss Exceedance Curve", fontweight="bold", fontsize=14)

    plt.grid(use_grid, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

def plot_risk_taxonomy_dropdown(df_results_per_rf_horizon: pd.DataFrame):
    """Defines impact of different risk taxonomy categories in final impact at horizon."""

    # Create DataFrame pr risk factor only at horizon
    df_results_per_rf_horizon = df_results_per_rf_horizon.iloc[:, :-1]
    df_temp = df_results_per_rf_horizon.drop(['Taxonomy'], axis=1).copy()
    df_temp['Average'] = df_temp.mean(axis=1)
    df_results_per_rf_horizon['Average Impact'] = df_temp['Average'].copy()


    # Group by risk taxonomy category and sum the impact
    category_sum = df_results_per_rf_horizon.groupby('Taxonomy')['Average Impact'].sum().reset_index()

    # Calculate the total sum
    total_sum = category_sum['Average Impact'].sum()

    # Add a percentage column
    category_sum['Pct of Total Impact'] = (category_sum['Average Impact'] / total_sum) * 100.00

    # Pie chart with percentage labels
    labels = category_sum['Taxonomy']
    sizes = category_sum['Average Impact']
    percent_labels = [f'{label}: {pct:.1f}%' for label, pct in zip(labels, category_sum['Pct of Total Impact'])]

    # Optional: define custom colors
    colors = ["#800000", "#FFA500", "#808000", "#008080", "#C0C0C0", "indigo", "#800080", "palevioletred"]

    # Plot
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=percent_labels, colors=colors, startangle=100)
    #plt.title('Impact per Risk Taxonomy Category', fontweight="bold", fontsize=12)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()
    plt.show()

    print(category_sum)


def plot_risk_taxonomy_level2_dropdown(df_results_per_rf_horizon: pd.DataFrame):
    """Defines impact of different risk taxonomy categories level II in final impact at horizon."""

    # Create DataFrame pr risk factor only at horizon
    # df_results_per_rf_horizon = df_results_per_rf_horizon.iloc[:, :-1]
    df_temp = df_results_per_rf_horizon.drop(['Taxonomy', 'Title'], axis=1).copy()
    df_temp['Average'] = df_temp.mean(axis=1)
    df_results_per_rf_horizon['Average Impact'] = df_temp['Average'].copy()


    # Group by risk taxonomy category and sum the impact
    category_sum = df_results_per_rf_horizon.groupby('Taxonomy')['Average Impact'].sum().reset_index()

    # Calculate the total sum
    total_sum = category_sum['Average Impact'].sum()

    # Add a percentage column
    category_sum['Pct of Total Impact'] = (category_sum['Average Impact'] / total_sum) * 100.00

    # Pie chart with percentage labels
    labels = category_sum['Taxonomy']
    sizes = category_sum['Average Impact']
    percent_labels = [f'{label}: {pct:.2f}%' for label, pct in zip(labels, category_sum['Pct of Total Impact'])]

    # Optional: define custom colors
    colors = ["#800000", "#FFA500", "#808000", "#008080", "#C0C0C0", "indigo", "#800080", "palevioletred"]

    # Plot
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=percent_labels, colors=colors, startangle=40, textprops={'fontsize': 7})
    #plt.title('Impact per Risk Taxonomy Level II', fontweight="bold", fontsize=10)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()
    plt.show()

    print(category_sum)
