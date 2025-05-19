import pandas as pd
import numpy as np
from models.fair_model import FAIRModel, TEFInput, VulnerabilityInput, LossInput

def load_sample_scenarios():
    """
    Load a set of predefined sample risk scenarios.
    
    Returns:
        Dictionary of sample scenarios
    """
    # Sample scenario 1: Data Breach
    data_breach = FAIRModel(
        name="Data Breach Scenario",
        description="A scenario involving unauthorized access to sensitive customer data"
    )
    data_breach.set_threat_event_frequency(TEFInput(
        min_value=0.5,
        max_value=3.0,
        most_likely=1.0,
        distribution="triangular"
    ))
    data_breach.set_vulnerability(VulnerabilityInput(
        min_value=0.2,
        max_value=0.6,
        most_likely=0.3,
        distribution="triangular"
    ))
    data_breach.set_loss_magnitude(LossInput(
        min_value=100000,
        max_value=2000000,
        most_likely=500000,
        distribution="pert"
    ))
    
    # Sample scenario 2: Ransomware Attack
    ransomware = FAIRModel(
        name="Ransomware Attack",
        description="A scenario involving a ransomware attack causing business disruption"
    )
    ransomware.set_threat_event_frequency(TEFInput(
        min_value=0.1,
        max_value=1.0,
        most_likely=0.3,
        distribution="triangular"
    ))
    ransomware.set_vulnerability(VulnerabilityInput(
        min_value=0.3,
        max_value=0.8,
        most_likely=0.5,
        distribution="triangular"
    ))
    ransomware.set_loss_magnitude(LossInput(
        min_value=50000,
        max_value=5000000,
        most_likely=750000,
        distribution="lognormal"
    ))
    
    # Sample scenario 3: DDoS Attack
    ddos = FAIRModel(
        name="DDoS Attack",
        description="A Distributed Denial of Service attack disrupting online services"
    )
    ddos.set_threat_event_frequency(TEFInput(
        min_value=1.0,
        max_value=10.0,
        most_likely=4.0,
        distribution="triangular"
    ))
    ddos.set_vulnerability(VulnerabilityInput(
        min_value=0.1,
        max_value=0.5,
        most_likely=0.3,
        distribution="triangular"
    ))
    ddos.set_loss_magnitude(LossInput(
        min_value=10000,
        max_value=500000,
        most_likely=100000,
        distribution="pert"
    ))
    
    # Sample scenario 4: Insider Threat
    insider_threat = FAIRModel(
        name="Insider Threat",
        description="A scenario involving data theft or sabotage by an employee"
    )
    insider_threat.set_threat_event_frequency(TEFInput(
        min_value=0.05,
        max_value=1.0,
        most_likely=0.2,
        distribution="triangular"
    ))
    insider_threat.set_vulnerability(VulnerabilityInput(
        min_value=0.3,
        max_value=0.7,
        most_likely=0.5,
        distribution="triangular"
    ))
    insider_threat.set_loss_magnitude(LossInput(
        min_value=50000,
        max_value=3000000,
        most_likely=500000,
        distribution="pert"
    ))
    
    # Sample scenario 5: Cloud Service Outage
    cloud_outage = FAIRModel(
        name="Cloud Service Outage",
        description="A scenario involving an extended outage of a critical cloud service"
    )
    cloud_outage.set_threat_event_frequency(TEFInput(
        min_value=0.5,
        max_value=3.0,
        most_likely=1.0,
        distribution="triangular"
    ))
    cloud_outage.set_vulnerability(VulnerabilityInput(
        min_value=0.1,
        max_value=0.4,
        most_likely=0.2,
        distribution="triangular"
    ))
    cloud_outage.set_loss_magnitude(LossInput(
        min_value=20000,
        max_value=1000000,
        most_likely=200000,
        distribution="pert"
    ))
    
    # Return the scenarios as a dictionary
    return {
        "Data Breach Scenario": data_breach,
        "Ransomware Attack": ransomware,
        "DDoS Attack": ddos,
        "Insider Threat": insider_threat,
        "Cloud Service Outage": cloud_outage
    }

def load_case_studies():
    """
    Load detailed case studies for educational purposes.
    
    Returns:
        Dictionary of case studies with associated data
    """
    case_studies = {
        "Healthcare Data Breach": {
            "title": "Healthcare Data Breach",
            "industry": "Healthcare",
            "scenario": "A major hospital system experiences a data breach exposing patient records.",
            "description": """
            A large hospital system with multiple locations experienced a breach where an unauthorized 
            third party gained access to patient health records including personal and financial information. 
            The breach affected approximately 50,000 patients and resulted in significant costs related to 
            breach notification, credit monitoring, regulatory fines, legal fees, and reputation damage.
            """,
            "fair_model": FAIRModel(
                name="Healthcare Data Breach",
                description="Data breach at a large hospital system"
            ),
            "impact_areas": [
                "HIPAA fines and penalties",
                "Breach notification costs",
                "Credit monitoring services",
                "Legal defense costs",
                "IT forensics and remediation",
                "Lost business and reputation damage"
            ],
            "mitigations": [
                "Enhanced data encryption",
                "Multi-factor authentication",
                "Regular security assessments",
                "Employee security training",
                "Data loss prevention tools",
                "Improved incident response planning"
            ],
            "lessons": [
                "Healthcare organizations face strict regulatory requirements for data protection.",
                "The cost of a breach extends far beyond the immediate technical response.",
                "Preventative measures are significantly less expensive than breach recovery.",
                "Having an incident response plan reduces the financial impact of a breach."
            ]
        },
        
        "Financial Services Ransomware": {
            "title": "Financial Services Ransomware",
            "industry": "Financial Services",
            "scenario": "A midsize financial institution is hit with a sophisticated ransomware attack.",
            "description": """
            A regional bank with 50 branches was targeted by a ransomware attack that encrypted critical 
            systems and demanded a $1 million ransom. The attack resulted in a 3-day operational outage, 
            affecting online banking, ATM networks, and branch operations. The institution had to restore 
            from backups and rebuild several systems, while facing customer dissatisfaction and potential 
            regulatory scrutiny.
            """,
            "fair_model": FAIRModel(
                name="Financial Services Ransomware",
                description="Ransomware attack on a midsize regional bank"
            ),
            "impact_areas": [
                "Business interruption costs",
                "IT recovery and restoration",
                "Customer compensation",
                "Regulatory response",
                "Reputation damage and customer churn",
                "Enhanced security measures"
            ],
            "mitigations": [
                "Robust and segregated backup systems",
                "Network segmentation",
                "Advanced endpoint protection",
                "24/7 security monitoring",
                "Regular penetration testing",
                "Employee awareness training"
            ],
            "lessons": [
                "Financial institutions are prime targets for ransomware attacks.",
                "Business continuity planning is critical for minimizing downtime costs.",
                "The decision to pay or not pay ransom should be evaluated through risk quantification.",
                "Having isolated, tested backups significantly reduces recovery time and costs."
            ]
        },
        
        "Manufacturing Supply Chain Attack": {
            "title": "Manufacturing Supply Chain Attack",
            "industry": "Manufacturing",
            "scenario": "A manufacturer experiences a cyber attack through a third-party supplier.",
            "description": """
            A large automotive parts manufacturer was compromised when attackers gained access through 
            a vulnerable third-party inventory management system. The attackers remained undetected for 
            3 months, eventually deploying malware that disrupted production systems at two facilities. 
            The incident resulted in a one-week production stoppage and the theft of proprietary design 
            specifications.
            """,
            "fair_model": FAIRModel(
                name="Manufacturing Supply Chain Attack",
                description="Cyber attack via third-party supplier affecting production"
            ),
            "impact_areas": [
                "Production downtime costs",
                "Remediation and recovery expenses",
                "Contractual penalties for missed deliveries",
                "Intellectual property theft",
                "Third-party liability",
                "Enhanced security controls"
            ],
            "mitigations": [
                "Third-party risk management program",
                "Vendor security assessments",
                "Network segmentation between vendors and production",
                "Enhanced monitoring for lateral movement",
                "Contractual security requirements",
                "Regular security testing of supply chain connections"
            ],
            "lessons": [
                "Supply chain vulnerabilities can provide attackers with an entry point.",
                "Production downtime often represents the largest cost component in manufacturing.",
                "Third-party connections should be continuously monitored and assessed.",
                "The true cost of intellectual property theft can be difficult to quantify but substantial."
            ]
        }
    }
    
    # Configure the FAIR models for each case study
    case_studies["Healthcare Data Breach"]["fair_model"].set_threat_event_frequency(TEFInput(
        min_value=0.2,
        max_value=1.0,
        most_likely=0.5,
        distribution="triangular"
    ))
    case_studies["Healthcare Data Breach"]["fair_model"].set_vulnerability(VulnerabilityInput(
        min_value=0.3,
        max_value=0.7,
        most_likely=0.5,
        distribution="triangular"
    ))
    case_studies["Healthcare Data Breach"]["fair_model"].set_loss_magnitude(LossInput(
        min_value=800000,
        max_value=3500000,
        most_likely=1500000,
        distribution="pert"
    ))
    
    case_studies["Financial Services Ransomware"]["fair_model"].set_threat_event_frequency(TEFInput(
        min_value=0.1,
        max_value=1.5,
        most_likely=0.4,
        distribution="triangular"
    ))
    case_studies["Financial Services Ransomware"]["fair_model"].set_vulnerability(VulnerabilityInput(
        min_value=0.2,
        max_value=0.6,
        most_likely=0.4,
        distribution="triangular"
    ))
    case_studies["Financial Services Ransomware"]["fair_model"].set_loss_magnitude(LossInput(
        min_value=500000,
        max_value=5000000,
        most_likely=1200000,
        distribution="lognormal"
    ))
    
    case_studies["Manufacturing Supply Chain Attack"]["fair_model"].set_threat_event_frequency(TEFInput(
        min_value=0.05,
        max_value=0.5,
        most_likely=0.2,
        distribution="triangular"
    ))
    case_studies["Manufacturing Supply Chain Attack"]["fair_model"].set_vulnerability(VulnerabilityInput(
        min_value=0.4,
        max_value=0.8,
        most_likely=0.6,
        distribution="triangular"
    ))
    case_studies["Manufacturing Supply Chain Attack"]["fair_model"].set_loss_magnitude(LossInput(
        min_value=1000000,
        max_value=8000000,
        most_likely=3000000,
        distribution="pert"
    ))
    
    return case_studies

def get_educational_resources():
    """
    Return a dictionary of educational resources about GRC concepts.
    
    Returns:
        Dictionary of educational resources
    """
    resources = {
        "FAIR Model Overview": {
            "title": "Factor Analysis of Information Risk (FAIR) Model",
            "content": """
            ## What is FAIR?
            
            The Factor Analysis of Information Risk (FAIR) is a framework for understanding, analyzing, and measuring information risk. 
            Unlike traditional qualitative risk frameworks that use "high/medium/low" ratings, FAIR provides a quantitative, probabilistic 
            approach to risk analysis.
            
            ## Key Components of FAIR
            
            The FAIR model breaks down risk into its fundamental components:
            
            ### 1. Loss Event Frequency (LEF)
            How often is a loss likely to occur? This is further broken down into:
            
            - **Threat Event Frequency (TEF)**: How often a threat agent will act against an asset
            - **Vulnerability**: The probability that a threat event will become a loss event
            
            ### 2. Loss Magnitude (LM)
            How much loss is likely to result? This includes:
            
            - **Primary Loss**: Direct loss from the event (response costs, replacement costs, etc.)
            - **Secondary Loss**: Indirect loss from the event (reputation damage, regulatory fines, etc.)
            
            ## Benefits of FAIR
            
            - Provides a consistent, quantitative approach to risk analysis
            - Facilitates better communication of risk to stakeholders, especially executives
            - Enables cost-benefit analysis of security controls
            - Supports better prioritization of risk mitigation efforts
            - Allows for comparison of different risk scenarios
            
            ## Limitations of FAIR
            
            - Requires more data and expertise than qualitative methods
            - Can create a false sense of precision if inputs are not carefully considered
            - May not capture all nuances of complex risk scenarios
            """,
            "image": None,
            "references": [
                "FAIR Institute (https://www.fairinstitute.org/)",
                "Measuring and Managing Information Risk: A FAIR Approach by Jack Freund and Jack Jones",
                "Open Group Standard: Open FAIR"
            ]
        },
        
        "Monte Carlo Simulation": {
            "title": "Monte Carlo Simulation in Risk Analysis",
            "content": """
            ## What is Monte Carlo Simulation?
            
            Monte Carlo simulation is a mathematical technique that uses random sampling and statistical modeling 
            to estimate the probability of different outcomes in a process that cannot easily be predicted due to 
            the intervention of random variables.
            
            ## How Monte Carlo Simulation Works in Risk Analysis
            
            1. **Define the model**: Identify the key variables and their relationships
            2. **Specify input distributions**: For each variable, define a range and probability distribution
            3. **Run simulations**: Generate random samples from each input distribution and calculate outcomes
            4. **Analyze results**: Examine the distribution of outcomes to understand the range of possible results
            
            ## Benefits in Cybersecurity Risk Assessment
            
            - **Handles uncertainty**: Incorporates the inherent uncertainty in risk parameters
            - **Produces distributions**: Shows the full range of possible outcomes, not just point estimates
            - **Enables probability statements**: Allows statements like "there is a 90% chance that losses will not exceed $X"
            - **Sensitivity analysis**: Helps identify which input parameters have the greatest impact on outcomes
            
            ## Practical Application in FAIR Analysis
            
            In a FAIR-based risk analysis, Monte Carlo simulation is used to:
            
            1. Sample from the distributions for Threat Event Frequency (TEF) and Vulnerability to calculate Loss Event Frequency (LEF)
            2. Sample from the distributions for various loss factors to calculate Loss Magnitude (LM)
            3. Combine these to calculate the overall risk in terms of Annual Loss Expectancy (ALE)
            4. Generate insights like Value at Risk (VaR) at different confidence levels
            
            ## Interpreting Monte Carlo Results
            
            - **Median (50th percentile)**: The "most likely" outcome
            - **90th/95th percentiles**: Often used for risk planning (Value at Risk)
            - **Mean**: The long-term average expected loss
            - **Standard deviation**: Indicates the volatility or uncertainty in the estimate
            """,
            "image": None,
            "references": [
                "Risk Analysis: A Quantitative Guide by David Vose",
                "Simulation Modeling and Analysis by Averill Law",
                "Monte Carlo methods in financial engineering by Paul Glasserman"
            ]
        },
        
        "GRC Fundamentals": {
            "title": "Governance, Risk, and Compliance (GRC) Fundamentals",
            "content": """
            ## What is GRC?
            
            Governance, Risk, and Compliance (GRC) is an integrated approach to organizational management that 
            aligns activities related to corporate governance, enterprise risk management, and regulatory compliance.
            
            ## Key Components of GRC
            
            ### Governance
            
            Governance ensures that organizational activities, like managing IT systems, are aligned in a way that 
            supports the organization's business goals. It includes:
            
            - Leadership and organizational structures
            - Strategic planning and decision-making processes
            - Policies and standards
            - Management oversight
            
            ### Risk Management
            
            Risk management is the process of identifying, assessing, and controlling threats to an organization's 
            capital, earnings, and operations. These threats or risks could stem from a wide variety of sources, including:
            
            - Cybersecurity incidents
            - Legal liabilities
            - Strategic management errors
            - Financial uncertainties
            - Natural disasters
            
            ### Compliance
            
            Compliance refers to the process of ensuring that an organization follows relevant laws, regulations, 
            and standards. This includes:
            
            - Industry regulations (HIPAA, PCI DSS, GDPR, etc.)
            - Legal requirements
            - Internal policies and procedures
            - Contractual obligations
            
            ## Benefits of an Integrated GRC Approach
            
            - **Reduced fragmentation**: Eliminates siloed approaches to governance, risk, and compliance
            - **Better decision-making**: Provides a holistic view for more informed decisions
            - **Cost efficiency**: Reduces duplicative activities and streamlines processes
            - **Improved business performance**: Aligns GRC activities with business objectives
            - **Enhanced risk visibility**: Provides a comprehensive view of organizational risk
            
            ## GRC Implementation Best Practices
            
            1. **Establish a GRC framework**: Choose or develop a framework that aligns with your organization's needs
            2. **Secure executive sponsorship**: Ensure leadership support and commitment
            3. **Define clear roles and responsibilities**: Clarify who is responsible for what across the organization
            4. **Implement appropriate technology**: Select tools that support your GRC processes
            5. **Develop metrics and reporting**: Establish how GRC performance will be measured and reported
            6. **Continuously improve**: Review and refine your GRC program regularly
            """,
            "image": None,
            "references": [
                "OCEG GRC Capability Model",
                "COBIT Framework by ISACA",
                "ISO 31000 Risk Management",
                "NIST Cybersecurity Framework"
            ]
        },
        
        "Risk Quantification Methods": {
            "title": "Cybersecurity Risk Quantification Methods",
            "content": """
            ## Why Quantify Cybersecurity Risk?
            
            Traditional qualitative approaches to risk assessment (using ratings like "high/medium/low") have limitations:
            
            - Subjective interpretations
            - Difficult to prioritize across different risk types
            - Cannot easily justify security investments in financial terms
            - Challenging to communicate effectively with executive leadership
            
            Quantitative risk assessment addresses these issues by expressing risk in monetary terms.
            
            ## Common Risk Quantification Methods
            
            ### Factor Analysis of Information Risk (FAIR)
            
            - Structured model for breaking down risk into component factors
            - Focuses on Loss Event Frequency and Loss Magnitude
            - Uses probability distributions rather than point estimates
            - Enables Monte Carlo simulation to model uncertainty
            
            ### NIST SSERM (Special Publication 800-30)
            
            - Provides a framework for conducting risk assessments of federal information systems
            - Considers threats, vulnerabilities, likelihood, and impact
            - Can be adapted for quantitative analysis
            
            ### Annualized Loss Expectancy (ALE)
            
            - A more traditional approach: ALE = Annual Rate of Occurrence × Single Loss Expectancy
            - Simpler but less sophisticated than FAIR
            - Limited ability to handle uncertainty and ranges
            
            ### Cyber Value-at-Risk (CVaR)
            
            - Adapted from financial VaR models
            - Estimates the maximum potential loss within a specified confidence interval
            - Considers asset value, threat vulnerability, and threat probability
            
            ## Challenges in Risk Quantification
            
            - **Data availability**: Limited historical data for cyber events
            - **Estimation uncertainty**: Difficult to precisely estimate probability and impact
            - **Expert bias**: Subject matter experts may have cognitive biases
            - **Model limitations**: All models are simplifications of reality
            
            ## Best Practices for Effective Risk Quantification
            
            1. **Use ranges instead of point estimates**: Acknowledge uncertainty in your inputs
            2. **Leverage multiple data sources**: Combine internal data, external data, and expert opinion
            3. **Document assumptions**: Clearly record the basis for all estimates
            4. **Perform sensitivity analysis**: Understand which inputs have the greatest effect on results
            5. **Update regularly**: Risk analysis should be an ongoing process, not a one-time exercise
            6. **Focus on decision-making**: The goal is better decisions, not perfect estimates
            """,
            "image": None,
            "references": [
                "How to Measure Anything in Cybersecurity Risk by Douglas W. Hubbard and Richard Seiersen",
                "Measuring and Managing Information Risk: A FAIR Approach by Jack Freund and Jack Jones",
                "NIST Special Publication 800-30: Guide for Conducting Risk Assessments",
                "World Economic Forum Cyber Value-at-Risk Framework"
            ]
        }
    }
    
    return resources
