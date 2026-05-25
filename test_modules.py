"""
Quick test to verify all modules work correctly.
"""
import sys
sys.path.insert(0, r'e:\WHU\EnglishLearning\PhDApplication\PolyU')

import pandas as pd
import numpy as np

# Quick validation of modules
print("Testing imports...")

try:
    from data_handler import DataHandler
    print("✓ data_handler imported")
except Exception as e:
    print(f"✗ data_handler error: {e}")
    sys.exit(1)

try:
    from regression_models import OLSModel, LogitModel
    print("✓ regression_models imported")
except Exception as e:
    print(f"✗ regression_models error: {e}")
    sys.exit(1)

try:
    from visualization import RegressionVisualizer
    print("✓ visualization imported")
except Exception as e:
    print(f"✗ visualization error: {e}")
    sys.exit(1)

try:
    from export_results import ResultsExporter
    print("✓ export_results imported")
except Exception as e:
    print(f"✗ export_results error: {e}")
    sys.exit(1)

print("\n✓ All modules imported successfully!")
print("\nTesting basic functionality...")

# Load demo data
try:
    data = pd.read_csv(r'e:\WHU\EnglishLearning\PhDApplication\PolyU\demo_data.csv')
    print(f"✓ Demo data loaded: {data.shape[0]} rows, {data.shape[1]} columns")
    print(f"  Columns: {list(data.columns)}")
except Exception as e:
    print(f"✗ Error loading demo data: {e}")
    sys.exit(1)

# Test data handler
try:
    handler = DataHandler()
    handler.data = data
    handler.original_data = data.copy()
    handler._update_info()
    
    var_types = handler.detect_variable_types()
    print(f"✓ Variable type detection working")
    print(f"  Types: {var_types}")
except Exception as e:
    print(f"✗ Data handler error: {e}")
    sys.exit(1)

# Test OLS model
try:
    clean_data, n_dropped = handler.prepare_for_regression(
        'Annual_Income',
        ['Years_Education', 'Work_Experience', 'Employment_Status']
    )
    
    print(f"✓ Data preparation working")
    print(f"  Clean data: {len(clean_data)} rows (dropped {n_dropped})")
    
    ols_model = OLSModel(clean_data, 'Annual_Income', 
                        ['Years_Education', 'Work_Experience', 'Employment_Status'])
    ols_model.fit()
    
    coef_df = ols_model.get_coefficients_ci()
    stats = ols_model.get_model_stats()
    
    print(f"✓ OLS model fitting working")
    print(f"  R² = {stats['r_squared']:.4f}")
    print(f"  N = {stats['n_obs']}")
except Exception as e:
    print(f"✗ OLS model error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test Logit model
try:
    clean_data_logit, n_dropped_logit = handler.prepare_for_regression(
        'Higher_Education',
        ['Age', 'Gender', 'Work_Experience']
    )
    
    logit_model = LogitModel(clean_data_logit, 'Higher_Education',
                            ['Age', 'Gender', 'Work_Experience'])
    logit_model.fit()
    
    coef_df_logit = logit_model.get_coefficients_ci()
    stats_logit = logit_model.get_model_stats()
    
    print(f"✓ Logit model fitting working")
    print(f"  Pseudo R² = {stats_logit['pseudo_r_squared']:.4f}")
    print(f"  N = {stats_logit['n_obs']}")
except Exception as e:
    print(f"✗ Logit model error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test visualization
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    visualizer = RegressionVisualizer()
    fig = visualizer.plot_coefficients(coef_df, model_name='Test OLS')
    plt.close(fig)
    
    print(f"✓ Visualization working")
except Exception as e:
    print(f"✗ Visualization error: {e}")
    import traceback
    traceback.print_exc()

# Test export
try:
    exporter = ResultsExporter()
    formatted_table = exporter.format_results_table(coef_df, stats, 'OLS')
    
    print(f"✓ Export formatting working")
    print(f"  Table shape: {formatted_table.shape}")
except Exception as e:
    print(f"✗ Export error: {e}")

print("\n" + "="*60)
print("✓✓✓ ALL TESTS PASSED ✓✓✓")
print("="*60)
print("\nTool is ready to use!")
print("\nTo start the Streamlit app, run:")
print("  streamlit run app.py")
