import streamlit as st
import pandas as pd
import numpy as np
from models.fair_model import FAIRModel
from models.monte_carlo import MonteCarloSimulation
from utils.visualization import (
    plot_loss_distribution, 
    plot_cumulative_distribution, 
    plot_loss_exceedance_curve,
    format_currency
)
from utils.data_helpers import load_case_studies

# Set page configuration
st.set_page_config(
    page_title="Case Studies - CyberRiskQuant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def display_case_study(case_study):
    """Display a detailed case study with analysis and visualizations"""
    st.header(case_study["title"])
    
    # Display key information about the case study
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Industry")
        st.write(case_study["industry"])
        
        st.subheader("Scenario")
        st.write(case_study["scenario"])
    
    with col2:
        st.subheader("Description")
        st.write(case_study["description"])
    
    # Impact areas and mitigations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Impact Areas")
        for impact in case_study["impact_areas"]:
            st.write(f"- {impact}")
    
    with col2:
        st.subheader("Key Mitigations")
        for mitigation in case_study["mitigations"]:
            st.write(f"- {mitigation}")
    
    # Run Monte Carlo simulation
    fair_model = case_study["fair_model"]
    simulation = MonteCarloSimulation(fair_model, 10000)
    results = simulation.run_simulation()
    stats = simulation.get_summary_statistics()
    
    # Display key metrics
    st.subheader("Risk Quantification")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Average Annual Loss",
            format_currency(stats["ALE"]["mean"]),
            help="The expected average loss per year over time"
        )
    
    with col2:
        st.metric(
            "Median Annual Loss",
            format_currency(stats["ALE"]["median"]),
            help="The middle value of the annual loss distribution (50% of simulations are below this value)"
        )
    
    with col3:
        st.metric(
            "95th Percentile Loss",
            format_currency(stats["ALE"]["percentile_95"]),
            help="The 'worst case' annual loss (only 5% of simulations exceed this value)"
        )
    
    # Create tabs for visualizations
    tab1, tab2 = st.tabs(["Loss Distribution", "Cumulative Probability"])
    
    with tab1:
        st.plotly_chart(
            plot_loss_distribution(results),
            use_container_width=True
        )
    
    with tab2:
        st.plotly_chart(
            plot_cumulative_distribution(results),
            use_container_width=True
        )
    
    # Key lessons learned
    st.subheader("Key Lessons")
    for lesson in case_study["lessons"]:
        st.markdown(f"- {lesson}")
    
    # Risk analysis interpretation
    st.subheader("Risk Analysis Interpretation")
    st.write(f"""
    The risk analysis for this {case_study["industry"]} scenario shows an expected annual loss of 
    {format_currency(stats["ALE"]["mean"])}, with a 95% confidence that annual losses will not exceed 
    {format_currency(stats["ALE"]["percentile_95"])}.
    
    The Loss Event Frequency (LEF) analysis indicates that this type of event can be expected to occur 
    {stats["LEF"]["mean"]:.2f} times per year on average, with each event causing an average loss of 
    {format_currency(stats["Loss_Magnitude"]["mean"])}.
    
    This case demonstrates how the FAIR model can help organizations quantify complex cyber risks 
    and make more informed decisions about security investments and risk mitigation strategies.
    """)
    
    # Option to use this case study as a basis for your own analysis
    if st.button("Use This Scenario as Template"):
        # Store the FAIR model in session state
        st.session_state["fair_model"] = fair_model
        st.session_state["scenario_name"] = fair_model.name
        st.session_state["scenario_description"] = fair_model.description
        
        # Store TEF parameters
        st.session_state["tef_min"] = fair_model.tef.min_value
        st.session_state["tef_max"] = fair_model.tef.max_value
        st.session_state["tef_most_likely"] = fair_model.tef.most_likely
        st.session_state["tef_distribution"] = fair_model.tef.distribution.capitalize()
        
        # Store Vulnerability parameters
        st.session_state["vuln_min"] = fair_model.vulnerability.min_value
        st.session_state["vuln_max"] = fair_model.vulnerability.max_value
        st.session_state["vuln_most_likely"] = fair_model.vulnerability.most_likely
        st.session_state["vuln_distribution"] = fair_model.vulnerability.distribution.capitalize()
        
        # Store Loss Magnitude parameters
        st.session_state["loss_min"] = fair_model.loss_magnitude.min_value
        st.session_state["loss_max"] = fair_model.loss_magnitude.max_value
        st.session_state["loss_most_likely"] = fair_model.loss_magnitude.most_likely
        st.session_state["loss_distribution"] = fair_model.loss_magnitude.distribution.capitalize()
        
        # Set number of simulations
        st.session_state["num_simulations"] = 10000
        
        # Run the simulation
        simulation = MonteCarloSimulation(fair_model, 10000)
        results = simulation.run_simulation()
        
        # Store in session state
        st.session_state["simulation_results"] = results
        st.session_state["simulation_summary"] = simulation.get_summary_statistics()
        
        # Navigate to the risk analysis page
        st.switch_page("pages/1_Risk_Analysis.py")

def compare_case_studies(case_studies):
    """Compare multiple case studies side by side"""
    st.header("Case Study Comparison")
    
    # Select case studies to compare
    selected_cases = st.multiselect(
        "Select case studies to compare",
        options=list(case_studies.keys()),
        default=list(case_studies.keys())[:2]
    )
    
    if len(selected_cases) < 2:
        st.warning("Please select at least two case studies to compare.")
        return
    
    # Run simulations for each selected case study
    simulation_results = []
    labels = []
    
    for case_name in selected_cases:
        fair_model = case_studies[case_name]["fair_model"]
        simulation = MonteCarloSimulation(fair_model, 10000)
        results = simulation.run_simulation()
        simulation_results.append(results)
        labels.append(case_name)
    
    # Create comparison table
    comparison_data = []
    
    for i, case_name in enumerate(selected_cases):
        stats = MonteCarloSimulation(
            case_studies[case_name]["fair_model"], 10000
        ).get_summary_statistics()
        
        comparison_data.append({
            "Case Study": case_name,
            "Industry": case_studies[case_name]["industry"],
            "Mean Annual Loss": stats["ALE"]["mean"],
            "Median Annual Loss": stats["ALE"]["median"],
            "95th Percentile Loss": stats["ALE"]["percentile_95"],
            "Mean Loss Event Frequency": stats["LEF"]["mean"],
            "Mean Loss Magnitude": stats["Loss_Magnitude"]["mean"]
        })
    
    # Convert to DataFrame and display
    comparison_df = pd.DataFrame(comparison_data)
    
    # Format currency columns
    for col in ["Mean Annual Loss", "Median Annual Loss", "95th Percentile Loss", "Mean Loss Magnitude"]:
        comparison_df[col] = comparison_df[col].apply(format_currency)
    
    # Format frequency column
    comparison_df["Mean Loss Event Frequency"] = comparison_df["Mean Loss Event Frequency"].apply(
        lambda x: f"{x:.2f} events/year"
    )
    
    st.dataframe(comparison_df, use_container_width=True)
    
    # Create loss distribution comparison
    st.subheader("Annual Loss Expectancy Comparison")
    
    # Create a combined histogram
    import plotly.graph_objects as go
    
    fig = go.Figure()
    colors = ["blue", "red", "green", "purple", "orange"]
    
    for i, (results, label) in enumerate(zip(simulation_results, labels)):
        fig.add_trace(go.Histogram(
            x=results["ALE"],
            name=label,
            opacity=0.7,
            histnorm='probability density',
            marker_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        title="Annual Loss Expectancy Comparison",
        xaxis_title="Annual Loss Expectancy ($)",
        yaxis_title="Probability Density",
        barmode='overlay',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Comparison insights
    st.subheader("Comparison Insights")
    
    # Sort case studies by mean annual loss
    sorted_cases = sorted(
        comparison_data,
        key=lambda x: float(x["Mean Annual Loss"].replace("$", "").replace(",", ""))
    )
    
    highest_risk = sorted_cases[-1]["Case Study"]
    lowest_risk = sorted_cases[0]["Case Study"]
    
    st.markdown(f"""
    #### Key Observations:
    
    - The **{highest_risk}** case study presents the highest risk in terms of expected annual loss.
    - The **{lowest_risk}** case study presents the lowest risk in terms of expected annual loss.
    - Different industries face different risk profiles, as shown by the varying shapes of the loss distributions.
    - The 95th percentile loss (often used for risk planning) varies significantly across scenarios.
    
    #### Practical Applications:
    
    - Organizations can use this comparative approach to prioritize risk mitigation efforts across different risk scenarios.
    - Understanding the relative magnitude of different risks helps in allocating security budgets effectively.
    - The varying risk profiles across industries highlight the importance of industry-specific risk assessment.
    """)

def main():
    st.title("Case Studies 📋")
    
    st.markdown("""
    Explore detailed case studies demonstrating how the FAIR model and Monte Carlo simulations
    can be applied to real-world cybersecurity risk scenarios. These examples illustrate how 
    organizations can quantify and manage their cyber risks effectively.
    
    You can:
    - Examine individual case studies in detail
    - Compare multiple case studies side by side
    - Use any case study as a template for your own risk analysis
    """)
    
    # Load case studies
    case_studies = load_case_studies()
    
    # Create tabs for individual case studies and comparison
    tabs = ["Comparison"] + list(case_studies.keys())
    selected_tab = st.tabs(tabs)
    
    # Comparison tab
    with selected_tab[0]:
        compare_case_studies(case_studies)
    
    # Individual case study tabs
    for i, case_name in enumerate(case_studies.keys()):
        with selected_tab[i+1]:
            display_case_study(case_studies[case_name])

if __name__ == "__main__":
    main()
