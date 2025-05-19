import streamlit as st
import pandas as pd
import numpy as np
from models.fair_model import FAIRModel, TEFInput, VulnerabilityInput, LossInput
from models.monte_carlo import MonteCarloSimulation
from utils.visualization import (
    plot_loss_distribution, 
    plot_cumulative_distribution,
    plot_heat_map,
    plot_sensitivity_analysis,
    plot_loss_exceedance_curve,
    format_currency
)
from utils.data_helpers import load_sample_scenarios

# Set page configuration
st.set_page_config(
    page_title="Risk Analysis - CyberRiskQuant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def display_input_section():
    """Display the risk analysis input section"""
    st.header("Risk Scenario Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Scenario Information")
        
        scenario_name = st.text_input(
            "Scenario Name",
            value=st.session_state.get("scenario_name", "New Risk Scenario"),
            help="Give your risk scenario a descriptive name"
        )
        
        scenario_description = st.text_area(
            "Scenario Description",
            value=st.session_state.get("scenario_description", "Describe the risk scenario in detail"),
            help="Provide a detailed description of the risk scenario you're analyzing"
        )
    
    with col2:
        st.subheader("Distribution Type Selection")
        st.info("""
        **Distribution Types:**
        - **Uniform**: All values in the range are equally likely
        - **Triangular**: Values near the most likely are more probable
        - **PERT**: Similar to triangular, but gives more weight to the most likely value
        - **Lognormal**: Good for modeling losses that can occasionally be very large
        """)
    
    # Create tabs for different input sections
    tef_tab, vuln_tab, loss_tab = st.tabs([
        "Threat Event Frequency (TEF)", 
        "Vulnerability", 
        "Loss Magnitude"
    ])
    
    # Threat Event Frequency inputs
    with tef_tab:
        st.markdown("""
        ### Threat Event Frequency (TEF)
        
        Threat Event Frequency represents how often a threat agent will act against an asset over a given timeframe.
        
        **Examples:**
        - For external hackers: Number of attempted breaches per year
        - For malware: Number of malware encounters per year
        - For insiders: Number of policy violations per year
        """)
        
        tef_col1, tef_col2 = st.columns(2)
        
        with tef_col1:
            tef_min = st.number_input(
                "Minimum TEF (events/year)",
                min_value=0.0,
                value=st.session_state.get("tef_min", 0.1),
                help="The minimum number of threat events expected per year"
            )
            
            tef_max = st.number_input(
                "Maximum TEF (events/year)",
                min_value=tef_min,
                value=max(st.session_state.get("tef_max", 1.0), tef_min),
                help="The maximum number of threat events expected per year"
            )
        
        with tef_col2:
            tef_distribution = st.selectbox(
                "TEF Distribution",
                options=["Uniform", "Triangular", "PERT"],
                index=1 if st.session_state.get("tef_distribution") == "Triangular" else 0,
                help="The probability distribution to use for Threat Event Frequency"
            )
            
            tef_most_likely = None
            if tef_distribution in ["Triangular", "PERT"]:
                tef_most_likely = st.number_input(
                    "Most Likely TEF (events/year)",
                    min_value=tef_min,
                    max_value=tef_max,
                    value=min(max(st.session_state.get("tef_most_likely", (tef_min + tef_max) / 2), tef_min), tef_max),
                    help="The most likely number of threat events per year"
                )
    
    # Vulnerability inputs
    with vuln_tab:
        st.markdown("""
        ### Vulnerability
        
        Vulnerability represents the probability that a threat event will become a loss event.
        
        **Examples:**
        - For phishing attacks: Percentage of employees who might click a malicious link
        - For system exploits: Probability that an attempted exploit succeeds
        - For physical security: Probability that an unauthorized person gains access
        """)
        
        vuln_col1, vuln_col2 = st.columns(2)
        
        with vuln_col1:
            vuln_min = st.number_input(
                "Minimum Vulnerability (probability)",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.get("vuln_min", 0.2),
                format="%.2f",
                help="The minimum probability that a threat event becomes a loss event"
            )
            
            vuln_max = st.number_input(
                "Maximum Vulnerability (probability)",
                min_value=vuln_min,
                max_value=1.0,
                value=max(st.session_state.get("vuln_max", 0.5), vuln_min),
                format="%.2f",
                help="The maximum probability that a threat event becomes a loss event"
            )
        
        with vuln_col2:
            vuln_distribution = st.selectbox(
                "Vulnerability Distribution",
                options=["Uniform", "Triangular", "PERT"],
                index=1 if st.session_state.get("vuln_distribution") == "Triangular" else 0,
                help="The probability distribution to use for Vulnerability"
            )
            
            vuln_most_likely = None
            if vuln_distribution in ["Triangular", "PERT"]:
                vuln_most_likely = st.number_input(
                    "Most Likely Vulnerability (probability)",
                    min_value=vuln_min,
                    max_value=vuln_max,
                    value=min(max(st.session_state.get("vuln_most_likely", (vuln_min + vuln_max) / 2), vuln_min), vuln_max),
                    format="%.2f",
                    help="The most likely probability that a threat event becomes a loss event"
                )
    
    # Loss Magnitude inputs
    with loss_tab:
        st.markdown("""
        ### Loss Magnitude
        
        Loss Magnitude represents the impact in financial terms when a loss event occurs.
        
        **Examples:**
        - For data breaches: Costs of notification, legal fees, regulatory fines, etc.
        - For system outages: Lost revenue, recovery costs, reputation damage
        - For intellectual property theft: Lost competitive advantage, market share reduction
        """)
        
        loss_col1, loss_col2 = st.columns(2)
        
        with loss_col1:
            loss_min = st.number_input(
                "Minimum Loss ($)",
                min_value=0,
                value=int(st.session_state.get("loss_min", 10000)),
                help="The minimum expected loss amount in dollars"
            )
            
            loss_max = st.number_input(
                "Maximum Loss ($)",
                min_value=loss_min,
                value=max(int(st.session_state.get("loss_max", 500000)), loss_min),
                help="The maximum expected loss amount in dollars"
            )
        
        with loss_col2:
            loss_distribution = st.selectbox(
                "Loss Magnitude Distribution",
                options=["Uniform", "Triangular", "PERT", "Lognormal"],
                index=2 if st.session_state.get("loss_distribution") == "PERT" else 0,
                help="The probability distribution to use for Loss Magnitude"
            )
            
            loss_most_likely = None
            if loss_distribution in ["Triangular", "PERT"]:
                loss_most_likely = st.number_input(
                    "Most Likely Loss ($)",
                    min_value=loss_min,
                    max_value=loss_max,
                    value=min(max(int(st.session_state.get("loss_most_likely", (loss_min + loss_max) / 2)), loss_min), loss_max),
                    help="The most likely loss amount in dollars"
                )
    
    # Monte Carlo simulation parameters
    st.subheader("Simulation Parameters")
    
    num_simulations = st.slider(
        "Number of Monte Carlo Simulations",
        min_value=1000,
        max_value=100000,
        value=st.session_state.get("num_simulations", 10000),
        step=1000,
        help="More simulations provide more stable results but take longer to compute"
    )
    
    # Save inputs to session state
    if st.button("Save Inputs & Run Simulation"):
        # Create FAIR model
        fair_model = FAIRModel(
            name=scenario_name,
            description=scenario_description
        )
        
        # Set TEF
        fair_model.set_threat_event_frequency(TEFInput(
            min_value=tef_min,
            max_value=tef_max,
            most_likely=tef_most_likely,
            distribution=tef_distribution.lower()
        ))
        
        # Set Vulnerability
        fair_model.set_vulnerability(VulnerabilityInput(
            min_value=vuln_min,
            max_value=vuln_max,
            most_likely=vuln_most_likely,
            distribution=vuln_distribution.lower()
        ))
        
        # Set Loss Magnitude
        fair_model.set_loss_magnitude(LossInput(
            min_value=loss_min,
            max_value=loss_max,
            most_likely=loss_most_likely,
            distribution=loss_distribution.lower()
        ))
        
        # Store in session state
        st.session_state["fair_model"] = fair_model
        st.session_state["num_simulations"] = num_simulations
        
        # Also store individual values for form persistence
        st.session_state["scenario_name"] = scenario_name
        st.session_state["scenario_description"] = scenario_description
        st.session_state["tef_min"] = tef_min
        st.session_state["tef_max"] = tef_max
        st.session_state["tef_most_likely"] = tef_most_likely
        st.session_state["tef_distribution"] = tef_distribution
        st.session_state["vuln_min"] = vuln_min
        st.session_state["vuln_max"] = vuln_max
        st.session_state["vuln_most_likely"] = vuln_most_likely
        st.session_state["vuln_distribution"] = vuln_distribution
        st.session_state["loss_min"] = loss_min
        st.session_state["loss_max"] = loss_max
        st.session_state["loss_most_likely"] = loss_most_likely
        st.session_state["loss_distribution"] = loss_distribution
        
        # Run the simulation
        run_simulation(fair_model, num_simulations)
        
        # Rerun to show results
        st.rerun()

def run_simulation(fair_model, num_simulations):
    """Run the Monte Carlo simulation and store results in session state"""
    # Create and run the simulation
    simulation = MonteCarloSimulation(fair_model, num_simulations)
    results = simulation.run_simulation()
    
    # Store results in session state
    st.session_state["simulation_results"] = results
    st.session_state["simulation_summary"] = simulation.get_summary_statistics()

def display_results():
    """Display the results of the risk analysis"""
    if "simulation_results" not in st.session_state:
        st.warning("Please configure your risk scenario and run the simulation first.")
        return
    
    st.header("Risk Analysis Results")
    st.subheader(f"Scenario: {st.session_state['fair_model'].name}")
    
    # Display summary statistics
    stats = st.session_state["simulation_summary"]
    
    # Create 3 columns for the key metrics
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
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Loss Distribution", 
        "Cumulative Probability", 
        "Loss Exceedance", 
        "Sensitivity Analysis",
        "Detailed Statistics"
    ])
    
    with tab1:
        st.subheader("Annual Loss Expectancy Distribution")
        st.plotly_chart(
            plot_loss_distribution(st.session_state["simulation_results"]),
            use_container_width=True
        )
        
        st.markdown("""
        **How to interpret this chart:**
        
        This histogram shows the distribution of possible annual losses based on the Monte Carlo simulation. 
        The height of each bar represents the probability density of that loss range.
        
        - The **vertical lines** indicate key percentiles (median, 90th, and 95th).
        - A **wider distribution** indicates greater uncertainty in the loss estimate.
        - The **peak(s)** of the distribution show the most likely loss values.
        """)
    
    with tab2:
        st.subheader("Cumulative Probability Distribution")
        st.plotly_chart(
            plot_cumulative_distribution(st.session_state["simulation_results"]),
            use_container_width=True
        )
        
        st.markdown("""
        **How to interpret this chart:**
        
        The cumulative distribution function (CDF) shows the probability that annual losses will not exceed a given amount.
        
        - The **y-axis** shows the probability (from 0 to 1).
        - The **x-axis** shows the annual loss amount.
        - For any point on the curve, you can determine the probability that losses will not exceed that amount.
        - For example, at the 0.9 probability line, 90% of simulated annual losses fall below this value.
        """)
    
    with tab3:
        st.subheader("Loss Exceedance Curve")
        st.plotly_chart(
            plot_loss_exceedance_curve(st.session_state["simulation_results"]),
            use_container_width=True
        )
        
        st.markdown("""
        **How to interpret this chart:**
        
        The loss exceedance curve shows the probability that annual losses will exceed a given amount.
        
        - The **y-axis** shows the probability (from 0 to 1) on a logarithmic scale.
        - The **x-axis** shows the annual loss amount.
        - For any point on the curve, you can determine the probability that losses will exceed that amount.
        - This is particularly useful for understanding the likelihood of extreme events.
        """)
    
    with tab4:
        st.subheader("Sensitivity Analysis")
        st.plotly_chart(
            plot_sensitivity_analysis(st.session_state["simulation_results"]),
            use_container_width=True
        )
        
        st.markdown("""
        **How to interpret this chart:**
        
        The sensitivity analysis shows how strongly each input parameter correlates with the Annual Loss Expectancy.
        
        - Longer bars indicate stronger correlation with the final loss amount.
        - Positive correlation (blue) means that as the parameter increases, the loss increases.
        - Negative correlation (red) means that as the parameter increases, the loss decreases.
        - This helps identify which parameters have the greatest impact on the risk estimate.
        """)
    
    with tab5:
        st.subheader("Detailed Statistics")
        
        # Create 2 columns for TEF/Vulnerability and Loss Magnitude/ALE
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Threat Event Frequency (events/year)")
            st.write(f"Min: {stats['LEF']['min']:.4f}")
            st.write(f"Max: {stats['LEF']['max']:.4f}")
            st.write(f"Mean: {stats['LEF']['mean']:.4f}")
            st.write(f"Median: {stats['LEF']['median']:.4f}")
            
            st.markdown("#### Vulnerability (probability)")
            st.write(f"Min: {stats['LEF']['min']:.4f}")
            st.write(f"Max: {stats['LEF']['max']:.4f}")
            st.write(f"Mean: {stats['LEF']['mean']:.4f}")
            st.write(f"Median: {stats['LEF']['median']:.4f}")
        
        with col2:
            st.markdown("#### Loss Magnitude ($)")
            st.write(f"Min: {format_currency(stats['Loss_Magnitude']['min'])}")
            st.write(f"Max: {format_currency(stats['Loss_Magnitude']['max'])}")
            st.write(f"Mean: {format_currency(stats['Loss_Magnitude']['mean'])}")
            st.write(f"Median: {format_currency(stats['Loss_Magnitude']['median'])}")
            
            st.markdown("#### Annual Loss Expectancy ($)")
            st.write(f"Min: {format_currency(stats['ALE']['min'])}")
            st.write(f"Max: {format_currency(stats['ALE']['max'])}")
            st.write(f"Mean: {format_currency(stats['ALE']['mean'])}")
            st.write(f"Median: {format_currency(stats['ALE']['median'])}")
            st.write(f"Standard Deviation: {format_currency(stats['ALE']['std'])}")
            st.write(f"90th Percentile: {format_currency(stats['ALE']['percentile_90'])}")
            st.write(f"95th Percentile: {format_currency(stats['ALE']['percentile_95'])}")
            st.write(f"99th Percentile: {format_currency(stats['ALE']['percentile_99'])}")
    
    # Display risk interpretation
    st.header("Risk Interpretation")
    
    mean_ale = stats["ALE"]["mean"]
    p95_ale = stats["ALE"]["percentile_95"]
    
    st.markdown(f"""
    ### Key Findings
    
    Based on the simulation results, we can make the following observations about this risk scenario:
    
    - The **expected annual loss** is {format_currency(mean_ale)}.
    - There is a **95% chance** that annual losses will not exceed {format_currency(p95_ale)}.
    - There is a **50% chance** that annual losses will not exceed {format_currency(stats["ALE"]["median"])}.
    
    ### Recommendations
    
    When evaluating potential security controls or mitigation strategies:
    
    1. Consider controls that cost less than the expected annual loss of {format_currency(mean_ale)} for positive ROI.
    2. For risk transfer strategies (like insurance), consider coverage that addresses the 95th percentile loss of {format_currency(p95_ale)}.
    3. Based on the sensitivity analysis, focus on controls that address the most impactful factors.
    """)
    
    # Option to download the results as CSV
    results_csv = st.session_state["simulation_results"].to_csv(index=False)
    st.download_button(
        label="Download Simulation Results as CSV",
        data=results_csv,
        file_name=f"{st.session_state['fair_model'].name.replace(' ', '_')}_simulation_results.csv",
        mime="text/csv"
    )

def main():
    st.title("Risk Analysis 📊")
    
    # Check if a sample scenario was selected from the home page
    if "selected_sample" in st.session_state and st.session_state["selected_sample"]:
        # Load the sample scenarios
        sample_scenarios = load_sample_scenarios()
        selected_scenario = st.session_state["selected_sample"]
        
        # Check if the scenario exists
        if selected_scenario in sample_scenarios:
            # Load the selected scenario
            fair_model = sample_scenarios[selected_scenario]
            
            # Store in session state
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
            run_simulation(fair_model, 10000)
            
            # Clear the selected sample to prevent reloading
            st.session_state["selected_sample"] = None
    
    # Create tabs for the Risk Analysis page
    input_tab, results_tab = st.tabs(["Risk Inputs", "Analysis Results"])
    
    with input_tab:
        display_input_section()
    
    with results_tab:
        display_results()

if __name__ == "__main__":
    main()
