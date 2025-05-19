import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import streamlit as st
from typing import Dict, List, Tuple

def plot_loss_distribution(simulation_results: pd.DataFrame, bin_count: int = 50) -> go.Figure:
    """
    Create a histogram of the Annual Loss Expectancy (ALE) distribution.
    
    Args:
        simulation_results: DataFrame containing the simulation results
        bin_count: Number of bins to use in the histogram
        
    Returns:
        Plotly figure object
    """
    # Create histogram
    fig = px.histogram(
        simulation_results, 
        x="ALE", 
        nbins=bin_count,
        histnorm='probability density',
        title="Annual Loss Expectancy (ALE) Distribution",
        labels={"ALE": "Annual Loss Expectancy ($)"},
        color_discrete_sequence=['#0066cc']
    )
    
    # Add vertical lines for key percentiles
    percentiles = [0.5, 0.9, 0.95]
    colors = ['green', 'orange', 'red']
    names = ['50% (Median)', '90th Percentile', '95th Percentile']
    
    for percentile, color, name in zip(percentiles, colors, names):
        value = simulation_results['ALE'].quantile(percentile)
        fig.add_vline(
            x=value, 
            line_dash="dash", 
            line_color=color,
            annotation_text=f"{name}: ${value:,.2f}",
            annotation_position="top right"
        )
    
    # Customize layout
    fig.update_layout(
        xaxis_title="Annual Loss Expectancy ($)",
        yaxis_title="Probability Density",
        legend_title="Percentiles",
        height=500
    )
    
    return fig

def plot_cumulative_distribution(simulation_results: pd.DataFrame) -> go.Figure:
    """
    Create a cumulative distribution function (CDF) plot for the ALE.
    
    Args:
        simulation_results: DataFrame containing the simulation results
        
    Returns:
        Plotly figure object
    """
    # Sort the ALE values and compute the empirical CDF
    ale_sorted = np.sort(simulation_results['ALE'].values)
    cdf = np.arange(1, len(ale_sorted) + 1) / len(ale_sorted)
    
    # Create the CDF plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ale_sorted,
        y=cdf,
        mode='lines',
        name='CDF',
        line=dict(color='#0066cc')
    ))
    
    # Add vertical lines for key percentiles
    percentiles = [0.5, 0.9, 0.95]
    colors = ['green', 'orange', 'red']
    names = ['50% (Median)', '90th Percentile', '95th Percentile']
    
    for percentile, color, name in zip(percentiles, colors, names):
        value = simulation_results['ALE'].quantile(percentile)
        fig.add_vline(
            x=value, 
            line_dash="dash", 
            line_color=color,
            annotation_text=f"{name}: ${value:,.2f}",
            annotation_position="top right"
        )
    
    # Customize layout
    fig.update_layout(
        title="Cumulative Distribution Function of Annual Loss Expectancy",
        xaxis_title="Annual Loss Expectancy ($)",
        yaxis_title="Cumulative Probability",
        height=500
    )
    
    return fig

def plot_heat_map(simulation_results: pd.DataFrame, x_column: str, y_column: str) -> go.Figure:
    """
    Create a heat map showing the relationship between two variables.
    
    Args:
        simulation_results: DataFrame containing the simulation results
        x_column: Column name for the x-axis
        y_column: Column name for the y-axis
        
    Returns:
        Plotly figure object
    """
    # Create bins for the x and y columns
    x_bins = pd.cut(simulation_results[x_column], bins=20)
    y_bins = pd.cut(simulation_results[y_column], bins=20)
    
    # Create a cross-tabulation of the binned data
    heatmap_data = pd.crosstab(y_bins, x_bins, normalize=True)
    
    # Convert to a format suitable for Plotly heatmap
    heatmap_x = [str(interval) for interval in heatmap_data.columns]
    heatmap_y = [str(interval) for interval in heatmap_data.index]
    
    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_x,
        y=heatmap_y,
        colorscale='Blues',
        colorbar=dict(title='Probability Density')
    ))
    
    # Customize layout
    fig.update_layout(
        title=f"Relationship Between {x_column} and {y_column}",
        xaxis_title=x_column,
        yaxis_title=y_column,
        height=500
    )
    
    return fig

def plot_sensitivity_analysis(simulation_results: pd.DataFrame) -> go.Figure:
    """
    Create a tornado chart showing the sensitivity of ALE to input parameters.
    
    Args:
        simulation_results: DataFrame containing the simulation results
        
    Returns:
        Plotly figure object
    """
    # Calculate correlation between input parameters and ALE
    correlations = {}
    input_params = ['TEF', 'Vulnerability', 'Loss Magnitude']
    
    for param in input_params:
        correlations[param] = np.corrcoef(simulation_results[param], simulation_results['ALE'])[0, 1]
    
    # Sort parameters by absolute correlation
    sorted_params = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
    
    # Create the tornado chart
    fig = go.Figure()
    
    # Add the bars
    for param, corr in sorted_params:
        fig.add_trace(go.Bar(
            y=[param],
            x=[corr],
            orientation='h',
            name=param,
            marker=dict(
                color='blue' if corr >= 0 else 'red',
                line=dict(color='black', width=1)
            )
        ))
    
    # Customize layout
    fig.update_layout(
        title="Sensitivity Analysis: Correlation with Annual Loss Expectancy",
        xaxis_title="Correlation Coefficient",
        yaxis_title="Input Parameter",
        height=400,
        showlegend=False
    )
    
    return fig

def create_boxplot_comparison(simulation_results: List[pd.DataFrame], labels: List[str]) -> go.Figure:
    """
    Create a box plot comparing ALE distributions for multiple scenarios.
    
    Args:
        simulation_results: List of DataFrames containing simulation results for each scenario
        labels: List of scenario names
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    for i, (results, label) in enumerate(zip(simulation_results, labels)):
        fig.add_trace(go.Box(
            y=results['ALE'],
            name=label,
            boxmean=True,  # adds a marker for the mean
            marker_color=px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
        ))
    
    # Customize layout
    fig.update_layout(
        title="Comparison of Annual Loss Expectancy Across Scenarios",
        yaxis_title="Annual Loss Expectancy ($)",
        height=500,
        boxmode='group'
    )
    
    return fig

def format_currency(value: float) -> str:
    """Format a value as a currency string with commas and 2 decimal places"""
    return f"${value:,.2f}"

def plot_loss_exceedance_curve(simulation_results: pd.DataFrame) -> go.Figure:
    """
    Create a loss exceedance curve, showing the probability of exceeding a certain loss.
    
    Args:
        simulation_results: DataFrame containing the simulation results
        
    Returns:
        Plotly figure object
    """
    # Sort the ALE values
    ale_sorted = np.sort(simulation_results['ALE'].values)
    
    # Calculate the exceedance probability (1 - CDF)
    exceedance_prob = 1 - (np.arange(1, len(ale_sorted) + 1) / len(ale_sorted))
    
    # Create the exceedance curve
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ale_sorted,
        y=exceedance_prob,
        mode='lines',
        name='Exceedance Probability',
        line=dict(color='#cc0000')
    ))
    
    # Add horizontal lines for key probabilities
    probabilities = [0.5, 0.1, 0.05]
    colors = ['green', 'orange', 'red']
    names = ['50% Chance', '10% Chance', '5% Chance']
    
    for prob, color, name in zip(probabilities, colors, names):
        # Find the loss value at this exceedance probability
        idx = (np.abs(exceedance_prob - prob)).argmin()
        value = ale_sorted[idx]
        
        fig.add_hline(
            y=prob, 
            line_dash="dash", 
            line_color=color,
            annotation_text=f"{name} of exceeding ${value:,.2f}",
            annotation_position="left"
        )
    
    # Customize layout
    fig.update_layout(
        title="Loss Exceedance Curve",
        xaxis_title="Annual Loss Expectancy ($)",
        yaxis_title="Probability of Loss Exceeding X",
        height=500,
        yaxis=dict(type='log')  # Use logarithmic scale for better visualization
    )
    
    return fig
