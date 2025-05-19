import streamlit as st
from utils.data_helpers import get_educational_resources

# Set page configuration
st.set_page_config(
    page_title="Educational Resources - CyberRiskQuant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def display_resource(resource):
    """Display a detailed educational resource"""
    st.header(resource["title"])
    
    st.markdown(resource["content"])
    
    if resource["image"]:
        st.image(resource["image"], use_column_width=True)
    
    st.subheader("References and Further Reading")
    for reference in resource["references"]:
        st.markdown(f"- {reference}")

def fair_model_interactive():
    """Interactive explanation of the FAIR model"""
    st.header("Interactive FAIR Model Explorer")
    
    st.markdown("""
    ## FAIR Model Components
    
    The Factor Analysis of Information Risk (FAIR) model breaks down risk into key components.
    Explore each component in the interactive diagram below.
    """)
    
    # Create a two-level expandable tree diagram using Streamlit's expanders
    
    # Level 1: Risk
    with st.expander("Risk (Annual Loss Expectancy)", expanded=True):
        st.markdown("""
        **Risk** in the FAIR model is calculated as the product of Loss Event Frequency and Loss Magnitude.
        It represents the expected loss over a given time period (typically annual).
        
        `Risk = Loss Event Frequency × Loss Magnitude`
        
        This is often called the Annual Loss Expectancy (ALE) when calculated on a yearly basis.
        """)
        
        # Level 2: Loss Event Frequency
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("Loss Event Frequency (LEF)", expanded=True):
                st.markdown("""
                **Loss Event Frequency (LEF)** is how often a loss event is expected to occur in a given timeframe.
                
                `LEF = Threat Event Frequency × Vulnerability`
                
                A loss event is when a threat successfully exploits a vulnerability and causes a loss.
                """)
                
                # Level 3: TEF and Vulnerability
                with st.expander("Threat Event Frequency (TEF)", expanded=True):
                    st.markdown("""
                    **Threat Event Frequency (TEF)** represents how often a threat agent will act against an asset.
                    
                    Examples:
                    - How often hackers attempt to breach your systems
                    - How often employees might accidentally mishandle data
                    - How often natural disasters might affect operations
                    
                    TEF depends on factors like:
                    - Motivation of threat agents
                    - Resources available to threat agents
                    - Opportunity to attack
                    - Visibility/attractiveness of the target
                    """)
                
                with st.expander("Vulnerability", expanded=True):
                    st.markdown("""
                    **Vulnerability** is the probability that a threat event will become a loss event.
                    
                    It represents the effectiveness of controls relative to the capabilities of threat agents.
                    
                    Examples:
                    - Probability that a phishing email will succeed
                    - Likelihood that an attacker can exploit a system vulnerability
                    - Chance that physical security measures can be bypassed
                    
                    Vulnerability depends on:
                    - Control strength
                    - Threat capability
                    - Control coverage
                    """)
        
        with col2:
            # Level 2: Loss Magnitude
            with st.expander("Loss Magnitude (LM)", expanded=True):
                st.markdown("""
                **Loss Magnitude (LM)** represents the total loss from a single loss event.
                
                `LM = Primary Loss + Secondary Loss`
                
                Loss magnitude quantifies the impact in financial terms, considering both immediate and long-term effects.
                """)
                
                # Level 3: Primary and Secondary Loss
                with st.expander("Primary Loss", expanded=True):
                    st.markdown("""
                    **Primary Loss** is the direct loss resulting from a loss event.
                    
                    Components:
                    - **Productivity loss**: The value of lost productivity
                    - **Response costs**: Costs to investigate and remediate
                    - **Replacement costs**: Costs to replace damaged assets
                    - **Fines and judgments**: Direct regulatory or legal consequences
                    """)
                
                with st.expander("Secondary Loss", expanded=True):
                    st.markdown("""
                    **Secondary Loss** includes indirect or consequential losses.
                    
                    Components:
                    - **Reputation damage**: Lost customers or business opportunities
                    - **Competitive advantage loss**: Stolen IP or strategic information
                    - **Regulatory response**: Increased scrutiny, audits
                    - **Third-party liability**: Claims from affected customers or partners
                    
                    Secondary losses often exceed primary losses in significant security events.
                    """)
    
    st.markdown("""
    ## How FAIR Differs from Traditional Risk Assessment
    
    | Traditional Approach | FAIR Approach |
    |---------------------|---------------|
    | Qualitative (High/Medium/Low) | Quantitative (Dollar values) |
    | Subjective ratings | Probabilistic estimates |
    | Point estimates | Ranges and distributions |
    | Difficult to prioritize | Clear financial basis for decisions |
    | Hard to communicate to executives | Financial terms executives understand |
    """)

def monte_carlo_interactive():
    """Interactive explanation of Monte Carlo simulation"""
    st.header("Monte Carlo Simulation Explorer")
    
    st.markdown("""
    ## How Monte Carlo Simulation Works
    
    Monte Carlo simulation is a powerful technique that helps us understand and quantify uncertainty in our risk estimates.
    Here's how it works in the context of cybersecurity risk quantification:
    """)
    
    # Step-by-step explanation with interactive elements
    steps = [
        {
            "title": "Step 1: Define Input Distributions",
            "content": """
            Instead of using single-point estimates, we define ranges and probability distributions for each input parameter:
            
            - **Threat Event Frequency (TEF)**: How often attacks might occur
            - **Vulnerability**: Probability of attacks succeeding
            - **Loss Magnitude**: Financial impact when a loss occurs
            
            Each distribution reflects our uncertainty about the true value of each parameter.
            """
        },
        {
            "title": "Step 2: Generate Random Samples",
            "content": """
            The simulation randomly samples values from each input distribution.
            
            For example, for a single simulation iteration:
            - TEF might be sampled as 2.3 attacks per year
            - Vulnerability might be sampled as 0.4 (40% chance of success)
            - Loss Magnitude might be sampled as $125,000 per event
            
            Each iteration represents one possible scenario based on our input distributions.
            """
        },
        {
            "title": "Step 3: Calculate Outcomes",
            "content": """
            For each iteration, the sampled values are combined according to the FAIR model:
            
            1. Loss Event Frequency (LEF) = TEF × Vulnerability
               In our example: 2.3 × 0.4 = 0.92 loss events per year
            
            2. Annual Loss Expectancy (ALE) = LEF × Loss Magnitude
               In our example: 0.92 × $125,000 = $115,000
            
            This single result represents one possible outcome given our input uncertainties.
            """
        },
        {
            "title": "Step 4: Repeat Many Times",
            "content": """
            Steps 2-3 are repeated thousands or tens of thousands of times.
            
            Each iteration uses different random samples from our input distributions.
            This builds up a distribution of possible outcomes that reflects our input uncertainties.
            
            Typically, 10,000 iterations provide a stable distribution of results.
            """
        },
        {
            "title": "Step 5: Analyze the Results Distribution",
            "content": """
            The resulting distribution of outcomes allows us to make probability statements about risk:
            
            - The **mean** represents the long-term expected annual loss
            - The **median** represents the most likely outcome (50% chance of being higher or lower)
            - The **90th/95th percentiles** represent reasonable worst-case scenarios
            - The **shape** of the distribution provides insights about uncertainty and skewness
            
            This gives decision-makers much richer information than single-point estimates.
            """
        }
    ]
    
    # Create expandable sections for each step
    for i, step in enumerate(steps):
        with st.expander(step["title"], expanded=i==0):
            st.markdown(step["content"])
    
    st.markdown("""
    ## Benefits of Monte Carlo for Cybersecurity Risk
    
    Monte Carlo simulation offers significant advantages for cybersecurity risk quantification:
    
    1. **Handles uncertainty explicitly** - Instead of hiding uncertainty with point estimates, it makes uncertainty visible and quantifiable
    
    2. **Produces actionable metrics** - Generates probability-based metrics like "95% confidence that losses won't exceed $X"
    
    3. **Enables better decision-making** - Helps prioritize security investments based on financial impact
    
    4. **Improves communication with leadership** - Provides results in financial terms that executives understand
    
    5. **Supports sensitivity analysis** - Identifies which input factors have the greatest impact on risk
    """)

def grc_guides():
    """Display GRC guides and explanations"""
    st.header("Governance, Risk, and Compliance Guides")
    
    st.markdown("""
    ## Understanding GRC in Cybersecurity
    
    Governance, Risk, and Compliance (GRC) is a structured approach to aligning IT with business goals 
    while effectively managing risk and meeting compliance requirements.
    """)
    
    # Create tabs for different GRC topics
    tab1, tab2, tab3 = st.tabs(["Governance", "Risk Management", "Compliance"])
    
    with tab1:
        st.markdown("""
        ## Governance
        
        Governance in cybersecurity refers to the framework of policies, procedures, and processes 
        that direct and control how an organization manages its cybersecurity program.
        
        ### Key Components of Cybersecurity Governance
        
        - **Leadership and Oversight**: Board and executive involvement in cybersecurity
        - **Policies and Standards**: Documented rules and guidelines
        - **Roles and Responsibilities**: Clear definition of security accountabilities
        - **Strategy Alignment**: Ensuring security supports business objectives
        - **Resource Management**: Allocation of people, technology, and budget
        
        ### Governance Frameworks
        
        Several frameworks provide guidance for cybersecurity governance:
        
        - **COBIT (Control Objectives for Information and Related Technologies)**
        - **ISO/IEC 27014 (Governance of Information Security)**
        - **NIST Cybersecurity Framework (Identify Function)**
        - **IT Governance frameworks from ISACA**
        
        ### Best Practices
        
        1. Establish a security steering committee with cross-functional representation
        2. Implement regular reporting to executive leadership and the board
        3. Develop a comprehensive policy framework with regular reviews
        4. Align security initiatives with business objectives and risk appetite
        5. Establish metrics to measure the effectiveness of the security program
        """)
    
    with tab2:
        st.markdown("""
        ## Risk Management
        
        Cybersecurity risk management is the ongoing process of identifying, assessing, and responding 
        to risks to information assets in a way that aligns with business objectives.
        
        ### The Risk Management Lifecycle
        
        1. **Risk Identification**: Discovering and documenting potential risks
        2. **Risk Assessment**: Analyzing and evaluating identified risks
        3. **Risk Treatment**: Selecting and implementing controls
        4. **Risk Monitoring**: Ongoing tracking of risks and control effectiveness
        
        ### Risk Assessment Approaches
        
        - **Qualitative**: Using scales (high/medium/low) to assess risks
        - **Quantitative**: Using numerical values (like FAIR) to measure risks
        - **Hybrid**: Combining qualitative and quantitative methods
        
        ### Risk Treatment Options
        
        - **Risk Acceptance**: Acknowledging and accepting the risk
        - **Risk Mitigation**: Implementing controls to reduce risk
        - **Risk Transfer**: Shifting risk to another party (e.g., insurance)
        - **Risk Avoidance**: Eliminating the risky activity or system
        
        ### Risk Management Frameworks
        
        - **ISO 31000**: General risk management principles
        - **NIST SP 800-30**: Guide for conducting risk assessments
        - **NIST Cybersecurity Framework**: Risk-based approach to cybersecurity
        - **FAIR**: Factor Analysis of Information Risk for quantitative analysis
        """)
    
    with tab3:
        st.markdown("""
        ## Compliance
        
        Compliance in cybersecurity involves ensuring that an organization adheres to internal policies, 
        industry standards, and legal/regulatory requirements related to information security.
        
        ### Types of Compliance Requirements
        
        - **Regulatory**: Government-mandated requirements (HIPAA, GDPR, SOX, etc.)
        - **Industry**: Sector-specific standards (PCI DSS, NERC CIP, etc.)
        - **Contractual**: Requirements from business agreements
        - **Internal**: Organization's own policies and standards
        
        ### Common Compliance Frameworks
        
        - **ISO/IEC 27001**: Information security management systems
        - **SOC 2**: Service Organization Control reports
        - **PCI DSS**: Payment Card Industry Data Security Standard
        - **HIPAA**: Health Insurance Portability and Accountability Act
        - **GDPR**: General Data Protection Regulation
        - **CCPA/CPRA**: California Consumer Privacy Act/California Privacy Rights Act
        
        ### Compliance Program Elements
        
        1. **Requirement Mapping**: Identifying applicable requirements
        2. **Policy Development**: Creating policies that meet requirements
        3. **Control Implementation**: Deploying technical and procedural safeguards
        4. **Training and Awareness**: Educating employees on compliance
        5. **Monitoring and Testing**: Verifying control effectiveness
        6. **Documentation**: Maintaining evidence of compliance
        7. **Audit and Assessment**: Evaluating the compliance program
        
        ### Compliance Challenges
        
        - Keeping up with changing regulations
        - Managing overlapping requirements
        - Balancing compliance with business agility
        - Demonstrating compliance to multiple stakeholders
        - Moving beyond "checkbox compliance" to effective security
        """)
    
    st.markdown("""
    ## Integrating GRC for Effective Cybersecurity
    
    A mature cybersecurity program integrates governance, risk management, and compliance:
    
    - **Governance** provides direction and oversight
    - **Risk Management** identifies and addresses security threats
    - **Compliance** ensures adherence to requirements
    
    ### Benefits of an Integrated Approach
    
    1. **Reduced Redundancy**: Eliminates duplicate efforts across governance, risk, and compliance activities
    2. **Improved Decision-Making**: Provides a comprehensive view for more informed security decisions
    3. **Enhanced Resource Allocation**: Directs resources to the most impactful security initiatives
    4. **Better Stakeholder Communication**: Offers consistent messaging about security posture
    5. **Increased Operational Efficiency**: Streamlines processes and reduces overhead
    
    ### GRC Technology Solutions
    
    Modern GRC platforms help organizations:
    
    - Centralize documentation of policies, controls, and risks
    - Automate assessment and monitoring processes
    - Provide dashboards and reporting for stakeholders
    - Track remediation activities and progress
    - Demonstrate compliance with multiple frameworks
    """)

def main():
    st.title("Educational Resources 📚")
    
    st.markdown("""
    This section provides educational resources about cybersecurity risk quantification, 
    the FAIR model, and GRC (Governance, Risk, and Compliance) concepts. Use these resources 
    to deepen your understanding of cybersecurity risk management.
    """)
    
    # Custom navigation for educational resources
    resource_type = st.radio(
        "Select a topic to learn about:",
        ["FAIR Model", "Monte Carlo Simulation", "GRC Concepts", "Detailed Resources"],
        horizontal=True
    )
    
    if resource_type == "FAIR Model":
        fair_model_interactive()
    
    elif resource_type == "Monte Carlo Simulation":
        monte_carlo_interactive()
    
    elif resource_type == "GRC Concepts":
        grc_guides()
    
    elif resource_type == "Detailed Resources":
        # Load educational resources
        resources = get_educational_resources()
        
        # Create a selectbox to choose a resource
        selected_resource = st.selectbox(
            "Select a resource to view:",
            options=list(resources.keys())
        )
        
        # Display the selected resource
        display_resource(resources[selected_resource])
    
    # Additional learning resources
    with st.expander("Additional Learning Resources"):
        st.markdown("""
        ## Books
        
        - **Measuring and Managing Information Risk: A FAIR Approach** by Jack Freund and Jack Jones
        - **How to Measure Anything in Cybersecurity Risk** by Douglas W. Hubbard and Richard Seiersen
        - **Security Risk Management** by Evan Wheeler
        - **The Cyber Risk Handbook** by Domenic Antonucci
        
        ## Online Resources
        
        - **FAIR Institute**: [fairinstitute.org](https://www.fairinstitute.org/)
        - **NIST Cybersecurity Framework**: [nist.gov/cyberframework](https://www.nist.gov/cyberframework)
        - **ISACA Risk IT Framework**: [isaca.org](https://www.isaca.org/)
        - **Open Group FAIR Standards**: [opengroup.org/certifications/openfair](https://www.opengroup.org/certifications/openfair)
        
        ## Courses and Certifications
        
        - **Open FAIR Certification**
        - **CRISC (Certified in Risk and Information Systems Control)**
        - **CISM (Certified Information Security Manager)**
        - **CISSP (Certified Information Systems Security Professional)**
        """)

if __name__ == "__main__":
    main()
