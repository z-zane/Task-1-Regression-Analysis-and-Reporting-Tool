# Regression Analysis and Reporting Tool

A user-friendly Streamlit application for conducting regression analysis and generating publication-ready research outputs.

## Features

✅ **Data Upload**: Support for CSV and Excel formats
✅ **Data Exploration**: Automatic data quality checks and missing data reporting
✅ **Variable Type Detection**: Automatic detection of continuous, categorical, and binary variables
✅ **Regression Models**: OLS and Logistic regression using statsmodels
✅ **Publication-Ready Tables**: Clean, professional regression results tables
✅ **Statistical Visualizations**: Coefficient plots with confidence intervals, residual diagnostics
✅ **Export Options**: CSV, Excel, and PNG format export
✅ **Non-Programmer Friendly**: Intuitive web interface, no coding required

## Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download this repository**
   ```bash
   cd regression_tool
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Quick Start Guide

### Step 1: Data Upload (Page 1)
- Click **"Upload a file"** to select a CSV or Excel file
- Alternatively, click **"Load Demo Dataset"** to use the included sample data
- The tool will display basic dataset information

### Step 2: Data Exploration (Page 2)
- Review summary statistics for all variables
- Check for missing data patterns
- Examine data types and distributions

### Step 3: Setup Variables (Page 3)
- Review automatically detected variable types
- Adjust variable types if needed (continuous, categorical, binary)
- Select your dependent variable (Y)
- Select your independent variables (X)
- The tool will suggest an appropriate model

### Step 4: Model Estimation (Page 4)
- Review sample size and missing data information
- Choose between OLS or Logistic regression
- Click **"Estimate Model"** to run the analysis
- Wait for confirmation that the model has been estimated

### Step 5: Results & Export (Page 5)
- **Regression Table**: View coefficients, standard errors, and p-values
- **Coefficient Plot**: Visual representation of coefficients with 95% confidence intervals
- **Diagnostics**: Residual plots and model assumptions
- **Download Results**: Export tables as CSV/Excel and plots as PNG

## Demo Dataset Description

The included `demo_data.csv` contains a simulated survey dataset with:

**Variables:**
- `Years_Education`: Years of formal education (continuous)
- `Age`: Age in years (continuous)
- `Work_Experience`: Years of work experience (continuous)
- `Gender`: 0 = Female, 1 = Male (binary)
- `Employment_Status`: 0 = Unemployed, 1 = Employed (binary)
- `Years_Current_Job`: Years in current position (continuous)
- `Job_Satisfaction`: 1-5 satisfaction rating (ordinal/categorical)
- `Annual_Income`: Annual income in dollars (continuous, ~5% missing)
- `Higher_Education`: 0 = No, 1 = Yes college degree (binary)

**Sample Size:** 200 observations

**Sample Analysis:**
- **OLS Model**: Predict `Annual_Income` from education, experience, and employment status
- **Logit Model**: Predict `Higher_Education` attainment from age, gender, and work experience

## Understanding the Output

### Regression Table
- **Coefficient**: The estimated effect of the predictor on the outcome
- **Std Error**: Standard error of the estimate (uncertainty)
- **t-stat / z-stat**: Test statistic (coefficient / SE)
- **p-value**: Statistical significance (*** p<0.001, ** p<0.01, * p<0.05, + p<0.1)
- **95% CI**: Confidence interval for the coefficient
- **Odds Ratio** (Logit only): Multiplicative effect on odds

### Model Statistics

**For OLS:**
- **R²**: Proportion of variance explained (0-1, higher is better)
- **Adj. R²**: R² adjusted for number of predictors
- **F-statistic**: Overall model significance
- **RMSE**: Root Mean Squared Error (prediction error)

**For Logit:**
- **Pseudo R²**: McFadden's pseudo-R² (0-1, higher is better)
- **Log-Likelihood**: Model fit measure
- **AIC/BIC**: Information criteria for model comparison

### Coefficient Plot
- Points show coefficient estimates
- Error bars show 95% confidence intervals
- Red dashed line at 0 indicates no effect
- Coefficients not crossing 0 are statistically significant at p<0.05

## Model Assumptions and Limitations

### OLS Regression Assumptions
1. **Linearity**: Relationship between variables is linear
2. **Independence**: Observations are independent
3. **Homoscedasticity**: Error variance is constant across values of predictors
4. **Normality**: Residuals are approximately normally distributed
5. **No Multicollinearity**: Predictors are not highly correlated

### Logistic Regression Assumptions
1. **Binary Outcome**: Dependent variable must have exactly 2 unique values
2. **Independence**: Observations are independent
3. **No Perfect Multicollinearity**: Predictors should not be perfectly correlated
4. **Linearity in Log-Odds**: Relationship is linear on the log-odds scale

### Data Requirements
- **Minimum observations**: 10-15 observations per predictor (rule of thumb)
- **Missing data**: Handled by complete-case analysis (rows with any missing values dropped)
- **Variable types**: Categorical variables with >10 categories should be recoded

### Limitations
1. **Missing Data**: Tool uses complete-case analysis; rows with any missing values are excluded
2. **Categorical Variables**: Currently treated as numeric; ordinal encoding assumed
3. **Non-linear Relationships**: Both models assume linearity (in original or log-odds scale)
4. **Sample Selection**: Tool assumes your sample is representative
5. **Specification**: Results depend on correct variable selection and specification
6. **Causality**: Regression identifies associations, not causation

## Troubleshooting

### "Error loading file"
- Ensure file is in CSV or Excel format
- Check that file has no encoding issues
- Try CSV format first

### "Logit requires binary dependent variable"
- Logit only works with outcomes having exactly 2 unique values
- Use OLS for continuous or ordinal outcomes
- Or recode your outcome to binary (0/1)

### "No coefficients to plot"
- This should not occur; report as a bug

### Missing data warnings
- This is normal; the tool automatically handles missing values
- Check "Data Exploration" page to see how many observations were affected

## File Structure

```
regression_tool/
├── app.py                    # Main Streamlit application
├── data_handler.py          # Data loading and validation
├── regression_models.py     # OLS and Logit model classes
├── visualization.py         # Figure generation
├── export_results.py        # Export functionality
├── requirements.txt         # Python dependencies
├── demo_data.csv           # Sample dataset
├── README.md               # This file
└── LIMITATIONS.md          # Detailed assumptions and limitations
```

## Requirements File

```
streamlit==1.28.1
pandas==2.0.3
numpy==1.24.3
statsmodels==0.14.0
scipy==1.11.1
matplotlib==3.7.2
seaborn==0.12.2
openpyxl==3.1.2
```

## Citation

If you use this tool in your research, please cite the underlying packages:

**Statsmodels**: Seabold, S., & Perktold, A. (2010). Statsmodels: Econometric and statistical modeling with Python. In *Proceedings of the 9th Python in Science Conference* (Vol. 57, p. 61).

**Streamlit**: Heres, G., Prabhu, R., & Ramachandran, R. (2019). Streamlit: A simple way to create customizable web apps for machine learning and data science.

**Pandas**: McKinney, W. (2010). Data structures for statistical computing in Python. In *Proceedings of the 9th Python in Science Conference* (Vol. 445, pp. 51-56).

## Version

Version 1.0  
Last Updated: 2024

## License

This tool is provided as-is for educational and research purposes.

## Support

For issues, questions, or feature requests, please check:
1. README.md (this file)
2. LIMITATIONS.md (assumptions and limitations)
3. Inline code documentation in the .py files

---

**Happy analyzing!** 📊
