"""
Regression models module.
Implements OLS and Logistic regression using statsmodels.
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols, logit
from typing import Dict, Tuple, List
import warnings


class RegressionModel:
    """Base class for regression models."""
    
    def __init__(self, data: pd.DataFrame, dep_var: str, indep_vars: List[str]):
        """
        Initialize regression model.
        
        Args:
            data: DataFrame with analysis data
            dep_var: Dependent variable name
            indep_vars: List of independent variable names
        """
        self.data = data
        self.dep_var = dep_var
        self.indep_vars = indep_vars
        self.result = None
        self.n_obs = len(data)
    
    def get_results_table(self) -> pd.DataFrame:
        """Get regression results as DataFrame."""
        if self.result is None:
            return None
        
        # Extract summary table
        summary_table = self.result.summary().tables[1]
        results_df = pd.DataFrame(summary_table.data[1:], columns=summary_table.data[0])
        
        return results_df
    
    def get_model_stats(self) -> Dict:
        """Get model fit statistics."""
        if self.result is None:
            return {}
        
        stats = {
            'n_obs': self.result.nobs,
            'df_resid': self.result.df_resid,
        }
        
        # Model-specific stats will be added by subclasses
        return stats


class OLSModel(RegressionModel):
    """Ordinary Least Squares regression."""
    
    def fit(self) -> bool:
        """Fit OLS model."""
        try:
            # Prepare formula
            formula = f'{self.dep_var} ~ {" + ".join(self.indep_vars)}'
            
            # Fit model
            self.result = ols(formula, data=self.data).fit()
            return True
        except Exception as e:
            raise ValueError(f"Error fitting OLS model: {str(e)}")
    
    def get_model_stats(self) -> Dict:
        """Get OLS-specific statistics."""
        stats = super().get_model_stats()
        
        if self.result is not None:
            stats.update({
                'r_squared': round(self.result.rsquared, 4),
                'adj_r_squared': round(self.result.rsquared_adj, 4),
                'f_statistic': round(self.result.fvalue, 4),
                'f_pvalue': self.result.f_pvalue,
                'aic': round(self.result.aic, 2),
                'bic': round(self.result.bic, 2),
                'rmse': round(np.sqrt(self.result.mse_resid), 4),
            })
        
        return stats
    
    def get_coefficients_ci(self, alpha: float = 0.05) -> pd.DataFrame:
        """Get coefficients with confidence intervals."""
        if self.result is None:
            return None
        
        conf_int = self.result.conf_int(alpha=alpha)
        
        coef_df = pd.DataFrame({
            'Variable': self.result.params.index,
            'Coefficient': self.result.params.values,
            'Std Error': self.result.bse.values,
            't-statistic': self.result.tvalues.values,
            'p-value': self.result.pvalues.values,
            'CI Lower': conf_int[0].values,
            'CI Upper': conf_int[1].values,
        })
        
        # Add significance stars
        coef_df['Sig'] = coef_df['p-value'].apply(self._get_significance)
        
        return coef_df
    
    @staticmethod
    def _get_significance(p_val):
        """Get significance stars based on p-value."""
        if p_val < 0.001:
            return '***'
        elif p_val < 0.01:
            return '**'
        elif p_val < 0.05:
            return '*'
        elif p_val < 0.1:
            return '+'
        else:
            return ''


class LogitModel(RegressionModel):
    """Logistic regression model."""
    
    def fit(self) -> bool:
        """Fit logit model."""
        try:
            # Check dependent variable
            unique_vals = self.data[self.dep_var].unique()
            if len(unique_vals) != 2:
                raise ValueError(
                    f"Logit requires binary dependent variable. "
                    f"Found {len(unique_vals)} unique values."
                )
            
            # Prepare formula
            formula = f'{self.dep_var} ~ {" + ".join(self.indep_vars)}'
            
            # Fit model
            self.result = logit(formula, data=self.data).fit(disp=0)
            return True
        except Exception as e:
            raise ValueError(f"Error fitting Logit model: {str(e)}")
    
    def get_model_stats(self) -> Dict:
        """Get Logit-specific statistics."""
        stats = super().get_model_stats()
        
        if self.result is not None:
            stats.update({
                'pseudo_r_squared': round(self.result.prsquared, 4),
                'log_likelihood': round(self.result.llf, 2),
                'aic': round(self.result.aic, 2),
                'bic': round(self.result.bic, 2),
                'll_null': round(self.result.llnull, 2),
                'll_model': round(self.result.llf, 2),
            })
        
        return stats
    
    def get_coefficients_ci(self, alpha: float = 0.05) -> pd.DataFrame:
        """Get coefficients with confidence intervals."""
        if self.result is None:
            return None
        
        conf_int = self.result.conf_int(alpha=alpha)
        
        coef_df = pd.DataFrame({
            'Variable': self.result.params.index,
            'Coefficient': self.result.params.values,
            'Std Error': self.result.bse.values,
            'z-statistic': self.result.tvalues.values,
            'p-value': self.result.pvalues.values,
            'CI Lower': conf_int[0].values,
            'CI Upper': conf_int[1].values,
        })
        
        # Add significance stars
        coef_df['Sig'] = coef_df['p-value'].apply(self._get_significance)
        
        # Calculate odds ratios
        coef_df['Odds Ratio'] = np.exp(coef_df['Coefficient'])
        
        return coef_df
    
    @staticmethod
    def _get_significance(p_val):
        """Get significance stars based on p-value."""
        if p_val < 0.001:
            return '***'
        elif p_val < 0.01:
            return '**'
        elif p_val < 0.05:
            return '*'
        elif p_val < 0.1:
            return '+'
        else:
            return ''


def suggest_model(dep_var_type: str) -> str:
    """Suggest appropriate model based on dependent variable type."""
    if dep_var_type == 'binary':
        return 'logit'
    elif dep_var_type in ['continuous', 'categorical']:
        return 'ols'
    else:
        return 'ols'  # default
