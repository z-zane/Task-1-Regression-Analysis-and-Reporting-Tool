"""
Data handling module for regression analysis tool.
Handles data upload, validation, and exploration.
"""
import pandas as pd
import numpy as np
from typing import Tuple, Dict, List


class DataHandler:
    """Handle data loading, validation, and exploration."""
    
    def __init__(self):
        self.data = None
        self.original_data = None
        self.data_info = {}
    
    def load_data(self, file) -> bool:
        """Load data from uploaded file (CSV or Excel)."""
        try:
            if file.name.endswith('.csv'):
                self.data = pd.read_csv(file)
            elif file.name.endswith(('.xlsx', '.xls')):
                self.data = pd.read_excel(file)
            else:
                raise ValueError("File must be CSV or Excel format")
            
            self.original_data = self.data.copy()
            self._update_info()
            return True
        except Exception as e:
            raise ValueError(f"Error loading file: {str(e)}")
    
    def _update_info(self):
        """Update data information."""
        if self.data is not None:
            self.data_info = {
                'n_rows': len(self.data),
                'n_cols': len(self.data.columns),
                'columns': list(self.data.columns),
                'dtypes': self.data.dtypes.to_dict(),
                'missing': self.data.isnull().sum().to_dict(),
            }
    
    def get_summary_stats(self) -> pd.DataFrame:
        """Get descriptive statistics."""
        if self.data is None:
            return None
        return self.data.describe().T
    
    def get_missing_data_report(self) -> pd.DataFrame:
        """Get missing data report."""
        if self.data is None:
            return None
        
        missing_counts = self.data.isnull().sum()
        missing_pct = (missing_counts / len(self.data) * 100).round(2)
        
        report = pd.DataFrame({
            'Variable': missing_counts.index,
            'Missing Count': missing_counts.values,
            'Missing %': missing_pct.values
        })
        
        report = report[report['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
        return report if len(report) > 0 else None
    
    def detect_variable_types(self) -> Dict[str, str]:
        """
        Automatically detect variable types.
        Returns dict with variable names as keys and types as values.
        Types: 'continuous', 'categorical', 'binary'
        """
        if self.data is None:
            return {}
        
        var_types = {}
        
        for col in self.data.columns:
            # Skip columns with all missing values
            if self.data[col].isnull().all():
                var_types[col] = 'unknown'
                continue
            
            # Check if numeric
            if pd.api.types.is_numeric_dtype(self.data[col]):
                unique_vals = self.data[col].nunique()
                
                # Binary if only 2 unique non-null values
                if unique_vals == 2:
                    var_types[col] = 'binary'
                # Continuous if many unique values
                elif unique_vals > 10:
                    var_types[col] = 'continuous'
                # Categorical if few unique values
                else:
                    var_types[col] = 'categorical'
            else:
                # Non-numeric - categorical
                unique_vals = self.data[col].nunique()
                if unique_vals == 2:
                    var_types[col] = 'binary'
                else:
                    var_types[col] = 'categorical'
        
        return var_types
    
    def get_variable_info(self, var_name: str, detected_type: str) -> Dict:
        """Get detailed information about a variable."""
        if self.data is None or var_name not in self.data.columns:
            return {}
        
        col = self.data[var_name]
        info = {
            'name': var_name,
            'detected_type': detected_type,
            'missing_count': col.isnull().sum(),
            'missing_pct': round(col.isnull().sum() / len(self.data) * 100, 2)
        }
        
        if detected_type in ['continuous', 'binary']:
            info['numeric'] = True
            info['min'] = col.min()
            info['max'] = col.max()
            info['mean'] = col.mean()
            info['std'] = col.std()
        else:
            info['numeric'] = False
            info['unique_values'] = col.nunique()
            info['unique_list'] = col.unique().tolist()[:10]
        
        return info
    
    def prepare_for_regression(self, dep_var: str, indep_vars: List[str]) -> Tuple[pd.DataFrame, int]:
        """
        Prepare data for regression: drop missing values, keep relevant columns.
        Returns clean dataset and number of observations removed.
        """
        if self.data is None:
            raise ValueError("No data loaded")
        
        all_vars = [dep_var] + indep_vars
        subset = self.data[all_vars].copy()
        
        n_original = len(subset)
        subset = subset.dropna()
        n_removed = n_original - len(subset)
        
        return subset, n_removed
    
    def get_data(self) -> pd.DataFrame:
        """Get current data."""
        return self.data
    
    def get_original_data(self) -> pd.DataFrame:
        """Get original loaded data."""
        return self.original_data
