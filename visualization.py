"""
Visualization module for regression analysis.
Generates coefficient plots and predicted value plots.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional
import io


class RegressionVisualizer:
    """Generate visualizations for regression analysis."""
    
    def __init__(self, style: str = 'whitegrid'):
        """Initialize visualizer."""
        sns.set_style(style)
        self.figsize = (10, 6)
    
    def plot_coefficients(self, coef_df: pd.DataFrame, model_name: str = 'Model',
                         exclude_intercept: bool = True) -> plt.Figure:
        """
        Generate coefficient plot with confidence intervals.
        
        Args:
            coef_df: DataFrame with columns ['Variable', 'Coefficient', 'CI Lower', 'CI Upper']
            model_name: Name of model for title
            exclude_intercept: Whether to exclude intercept from plot
        
        Returns:
            matplotlib Figure object
        """
        # Prepare data
        plot_df = coef_df.copy()
        if exclude_intercept and 'Intercept' in plot_df['Variable'].values:
            plot_df = plot_df[plot_df['Variable'] != 'Intercept'].reset_index(drop=True)
        
        if len(plot_df) == 0:
            raise ValueError("No coefficients to plot")
        
        # Create plot
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Calculate error bars
        errors = [
            plot_df['Coefficient'] - plot_df['CI Lower'],
            plot_df['CI Upper'] - plot_df['Coefficient']
        ]
        
        # Plot
        ax.errorbar(plot_df['Coefficient'], range(len(plot_df)),
                   xerr=errors, fmt='o', markersize=8, capsize=5, capthick=2,
                   color='steelblue', ecolor='steelblue')
        
        # Add vertical line at x=0
        ax.axvline(x=0, color='red', linestyle='--', alpha=0.5, linewidth=1)
        
        # Formatting
        ax.set_yticks(range(len(plot_df)))
        ax.set_yticklabels(plot_df['Variable'])
        ax.set_xlabel('Coefficient Estimate', fontsize=11, fontweight='bold')
        ax.set_title(f'Regression Coefficients with 95% CI\n{model_name}',
                    fontsize=12, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_predicted_values(self, y_actual: pd.Series, y_predicted: pd.Series,
                             model_name: str = 'Model') -> plt.Figure:
        """
        Generate predicted vs actual values plot.
        
        Args:
            y_actual: Actual values
            y_predicted: Predicted values
            model_name: Name of model for title
        
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Scatter plot
        ax.scatter(y_actual, y_predicted, alpha=0.6, s=50, color='steelblue')
        
        # Perfect prediction line
        lim_min = min(y_actual.min(), y_predicted.min())
        lim_max = max(y_actual.max(), y_predicted.max())
        ax.plot([lim_min, lim_max], [lim_min, lim_max], 'r--', lw=2, label='Perfect Prediction')
        
        ax.set_xlabel('Actual Values', fontsize=11, fontweight='bold')
        ax.set_ylabel('Predicted Values', fontsize=11, fontweight='bold')
        ax.set_title(f'Predicted vs Actual Values\n{model_name}',
                    fontsize=12, fontweight='bold', pad=20)
        ax.legend()
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_residuals(self, residuals: pd.Series, model_name: str = 'Model') -> plt.Figure:
        """
        Generate residual plot.
        
        Args:
            residuals: Model residuals
            model_name: Name of model for title
        
        Returns:
            matplotlib Figure object
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Residuals vs fitted
        fitted = pd.Series(range(len(residuals)))
        axes[0].scatter(fitted, residuals, alpha=0.6, color='steelblue')
        axes[0].axhline(y=0, color='red', linestyle='--', lw=2)
        axes[0].set_xlabel('Observation Number', fontsize=10, fontweight='bold')
        axes[0].set_ylabel('Residuals', fontsize=10, fontweight='bold')
        axes[0].set_title('Residuals Plot', fontsize=11, fontweight='bold')
        axes[0].grid(alpha=0.3)
        
        # Q-Q plot approximation (histogram)
        axes[1].hist(residuals, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
        axes[1].set_xlabel('Residuals', fontsize=10, fontweight='bold')
        axes[1].set_ylabel('Frequency', fontsize=10, fontweight='bold')
        axes[1].set_title('Distribution of Residuals', fontsize=11, fontweight='bold')
        axes[1].grid(alpha=0.3, axis='y')
        
        fig.suptitle(f'Diagnostic Plots\n{model_name}', fontsize=12, fontweight='bold', y=1.00)
        plt.tight_layout()
        return fig
    
    def plot_marginal_effects(self, var_name: str, var_values: np.ndarray,
                             predicted_values: np.ndarray,
                             model_name: str = 'Model') -> plt.Figure:
        """
        Generate marginal effects plot.
        
        Args:
            var_name: Variable name
            var_values: Range of variable values
            predicted_values: Corresponding predicted values
            model_name: Name of model for title
        
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ax.plot(var_values, predicted_values, linewidth=2.5, color='steelblue', marker='o')
        ax.fill_between(var_values, predicted_values * 0.95, predicted_values * 1.05,
                       alpha=0.2, color='steelblue')
        
        ax.set_xlabel(var_name, fontsize=11, fontweight='bold')
        ax.set_ylabel('Predicted Values', fontsize=11, fontweight='bold')
        ax.set_title(f'Marginal Effect: {var_name}\n{model_name}',
                    fontsize=12, fontweight='bold', pad=20)
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        return fig


def save_figure(fig: plt.Figure, filepath: str, dpi: int = 300):
    """Save figure to file."""
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    plt.close(fig)


def get_figure_as_bytes(fig: plt.Figure) -> bytes:
    """Get figure as bytes for display in Streamlit."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    return buf.getvalue()
