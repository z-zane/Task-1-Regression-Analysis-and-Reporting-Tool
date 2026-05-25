"""
Export module for regression results.
Handles exporting results to various formats.
"""
import pandas as pd
import numpy as np
from typing import Dict, List
import io


class ResultsExporter:
    """Export regression results to various formats."""
    
    @staticmethod
    def format_results_table(coef_df: pd.DataFrame, model_stats: Dict,
                            model_type: str = 'OLS') -> pd.DataFrame:
        """
        Format results table for publication.
        
        Args:
            coef_df: Coefficient DataFrame
            model_stats: Model statistics dictionary
            model_type: Type of model ('OLS' or 'Logit')
        
        Returns:
            Formatted DataFrame
        """
        formatted_df = pd.DataFrame()
        
        formatted_df['Variable'] = coef_df['Variable']
        formatted_df['Coefficient'] = coef_df['Coefficient'].round(4)
        formatted_df['Std Error'] = coef_df['Std Error'].round(4)
        
        if model_type == 'OLS':
            formatted_df['t-stat'] = coef_df['t-statistic'].round(3)
        else:  # Logit
            formatted_df['z-stat'] = coef_df['z-statistic'].round(3)
        
        formatted_df['p-value'] = coef_df['p-value'].apply(lambda x: f"{x:.4f}")
        formatted_df['Sig'] = coef_df['Sig']
        
        if model_type == 'Logit':
            formatted_df['Odds Ratio'] = coef_df['Odds Ratio'].round(4)
        
        return formatted_df
    
    @staticmethod
    def add_model_info(results_table: pd.DataFrame, model_stats: Dict,
                      n_obs_dropped: int, model_type: str = 'OLS',
                      dep_var: str = '') -> pd.DataFrame:
        """
        Add model information footer to results table.
        
        Args:
            results_table: Results DataFrame
            model_stats: Model statistics
            n_obs_dropped: Number of observations dropped due to missing values
            model_type: Type of model
            dep_var: Dependent variable name
        
        Returns:
            DataFrame with model info
        """
        # Create info rows
        info_rows = []
        
        info_rows.append({
            'Variable': 'Model Statistics',
            'Coefficient': '',
            'Std Error': '',
            't-stat' if model_type == 'OLS' else 'z-stat': '',
            'p-value': '',
            'Sig': ''
        })
        
        info_rows.append({
            'Variable': f'N (analyzed)',
            'Coefficient': model_stats.get('n_obs', 'N/A'),
            'Std Error': '',
            't-stat' if model_type == 'OLS' else 'z-stat': '',
            'p-value': '',
            'Sig': ''
        })
        
        info_rows.append({
            'Variable': f'N (dropped due to missing)',
            'Coefficient': n_obs_dropped,
            'Std Error': '',
            't-stat' if model_type == 'OLS' else 'z-stat': '',
            'p-value': '',
            'Sig': ''
        })
        
        if model_type == 'OLS':
            info_rows.append({
                'Variable': f'R²',
                'Coefficient': model_stats.get('r_squared', 'N/A'),
                'Std Error': '',
                't-stat': '',
                'p-value': '',
                'Sig': ''
            })
            
            info_rows.append({
                'Variable': f'Adj. R²',
                'Coefficient': model_stats.get('adj_r_squared', 'N/A'),
                'Std Error': '',
                't-stat': '',
                'p-value': '',
                'Sig': ''
            })
            
            if model_stats.get('f_pvalue'):
                info_rows.append({
                    'Variable': f'F-stat (p-value)',
                    'Coefficient': f"{model_stats.get('f_statistic', 'N/A')} ({model_stats.get('f_pvalue', 'N/A'):.4f})",
                    'Std Error': '',
                    't-stat': '',
                    'p-value': '',
                    'Sig': ''
                })
        else:  # Logit
            info_rows.append({
                'Variable': f'Pseudo R²',
                'Coefficient': model_stats.get('pseudo_r_squared', 'N/A'),
                'Std Error': '',
                'z-stat': '',
                'p-value': '',
                'Sig': ''
            })
            
            info_rows.append({
                'Variable': f'Log Likelihood',
                'Coefficient': model_stats.get('ll_model', 'N/A'),
                'Std Error': '',
                'z-stat': '',
                'p-value': '',
                'Sig': ''
            })
        
        info_rows.append({
            'Variable': f'AIC',
            'Coefficient': model_stats.get('aic', 'N/A'),
            'Std Error': '',
            't-stat' if model_type == 'OLS' else 'z-stat': '',
            'p-value': '',
            'Sig': ''
        })
        
        info_rows.append({
            'Variable': f'BIC',
            'Coefficient': model_stats.get('bic', 'N/A'),
            'Std Error': '',
            't-stat' if model_type == 'OLS' else 'z-stat': '',
            'p-value': '',
            'Sig': ''
        })
        
        info_df = pd.DataFrame(info_rows)
        
        # Combine with results
        combined = pd.concat([results_table, info_df], ignore_index=True)
        return combined
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filepath: str):
        """Export DataFrame to CSV."""
        df.to_csv(filepath, index=False)
    
    @staticmethod
    def export_to_excel(df: pd.DataFrame, filepath: str):
        """Export DataFrame to Excel."""
        df.to_excel(filepath, index=False, sheet_name='Regression Results')
    
    @staticmethod
    def export_table_as_latex(df: pd.DataFrame) -> str:
        """Export table as LaTeX."""
        return df.to_latex(index=False)
    
    @staticmethod
    def export_table_as_html(df: pd.DataFrame) -> str:
        """Export table as HTML."""
        return df.to_html(index=False, border=0, classes='table')
