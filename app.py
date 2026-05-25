"""
Regression Analysis and Reporting Tool
A Streamlit application for conducting regression analysis and generating publication-ready outputs.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

from data_handler import DataHandler
from regression_models import OLSModel, LogitModel, suggest_model
from visualization import RegressionVisualizer, save_figure
from export_results import ResultsExporter

# Page configuration
st.set_page_config(
    page_title="Regression Analysis Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_handler' not in st.session_state:
    st.session_state.data_handler = DataHandler()
if 'var_types' not in st.session_state:
    st.session_state.var_types = {}
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'model' not in st.session_state:
    st.session_state.model = None
if 'model_type' not in st.session_state:
    st.session_state.model_type = None

# Title
st.markdown('<div class="main-header">📊 Regression Analysis and Reporting Tool</div>',
            unsafe_allow_html=True)
st.markdown("""
This tool allows you to upload a dataset, select variables, run regression models (OLS and Logit),
and generate publication-ready results tables and figures.
""")

# Sidebar
with st.sidebar:
    st.markdown("### 📋 Navigation")
    page = st.radio("Select a page:", 
                    ["1. Data Upload", "2. Data Exploration", "3. Analysis Setup", 
                     "4. Model Estimation", "5. Results & Export"])

# ============================================================================
# PAGE 1: DATA UPLOAD
# ============================================================================
if page == "1. Data Upload":
    st.markdown('<div class="section-header">📁 Upload Your Dataset</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Upload Data File")
        st.markdown("Supported formats: CSV, Excel (.xlsx, .xls)")
        
        uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                st.session_state.data_handler.load_data(uploaded_file)
                st.success("✅ Data loaded successfully!")
                
                # Show basic info
                data = st.session_state.data_handler.get_data()
                st.write(f"**Dataset dimensions:** {data.shape[0]} rows × {data.shape[1]} columns")
                st.write(f"**Variables:** {', '.join(data.columns[:5])}{'...' if len(data.columns) > 5 else ''}")
                
            except Exception as e:
                st.error(f"❌ Error loading data: {str(e)}")
    
    with col2:
        st.markdown("#### Demo Dataset")
        if st.button("📥 Load Demo Dataset"):
            try:
                demo_file = "demo_data.csv"
                st.session_state.data_handler.original_data = pd.read_csv(demo_file)
                st.session_state.data_handler.data = st.session_state.data_handler.original_data.copy()
                st.session_state.data_handler._update_info()
                st.success("✅ Demo dataset loaded!")
                
                data = st.session_state.data_handler.get_data()
                st.write(f"**Dataset dimensions:** {data.shape[0]} rows × {data.shape[1]} columns")
                st.write(f"**Variables:** {', '.join(data.columns)}")
            except Exception as e:
                st.error(f"❌ Error loading demo: {str(e)}")
    
    if st.session_state.data_handler.get_data() is not None:
        st.markdown("---")
        st.markdown("#### Data Preview")
        data = st.session_state.data_handler.get_data()
        st.dataframe(data.head(10), use_container_width=True)

# ============================================================================
# PAGE 2: DATA EXPLORATION
# ============================================================================
elif page == "2. Data Exploration":
    st.markdown('<div class="section-header">🔍 Data Exploration & Quality Check</div>', unsafe_allow_html=True)
    
    if st.session_state.data_handler.get_data() is None:
        st.warning("⚠️ Please upload a dataset first (go to Page 1)")
    else:
        data = st.session_state.data_handler.get_data()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Observations", len(data))
        col2.metric("Total Variables", len(data.columns))
        col3.metric("Missing Data Points", data.isnull().sum().sum())
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["Summary Statistics", "Missing Data", "Data Preview"])
        
        with tab1:
            st.markdown("#### Descriptive Statistics")
            summary_stats = st.session_state.data_handler.get_summary_stats()
            st.dataframe(summary_stats, use_container_width=True)
        
        with tab2:
            st.markdown("#### Missing Data Report")
            missing_report = st.session_state.data_handler.get_missing_data_report()
            if missing_report is not None:
                st.markdown('<div class="warning-box">⚠️ Missing data detected. These observations will be dropped during analysis.</div>',
                           unsafe_allow_html=True)
                st.dataframe(missing_report, use_container_width=True)
            else:
                st.markdown('<div class="success-box">✅ No missing data detected</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown("#### Full Data Preview")
            st.dataframe(data, use_container_width=True)

# ============================================================================
# PAGE 3: ANALYSIS SETUP
# ============================================================================
elif page == "3. Analysis Setup":
    st.markdown('<div class="section-header">⚙️ Setup Variables for Analysis</div>', unsafe_allow_html=True)
    
    if st.session_state.data_handler.get_data() is None:
        st.warning("⚠️ Please upload a dataset first (go to Page 1)")
    else:
        data = st.session_state.data_handler.get_data()
        
        # Detect variable types
        st.markdown("#### Variable Type Detection")
        st.info("The system automatically detects variable types. Review and adjust if needed.")
        
        var_types = st.session_state.data_handler.detect_variable_types()
        st.session_state.var_types = var_types
        
        # Display and allow editing of variable types
        col_names = list(data.columns)
        col1, col2, col3 = st.columns(3)
        
        var_type_editor = {}
        for i, var in enumerate(col_names):
            if i % 3 == 0:
                col = col1
            elif i % 3 == 1:
                col = col2
            else:
                col = col3
            
            with col:
                detected = var_types.get(var, 'unknown')
                var_type_editor[var] = st.selectbox(
                    f"**{var}**",
                    ['continuous', 'categorical', 'binary', 'unknown'],
                    index=['continuous', 'categorical', 'binary', 'unknown'].index(detected)
                )
        
        st.session_state.var_types = var_type_editor
        
        # Variable selection
        st.markdown("---")
        st.markdown("#### Select Variables for Regression")
        
        # Suggest dependent and independent variables
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Dependent Variable (Y)**")
            dep_var = st.selectbox(
                "Choose dependent variable",
                col_names,
                key="dep_var_select"
            )
        
        with col2:
            st.markdown("**Independent Variables (X)**")
            indep_vars = st.multiselect(
                "Choose independent variables",
                [v for v in col_names if v != dep_var],
                key="indep_var_select"
            )
        
        if dep_var and indep_vars:
            # Store selections
            st.session_state.dep_var = dep_var
            st.session_state.indep_vars = indep_vars
            
            # Suggest model
            dep_type = st.session_state.var_types.get(dep_var, 'continuous')
            suggested_model = suggest_model(dep_type)
            
            st.markdown(f"""
            ##### Model Suggestion
            - **Dependent Variable:** {dep_var} ({dep_type})
            - **Number of Predictors:** {len(indep_vars)}
            - **Suggested Model:** {suggested_model.upper()}
            """)
            
            # Store suggestion
            st.session_state.suggested_model = suggested_model
            
            st.success("✅ Setup complete! Proceed to Page 4 to estimate the model.")

# ============================================================================
# PAGE 4: MODEL ESTIMATION
# ============================================================================
elif page == "4. Model Estimation":
    st.markdown('<div class="section-header">🔬 Estimate Regression Model</div>', unsafe_allow_html=True)
    
    if 'dep_var' not in st.session_state or 'indep_vars' not in st.session_state:
        st.warning("⚠️ Please complete variable selection first (go to Page 3)")
    else:
        data = st.session_state.data_handler.get_data()
        
        try:
            # Prepare data
            clean_data, n_dropped = st.session_state.data_handler.prepare_for_regression(
                st.session_state.dep_var,
                st.session_state.indep_vars
            )
            
            if n_dropped > 0:
                st.markdown(f'<div class="warning-box">⚠️ {n_dropped} observations dropped due to missing values</div>',
                           unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Observations analyzed:** {len(clean_data)}")
                st.markdown(f"**Observations dropped:** {n_dropped}")
            
            with col2:
                st.markdown(f"**Dependent variable:** {st.session_state.dep_var}")
                st.markdown(f"**Predictors:** {', '.join(st.session_state.indep_vars[:3])}{'...' if len(st.session_state.indep_vars) > 3 else ''}")
            
            # Model selection
            st.markdown("---")
            st.markdown("#### Choose Model Type")
            
            model_choice = st.radio(
                "Select regression model:",
                ["OLS Regression", "Logistic Regression"],
                index=0 if st.session_state.suggested_model == 'ols' else 1
            )
            
            st.session_state.model_type = 'ols' if model_choice == "OLS Regression" else 'logit'
            
            # Fit model button
            if st.button("🚀 Estimate Model", key="fit_button", use_container_width=True):
                with st.spinner("Estimating model..."):
                    try:
                        if st.session_state.model_type == 'ols':
                            model = OLSModel(
                                clean_data,
                                st.session_state.dep_var,
                                st.session_state.indep_vars
                            )
                        else:
                            model = LogitModel(
                                clean_data,
                                st.session_state.dep_var,
                                st.session_state.indep_vars
                            )
                        
                        model.fit()
                        st.session_state.model = model
                        st.session_state.n_obs_dropped = n_dropped
                        st.session_state.analysis_done = True
                        
                        st.success("✅ Model estimated successfully!")
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"❌ Error fitting model: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ Error preparing data: {str(e)}")

# ============================================================================
# PAGE 5: RESULTS & EXPORT
# ============================================================================
elif page == "5. Results & Export":
    st.markdown('<div class="section-header">📊 Results and Export</div>', unsafe_allow_html=True)
    
    if not st.session_state.analysis_done or st.session_state.model is None:
        st.warning("⚠️ Please estimate a model first (go to Page 4)")
    else:
        model = st.session_state.model
        
        # Get results
        coef_df = model.get_coefficients_ci()
        model_stats = model.get_model_stats()
        
        tab1, tab2, tab3, tab4 = st.tabs(["Regression Table", "Coefficient Plot", 
                                          "Diagnostics", "Download Results"])
        
        # Tab 1: Results Table
        with tab1:
            st.markdown("#### Regression Results")
            
            # Format results
            exporter = ResultsExporter()
            formatted_table = exporter.format_results_table(
                coef_df, model_stats,
                st.session_state.model_type.upper()
            )
            
            st.dataframe(formatted_table, use_container_width=True)
            
            st.markdown("---")
            st.markdown("#### Model Statistics")
            
            col1, col2, col3 = st.columns(3)
            
            col1.metric("N (Observations)", model_stats.get('n_obs', 'N/A'))
            col1.metric("N (Dropped)", st.session_state.n_obs_dropped)
            
            if st.session_state.model_type == 'ols':
                col2.metric("R²", f"{model_stats.get('r_squared', 'N/A'):.4f}")
                col2.metric("Adj. R²", f"{model_stats.get('adj_r_squared', 'N/A'):.4f}")
                col3.metric("F-statistic", f"{model_stats.get('f_statistic', 'N/A'):.4f}")
                col3.metric("RMSE", f"{model_stats.get('rmse', 'N/A'):.4f}")
            else:
                col2.metric("Pseudo R²", f"{model_stats.get('pseudo_r_squared', 'N/A'):.4f}")
                col2.metric("Log-Likelihood", f"{model_stats.get('ll_model', 'N/A'):.2f}")
                col3.metric("AIC", f"{model_stats.get('aic', 'N/A'):.2f}")
                col3.metric("BIC", f"{model_stats.get('bic', 'N/A'):.2f}")
        
        # Tab 2: Coefficient Plot
        with tab2:
            st.markdown("#### Coefficient Plot with 95% Confidence Intervals")
            
            try:
                visualizer = RegressionVisualizer()
                fig = visualizer.plot_coefficients(
                    coef_df,
                    model_name=f"{st.session_state.model_type.upper()} Model"
                )
                st.pyplot(fig, use_container_width=True)
                
                # Save button
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Save Coefficient Plot", key="save_coef_plot"):
                        save_figure(fig, "coefficient_plot.png")
                        st.success("Saved as coefficient_plot.png")
            
            except Exception as e:
                st.error(f"Error generating plot: {str(e)}")
        
        # Tab 3: Diagnostics
        with tab3:
            st.markdown("#### Model Diagnostics")
            
            try:
                if st.session_state.model_type == 'ols':
                    visualizer = RegressionVisualizer()
                    residuals = st.session_state.model.result.resid
                    fig = visualizer.plot_residuals(
                        residuals,
                        model_name="OLS Model"
                    )
                    st.pyplot(fig, use_container_width=True)
                    
                    # Summary statistics of residuals
                    st.markdown("##### Residual Statistics")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Mean", f"{residuals.mean():.4f}")
                    col2.metric("Std Dev", f"{residuals.std():.4f}")
                    col3.metric("Min", f"{residuals.min():.4f}")
                    col4.metric("Max", f"{residuals.max():.4f}")
                else:
                    st.info("Diagnostic plots are primarily for OLS models. Logit diagnostics available on request.")
            
            except Exception as e:
                st.error(f"Error generating diagnostics: {str(e)}")
        
        # Tab 4: Download Results
        with tab4:
            st.markdown("#### Export Results")
            
            # Export options
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Export Table")
                
                exporter = ResultsExporter()
                full_table = exporter.add_model_info(
                    formatted_table,
                    model_stats,
                    st.session_state.n_obs_dropped,
                    st.session_state.model_type.upper()
                )
                
                # CSV export
                csv = full_table.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name=f"regression_results_{st.session_state.model_type}.csv",
                    mime="text/csv"
                )
                
                # Excel export
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    full_table.to_excel(writer, index=False, sheet_name='Results')
                    
                    # Add model info sheet
                    info_df = pd.DataFrame({
                        'Metric': ['Model Type', 'Dependent Variable', 'N Observations', 
                                  'N Dropped', 'Independent Variables'],
                        'Value': [st.session_state.model_type.upper(),
                                 st.session_state.dep_var,
                                 model_stats.get('n_obs', 'N/A'),
                                 st.session_state.n_obs_dropped,
                                 ', '.join(st.session_state.indep_vars)]
                    })
                    info_df.to_excel(writer, index=False, sheet_name='Model Info')
                
                buffer.seek(0)
                st.download_button(
                    label="📊 Download as Excel",
                    data=buffer,
                    file_name=f"regression_results_{st.session_state.model_type}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col2:
                st.markdown("##### Export Plot")
                
                try:
                    visualizer = RegressionVisualizer()
                    fig = visualizer.plot_coefficients(coef_df)
                    
                    # Save as PNG
                    img_buffer = BytesIO()
                    fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
                    img_buffer.seek(0)
                    
                    st.download_button(
                        label="📈 Download Coefficient Plot (PNG)",
                        data=img_buffer,
                        file_name="coefficient_plot.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"Error generating plot: {str(e)}")

st.markdown("---")
st.markdown("""
### 📚 Help & Documentation
- **Minimum Requirements:** Python 3.8+, Streamlit 1.0+
- **Data Format:** CSV or Excel with numeric and categorical variables
- **OLS Model:** For continuous or count dependent variables
- **Logit Model:** For binary (0/1) dependent variables
- **Assumptions:** No perfect multicollinearity, proper variable specification
- **Missing Data:** Automatically dropped from analysis (shown transparently)

For questions or issues, check the README file or source code documentation.
""")
