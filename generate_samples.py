"""
Script to generate sample outputs for demonstration.
Run this to create sample regression table and plots.
"""
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend

# Import modules
from data_handler import DataHandler
from regression_models import OLSModel, LogitModel
from visualization import RegressionVisualizer, save_figure
from export_results import ResultsExporter

def generate_samples():
    """Generate sample outputs using demo dataset."""
    
    print("=" * 60)
    print("SAMPLE OUTPUT GENERATION")
    print("=" * 60)
    
    # Load demo data
    print("\n1. Loading demo dataset...")
    handler = DataHandler()
    try:
        with open('demo_data.csv') as f:
            handler.load_data(f)
        data = handler.get_data()
        print(f"   ✓ Loaded {len(data)} observations")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Sample 1: OLS Regression - Annual Income Prediction
    print("\n2. Estimating OLS Model (Annual Income)...")
    try:
        dep_var = 'Annual_Income'
        indep_vars = ['Years_Education', 'Work_Experience', 'Employment_Status', 'Age']
        
        clean_data, n_dropped = handler.prepare_for_regression(dep_var, indep_vars)
        print(f"   ✓ Using {len(clean_data)} observations ({n_dropped} dropped)")
        
        # Fit model
        ols_model = OLSModel(clean_data, dep_var, indep_vars)
        ols_model.fit()
        
        # Get results
        coef_df = ols_model.get_coefficients_ci()
        model_stats = ols_model.get_model_stats()
        
        print(f"   ✓ Model fit successfully")
        print(f"   ✓ R² = {model_stats['r_squared']:.4f}")
        print(f"   ✓ F-statistic = {model_stats['f_statistic']:.4f} (p < 0.001)")
        
        # Save results table
        print("\n3. Saving OLS Results Table...")
        exporter = ResultsExporter()
        formatted_table = exporter.format_results_table(coef_df, model_stats, 'OLS')
        full_table = exporter.add_model_info(formatted_table, model_stats, n_dropped, 'OLS', dep_var)
        
        full_table.to_csv('sample_ols_regression_table.csv', index=False)
        print("   ✓ Saved: sample_ols_regression_table.csv")
        print("\nOLS Regression Results:")
        print(formatted_table.to_string(index=False))
        
        # Save coefficient plot
        print("\n4. Generating OLS Coefficient Plot...")
        visualizer = RegressionVisualizer()
        fig = visualizer.plot_coefficients(coef_df, model_name='OLS: Annual Income Prediction')
        save_figure(fig, 'sample_ols_coefficient_plot.png')
        print("   ✓ Saved: sample_ols_coefficient_plot.png")
        
        # Save residual plot
        print("\n5. Generating OLS Diagnostic Plot...")
        residuals = ols_model.result.resid
        fig = visualizer.plot_residuals(residuals, model_name='OLS: Annual Income')
        save_figure(fig, 'sample_ols_diagnostic_plot.png')
        print("   ✓ Saved: sample_ols_diagnostic_plot.png")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Sample 2: Logit Regression - Higher Education Prediction
    print("\n" + "=" * 60)
    print("6. Estimating Logit Model (Higher Education)...")
    try:
        dep_var = 'Higher_Education'
        indep_vars = ['Age', 'Gender', 'Work_Experience', 'Employment_Status']
        
        clean_data, n_dropped = handler.prepare_for_regression(dep_var, indep_vars)
        print(f"   ✓ Using {len(clean_data)} observations ({n_dropped} dropped)")
        
        # Fit model
        logit_model = LogitModel(clean_data, dep_var, indep_vars)
        logit_model.fit()
        
        # Get results
        coef_df = logit_model.get_coefficients_ci()
        model_stats = logit_model.get_model_stats()
        
        print(f"   ✓ Model fit successfully")
        print(f"   ✓ Pseudo R² = {model_stats['pseudo_r_squared']:.4f}")
        print(f"   ✓ Log-Likelihood = {model_stats['ll_model']:.2f}")
        
        # Save results table
        print("\n7. Saving Logit Results Table...")
        exporter = ResultsExporter()
        formatted_table = exporter.format_results_table(coef_df, model_stats, 'Logit')
        full_table = exporter.add_model_info(formatted_table, model_stats, n_dropped, 'Logit', dep_var)
        
        full_table.to_csv('sample_logit_regression_table.csv', index=False)
        print("   ✓ Saved: sample_logit_regression_table.csv")
        print("\nLogit Regression Results:")
        print(formatted_table.to_string(index=False))
        
        # Save coefficient plot
        print("\n8. Generating Logit Coefficient Plot...")
        visualizer = RegressionVisualizer()
        fig = visualizer.plot_coefficients(coef_df, model_name='Logit: Higher Education Prediction')
        save_figure(fig, 'sample_logit_coefficient_plot.png')
        print("   ✓ Saved: sample_logit_coefficient_plot.png")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✓ SAMPLE OUTPUTS GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print("\nGenerated Files:")
    print("  - sample_ols_regression_table.csv")
    print("  - sample_ols_coefficient_plot.png")
    print("  - sample_ols_diagnostic_plot.png")
    print("  - sample_logit_regression_table.csv")
    print("  - sample_logit_coefficient_plot.png")
    print("\nThese files demonstrate the tool's output format.")
    print("=" * 60)

if __name__ == '__main__':
    generate_samples()
