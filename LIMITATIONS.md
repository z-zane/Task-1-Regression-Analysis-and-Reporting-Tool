# Regression Analysis Tool: Assumptions and Limitations

## Model Specification and Assumptions

### OLS Regression (Ordinary Least Squares)

**When to use:**
- Continuous dependent variables (e.g., income, test scores, distance)
- Count data with reasonable variation
- Any linear prediction problem

**Key Assumptions:**

1. **Linearity**: The relationship between X and Y is linear
   - Check: Scatter plots, fitted vs residuals plot
   - Violation: May need polynomial terms or transformations

2. **Independence of Observations**: Each observation is independent
   - Check: Data collection process
   - Violation: May need panel/time-series methods (not in this tool)

3. **Homoscedasticity**: Constant error variance across X values
   - Check: Residuals plot should show random scatter
   - Violation: May need weighted regression or robust standard errors

4. **Normality of Residuals**: Errors approximately follow normal distribution
   - Check: Histogram of residuals, Q-Q plot
   - Violation: May need transformations or robust regression (large samples often okay)

5. **No Perfect Multicollinearity**: Predictors not perfectly correlated
   - Check: Correlation matrix (not provided in this tool; do separately)
   - Violation: Drop redundant variables

6. **Correct Specification**: Important variables included, no serious omitted variable bias
   - Check: Literature review, theory
   - Violation: Include relevant variables

**Interpretation:**
- **Coefficient (β)**: One unit increase in X associated with β unit change in Y (holding other variables constant)
- **R²**: Proportion of variance in Y explained by the model (0-1)
- **p-value**: Probability of observing this coefficient if true effect is zero; p<0.05 typically significant

**Limitations:**
- Assumes mean is the relevant center (may not be for skewed data)
- Predictions can fall outside reasonable ranges (e.g., negative income)
- Sensitive to outliers

### Logistic Regression

**When to use:**
- Binary dependent variables (yes/no, success/failure, presence/absence)
- Two-category outcomes
- Probability prediction problems

**Requirements:**
- Dependent variable must have exactly 2 unique values
- Typically coded as 0 and 1 (though any two values work)

**Key Assumptions:**

1. **Binary Outcome**: Y ∈ {0, 1}
   - Check: Before analysis
   - Violation: Tool will reject the model

2. **Independence of Observations**: Each observation is independent
   - Check: Data collection process
   - Violation: May need multilevel or GEE models (not in this tool)

3. **Linearity in Log-Odds**: Logit(P) = β₀ + β₁X₁ + β₂X₂ + ...
   - Check: Box-Tidwell test (not in tool)
   - Violation: May need interaction terms or polynomial terms

4. **No Perfect Multicollinearity**: Predictors not perfectly correlated
   - Check: Correlation matrix
   - Violation: Drop redundant variables

5. **Correct Specification**: Important variables included
   - Check: Literature review, theory
   - Violation: Include relevant variables

**Interpretation:**
- **Coefficient (β)**: One unit increase in X is associated with β change in log-odds of Y=1
- **Odds Ratio (exp(β))**: One unit increase in X multiplies the odds of Y=1 by exp(β)
- **Pseudo R²**: McFadden's R² (similar to R² for OLS but different interpretation; generally lower values)
- **p-value**: Probability of observing this coefficient if true effect is zero

**Example:** If coefficient for "Male" is 0.405, odds ratio is 1.50. Being male is associated with 50% higher odds of outcome.

**Limitations:**
- Assumes logistic functional form (may not always be true)
- Sensitive to separation (perfect prediction for one group)
- Requires sufficient sample size per predictor (rule of thumb: 10-15 obs/predictor)

## Data Handling and Preprocessing

### Missing Data

**This Tool's Approach:**
- Complete-case analysis: Drops any row with missing values in analysis variables
- Transparent reporting: Shows how many observations dropped

**Advantages:**
- Simple, reproducible, unbiased (under MCAR assumption)

**Disadvantages:**
- Loss of information if missingness is extensive
- Potential bias if data not MCAR (Missing Completely At Random)

**When problematic:**
- >10% of data missing
- Missing data systematically related to outcome
- Missing data related to unobserved confounders

**Alternatives not in this tool:**
- Multiple imputation
- Maximum likelihood estimation with missing data
- Sensitivity analysis

### Categorical Variables

**Current Handling:**
- Treated as numeric (dummy coding assumed not done)
- If ordinal (1,2,3,...), treated as continuous

**Recommendations:**
- Binary variables (0/1): Use directly
- Ordered categories (1-5 satisfaction): Treat as continuous or collapse categories
- Unordered categories: Manually create dummy variables before importing

**Potential Issues:**
- Unordered categories treated as continuous assumes ordering
- More than 10 categories may indicate need for recoding

## Sample Size and Power

### Minimum Sample Size Guidelines

**Rule of Thumb (Peduzzi et al., 1996):**
- Minimum N = 10 × number of predictors
- Recommended N = 15-20 × number of predictors

**Examples:**
- 3 predictors: Minimum 30, recommended 45-60
- 5 predictors: Minimum 50, recommended 75-100
- 10 predictors: Minimum 100, recommended 150-200

### Consequences of Small Samples
- Wide confidence intervals
- Unstable estimates
- Type II error (fail to detect real effects)
- Model overfitting

## Generalizability and Causality

### What This Tool Does
- Estimates associations (correlations in regression form)
- Tests statistical significance
- Quantifies effect sizes

### What This Tool Does NOT Do
- Establish causation
- Prove one variable causes changes in another
- Account for selection bias or confounding

### Establishing Causality Requires
1. **Temporal precedence**: Cause occurs before effect (not always clear in cross-sectional data)
2. **Covariation**: Cause and effect related (shown by regression)
3. **No alternative explanations**: Other variables controlled (done by including controls)

**Confounding Variables:**
If X→Y relationship confounded by Z:
- Z causes X
- Z causes Y
- Without controlling Z, X coefficient biased

**Solution:** Include Z as predictor

**Unobserved Confounding:**
If unmeasured Z confounds relationship:
- Regression cannot help
- Need research design (randomization, matching, natural experiments)

## Checks You Should Do (Outside This Tool)

1. **Data Quality**
   - Outliers and extreme values
   - Coding errors and inconsistencies
   - Distribution of each variable

2. **Relationships**
   - Scatter plots between Y and each X
   - Correlation matrix
   - Evidence of nonlinearity

3. **Model Assumptions** (OLS)
   - Residual plots (Diagnostic tab provides these)
   - Normality test
   - Multicollinearity (VIF - Variance Inflation Factor)

4. **Results Robustness**
   - Run model with/without outliers
   - Run model with different subsets of predictors
   - Check sensitivity to specification

5. **Reporting Requirements**
   - Full sample size and analysis sample
   - Missing data mechanisms and amounts
   - Variable definitions and coding
   - Model specification details

## Statistical Significance vs. Practical Significance

**Statistical Significance (p < 0.05):**
- Unlikely to occur by chance (under null hypothesis)
- Influenced by sample size (larger N → easier to be significant)
- Doesn't indicate effect size or importance

**Practical Significance:**
- Does the effect size matter in real-world terms?
- Even small effects can be statistically significant with large samples
- Always examine coefficient size alongside p-values

**Example:**
- Coefficient: 0.001, p-value: 0.02 (statistically significant)
- But 1-unit increase in X → 0.001 change in Y (practically negligible?)

## Common Pitfalls and Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| All predictors insignificant but high R² | Multicollinearity | Check VIF, remove correlated variables |
| Unreasonable coefficient magnitudes | Scale differences | Standardize variables before analysis |
| Perfect separation (Logit fails) | One group perfectly predicted | Check data; may need more data or different model |
| Wide confidence intervals | Small sample size | Increase N or simplify model |
| Non-significant F-test but significant predictors | Multicollinearity | Check correlations; may reflect redundancy |
| Residuals violate normality | Outliers or transformation needed | Check residual plot; consider transformations |

## Best Practices

1. **Start simple**: Begin with fewer predictors; add complexity as justified
2. **Visualize first**: Plot data before running models
3. **Interpret coefficients**: Look at effect size, not just p-values
4. **Report everything**: Sample size, missing data, model specification
5. **Sensitivity check**: Verify results with alternative specifications
6. **Avoid p-hacking**: Pre-specify model before seeing results
7. **Think causally**: Consider confounders and alternative explanations

## References for Further Reading

- **Regression Basics:**
  - Wooldridge, J. M. (2012). *Introductory Econometrics* (5th ed.). Cengage Learning.
  - Fox, J. (2015). *Applied Regression Analysis and Generalized Linear Models* (3rd ed.). SAGE.

- **Logistic Regression:**
  - Hosmer Jr, D. W., Lemeshow, S., & Sturdivant, R. X. (2013). *Applied Logistic Regression* (3rd ed.). Wiley.

- **Assumptions:**
  - Field, A. (2013). *Discovering Statistics Using IBM SPSS Statistics* (4th ed.). SAGE.

- **Causal Inference:**
  - Angrist, J. D., & Pischke, J. S. (2008). *Mostly Harmless Econometrics*. Princeton University Press.

---

**Version 1.0 | Last Updated 2024**

*This document provides guidance on appropriate use of the Regression Analysis Tool. Users are responsible for understanding the assumptions underlying their analysis and for correct interpretation of results.*
