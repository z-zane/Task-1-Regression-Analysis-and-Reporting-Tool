# Technical Note: Regression Analysis and Reporting Tool

## Overview

The **Regression Analysis and Reporting Tool** is a web-based application that enables researchers to conduct statistical regression analysis without requiring programming knowledge. Built with Streamlit and statsmodels, it provides an intuitive interface for uploading data, selecting variables, fitting regression models, and exporting publication-ready results.

## What Does the Tool Do?

The tool automates the workflow from raw data to statistical analysis and exportable results. Users can:

1. **Upload and explore data** - Import datasets (CSV, Excel) and review data quality
2. **Detect variable types** - Automatically classify variables as continuous, categorical, or binary with user override capability
3. **Select variables** - Choose dependent and independent variables for analysis
4. **Fit regression models** - Run OLS (Ordinary Least Squares) or Logistic regression with automatic model suggestion
5. **View results** - Display regression tables with coefficients, standard errors, p-values, and confidence intervals
6. **Generate visualizations** - Create coefficient plots with confidence intervals and diagnostic plots
7. **Export outputs** - Save regression tables (CSV/Excel) and figures (PNG) for use in reports and papers

The entire workflow is guided through a 5-page interface requiring no programming expertise.

## Data Requirements

**Input Format:**
- CSV (comma-separated values) or Excel (.xlsx, .xls) files
- Data should be in tabular format with variables as columns and observations as rows
- First row should contain variable names

**Variable Requirements:**
- **Dependent variable:** Should be numeric (continuous for OLS, binary 0/1 for Logit)
- **Independent variables:** Should be numeric; categorical variables with >2 categories should be pre-encoded as numeric
- **Sample size:** Minimum ~30 observations; recommended 15-20+ observations per predictor
- **Missing data:** Any missing values (NA, empty cells) will be handled via complete-case analysis

**Quality Considerations:**
- Remove ID columns, names, and other non-analytical variables
- Ensure proper encoding of categorical variables (0/1 for binary, 1/2/3 for ordered categories)
- Check for data entry errors and extreme outliers

## Outputs Produced

**1. Regression Results Table**
- Variable names
- Coefficients (estimated effects)
- Standard errors (uncertainty measures)
- Test statistics (t-values for OLS, z-values for Logit)
- P-values (significance levels)
- 95% Confidence intervals
- Significance indicators (*, **, ***, +)

**2. Model Statistics**
- **OLS specific:** R² (variance explained), Adjusted R², F-statistic with p-value, AIC, BIC, RMSE
- **Logit specific:** Pseudo R² (McFadden's), Log-Likelihood, AIC, BIC
- Sample size (observations analyzed and dropped)

**3. Visualizations**
- **Coefficient plot:** Displays coefficients with 95% confidence intervals; helps identify significant effects
- **Diagnostic plots (OLS only):** Residuals plot and distribution; assess model assumptions
- **Predicted vs. Actual:** Comparison of model predictions to observed values

**4. Export Formats**
- CSV tables (universal compatibility)
- Excel workbooks (formatted for presentation)
- PNG images at 300 DPI (publication-ready)

## Result Interpretation

**Coefficients:**
- **OLS:** One-unit increase in predictor X is associated with [coefficient] unit change in outcome Y
- **Logit:** One-unit increase in X is associated with [coefficient] change in log-odds of outcome; multiply by e for odds ratio

**Significance:**
- P-value < 0.05 indicates statistical significance at the 5% level
- Confidence intervals not crossing zero indicate significant effects
- Significance stars (*, **, ***) follow standard conventions

**Model Fit:**
- **R² (OLS):** Higher is better; 0.3 = 30% variance explained
- **Pseudo R² (Logit):** Generally lower values than OLS; use for model comparison not absolute fit
- **AIC/BIC:** Lower values indicate better model fit; useful for comparing competing models

**Effect Size:**
- Small effect: Coefficient/OR ≈ 0.1-0.2 units or 10-20% change
- Medium effect: Coefficient/OR ≈ 0.5 units or 50% change
- Large effect: Coefficient/OR ≈ 1.0+ units or >100% change

## Model Assumptions

**OLS (Ordinary Least Squares) Regression:**
1. **Linearity:** Relationship between X and Y is linear
2. **Independence:** Observations are independent (no clustering, time-series correlation)
3. **Homoscedasticity:** Constant error variance across all X values
4. **Normality:** Residuals approximately follow normal distribution (less critical with large samples)
5. **No multicollinearity:** Predictors not highly correlated (>0.8)
6. **Correct specification:** No serious omitted variable bias

**Logistic Regression:**
1. **Binary outcome:** Dependent variable must have exactly 2 unique values
2. **Independence:** Observations are independent
3. **Log-odds linearity:** Linear relationship between X and log-odds of Y
4. **No perfect multicollinearity:** Predictors not perfectly correlated
5. **Adequate sample size:** At least 10-15 observations per predictor

## Main Limitations

1. **Missing Data Handling:** Uses complete-case analysis only; rows with any missing values are dropped. Suitable only when missingness is <10% and missing completely at random (MCAR).

2. **Categorical Variables:** Requires manual encoding before import. No automatic dummy variable creation. Unordered categories should not be treated as continuous without justification.

3. **Limited Model Types:** Offers only OLS and Logit. Does not support Poisson regression, negative binomial, Tobit, or other specialized models.

4. **No Interaction Terms:** Users must create interaction terms manually before importing. Automatic interaction detection not available.

5. **Sample Size:** No power analysis or sample size calculations; user responsible for ensuring adequate sample.

6. **Causality:** Regression identifies associations only. Cannot establish causation without proper research design (randomization, natural experiments, etc.).

7. **Assumption Checking:** Limited automatic diagnostics. Users must manually assess violations (e.g., multicollinearity via VIF, normality via Q-Q plots).

8. **Outliers:** Sensitive to extreme values. No automatic outlier detection or robust regression options.

## Future Improvements

With additional development time, the following enhancements would be valuable:

1. **Multiple Imputation:** Replace complete-case analysis with multiple imputation for better handling of missing data
2. **Automatic Dummy Variables:** Create dummy variables for categorical predictors automatically
3. **Additional Models:** Add Poisson, negative binomial, Tobit, and other regression types
4. **Interaction Builder:** UI tool to specify and create interaction terms
5. **Advanced Diagnostics:** VIF calculation, multicollinearity assessment, Breusch-Pagan test for heteroscedasticity, normality tests
6. **Robust Regression:** Huber-M and other robust estimation methods for outlier-resistant inference
7. **Model Comparison:** Tools for comparing competing models (AIC/BIC comparison, nested F-test)
8. **Survey Weighting:** Support for survey-weighted analysis and design effects
9. **Panel Data:** Models for repeated measures and longitudinal data
10. **Batch Analysis:** Process multiple datasets or specifications in batch mode
11. **API Integration:** Programmatic access for automation
12. **Mobile Optimization:** Responsive design for tablet/mobile use

## Conclusion

The Regression Analysis and Reporting Tool makes regression analysis accessible to non-programmers while maintaining statistical rigor. By automating data validation, model fitting, and result formatting, it reduces barriers to entry for applied research. The tool is best suited for exploratory analysis, quick model comparison, and producing presentation-ready results in academic and applied settings. Researchers should remain aware of the model assumptions and limitations, particularly regarding causality inference and missing data handling.

---

**Technical Specifications:**
- **Language:** Python 3.8+
- **Framework:** Streamlit 1.28.1
- **Statistics:** statsmodels 0.14.0
- **Data:** pandas 2.0.3, numpy 1.24.3
- **Visualization:** matplotlib 3.7.2, seaborn 0.12.2
- **License:** MIT (open-source)
- **Repository:** [To be filled with GitHub link]

**Word Count:** 1,047 words
