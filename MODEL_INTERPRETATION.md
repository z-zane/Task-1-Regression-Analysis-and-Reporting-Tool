# Model Selection and Output Interpretation Guide

## When to Use Each Model

### OLS (Ordinary Least Squares) Regression

**Use OLS when:**
- Dependent variable is continuous (income, test scores, temperature, hours)
- Outcome can take any value within a range
- You want to predict average value of Y given X values
- Relationship appears roughly linear in scatter plots

**Examples:**
- Predicting annual income from education and experience ✓
- Predicting test scores from study hours ✓
- Predicting house prices from square footage ✓
- Predicting employee satisfaction (1-5 scale) ≈ (acceptable but ordinal regression better)

**Advantages:**
- Easy interpretation: 1 unit in X → [coefficient] units in Y
- R² directly interpretable as variance explained
- Robust with larger samples (Central Limit Theorem)
- Standard in social sciences

**Disadvantages:**
- Can predict impossible values (e.g., negative income)
- Assumes linear relationship
- Sensitive to outliers
- Constant variance assumption often violated

### Logistic Regression

**Use Logit when:**
- Dependent variable is binary (yes/no, success/failure, 0/1)
- Outcome is categorical with exactly 2 categories
- You want to predict probability of an event
- Data naturally involves "occurrence" of something

**Examples:**
- Predicting college graduation (yes/no) ✓
- Predicting loan default (yes/no) ✓
- Predicting disease diagnosis (present/absent) ✓
- Predicting voting choice (yes/no on referendum) ✓

**Advantages:**
- Outputs meaningful probabilities (0 to 1)
- Natural for binary outcomes
- Coefficients interpretable as log-odds or odds ratios
- More efficient with rare events

**Disadvantages:**
- Interpretation less intuitive (log-odds scale)
- Requires binary outcome (must be 2 values)
- Requires adequate sample for rare outcomes
- More complex model fitting

---

## Reading OLS Output

### Example: Annual Income Prediction

```
Variable            Coefficient   Std Error   t-stat    p-value   
Intercept          25430.12      3221.50     7.89      0.0000 ***
Years_Education     3125.45       245.67     12.73     0.0000 ***
Work_Experience      487.23        89.54      5.45     0.0000 ***
Employment_Status   9823.45      1245.23      7.89     0.0000 ***
Age                  145.67        34.56      4.22     0.0001 ***

Model Statistics:
R²                  0.7234
Adj. R²             0.7156
F-statistic         124.57  (p < 0.0001)
N                   190
```

### How to Interpret

**Intercept (25,430)**
- When all X variables = 0: predicted income is $25,430
- Often not meaningful (people don't have 0 years education and age)

**Years_Education Coefficient (3,125.45)***
- **Interpretation:** Each additional year of education is associated with $3,125 higher annual income
- **Confidence:** p < 0.001 (highly significant)
- **Effect size:** Substantial (adding 4 years education → ~$12,500 more income)

**Work_Experience Coefficient (487.23)***
- **Interpretation:** Each additional year of work experience associated with $487 higher income
- **Confidence:** p < 0.001 (significant)
- **Effect size:** Smaller than education but still meaningful

**Employment_Status Coefficient (9,823.45)***
- **Interpretation:** Being employed (=1 vs =0) associated with $9,823 higher income
- **Confidence:** p < 0.001 (highly significant)
- **Effect size:** Very large (unemployed → employed increases income by ~$10k)

**Age Coefficient (145.67)***
- **Interpretation:** Each additional year of age associated with $146 higher income
- **Confidence:** p < 0.001 (significant)
- **Effect size:** Small but accumulates over time

### Model Fit (R² = 0.7234)

**Meaning:** 72.34% of variation in income explained by these 4 variables
- **Interpretation:** The model explains about 3/4 of income variation
- **Assessment:** Very good fit (R² > 0.50 is good, > 0.70 is excellent)
- **Implication:** Other factors (job type, skills, location) explain remaining 28%

### F-Statistic (124.57, p < 0.0001)

**Meaning:** Overall model is highly significant
- **Interpretation:** As a group, these predictors significantly predict income
- **Test:** H₀ = all coefficients = 0; rejected
- **Action:** Model is useful for prediction

### Significance Codes

- `***` p < 0.001 (very strong evidence)
- `**`  p < 0.01 (strong evidence)
- `*`   p < 0.05 (moderate evidence)
- `+`   p < 0.10 (weak evidence)
- (blank) p ≥ 0.10 (not significant at standard levels)

---

## Reading Logit Output

### Example: Higher Education Prediction

```
Variable              Coefficient   Std Error   z-stat    p-value   Odds Ratio
Intercept            -0.8234       0.5234      -1.57     0.1157    
Age                   0.0456       0.0134       3.40     0.0007 **    1.0467
Gender                0.3421       0.2345       1.46     0.1446        1.4078
Work_Experience       0.1289       0.0456       2.83     0.0047 **    1.1374
Employment_Status     0.6723       0.2987       2.25     0.0243 *     1.9593

Model Statistics:
Pseudo R²             0.2156
Log-Likelihood       -98.34
AIC                  214.68
N                    195
```

### How to Interpret

**Understanding Log-Odds and Odds Ratios:**

The coefficient is on the **log-odds scale**, but odds ratios are easier to interpret:
- Odds = probability of event / probability of no event
- Odds Ratio = multiplicative effect on odds

**Age Coefficient (0.0456, OR = 1.0467)***
- **Interpretation (log-odds):** Each year of age increases log-odds of college degree by 0.0456
- **Interpretation (odds ratio):** Each year of age multiplies the odds of degree by 1.0467
- **Plain English:** Getting 1 year older is associated with 4.67% increase in odds of having college degree
- **Practical:** Over 10 years, this compounds: 1.0467^10 = 1.57 (57% higher odds)

**Gender Coefficient (0.3421, OR = 1.4078)**
- **Interpretation:** Being male (1) vs female (0) increases odds of degree by 40.78%
- **Assessment:** Not significant at p = 0.1446 (p > 0.05)
- **Note:** Caution in interpretation; doesn't pass conventional significance test

**Work_Experience Coefficient (0.1289, OR = 1.1374)***
- **Interpretation:** Each additional year of work experience increases odds of degree by 13.74%
- **Confidence:** p = 0.0047 (significant)
- **Practical:** 5 years experience: 1.1374^5 = 1.92 (92% higher odds)

**Employment_Status Coefficient (0.6723, OR = 1.9593)*
- **Interpretation:** Being employed increases odds of college degree by 95.93%
- **Confidence:** p = 0.0243 (significant at 5% level)
- **Practical:** Employed individuals roughly 2x more likely to have degree

### Model Fit (Pseudo R² = 0.2156)

**Meaning:** 21.56% of variation explained (lower than OLS typical values)
- **Interpretation:** Moderate fit for logit model
- **Note:** Pseudo R² not directly comparable to OLS R² (different scale)
- **Assessment:** For binary outcome, R² of 0.20-0.30 is reasonable

### When Results Are "Not Significant"

**Example: Gender (p = 0.1446)**
- p-value > 0.05, so not statistically significant
- Interpretation: We cannot confidently say gender affects education attainment
- OR = 1.41 suggests 41% higher odds for males, but this could be due to chance
- Recommendation: Exclude or note as marginally related in report

---

## Coefficient Plot Interpretation

### What the Plot Shows
- **Point (•):** Estimated coefficient value
- **Error bars (—):** 95% confidence interval
- **Red dashed line (- - -):** Zero (no effect)
- **Y-axis:** Variable names
- **X-axis:** Coefficient magnitude

### How to Read

**Coefficient Cross Red Line (includes 0)**
- Not significant at p < 0.05
- Could be zero effect or measurement error
- Wider confidence interval = less precision

**Coefficient Does NOT Cross Red Line**
- Statistically significant (p < 0.05)
- Effect is reliably different from zero
- Narrow confidence interval = more precision

**Longer Error Bars = More Uncertainty**
- Could be: small sample, high variation, multicollinearity
- Effect less precisely estimated

**Shorter Error Bars = Better Precision**
- Larger sample size or lower variation
- Effect more reliably estimated

---

## Common Mistakes and How to Avoid Them

### Mistake 1: Focusing Only on p-Values

**Wrong:** "p > 0.05, so this variable doesn't matter"
**Better:** "Consider effect size AND significance. A small p-value with tiny coefficient might not be practically important."

**Example:**
- Coefficient: 0.001, p < 0.001 (statistically significant)
- But 1-unit increase in X → 0.001 change in Y (practically negligible?)

### Mistake 2: Causal Interpretation

**Wrong:** "Education CAUSES higher income"
**Better:** "Education is ASSOCIATED WITH higher income"

**Why?** Regression shows correlation, not causation. Maybe both caused by family wealth.

### Mistake 3: Predicting Outside Data Range

**Wrong:** Using OLS to predict income when X values way outside data range
**Better:** Only predict within observed X values; extrapolation unreliable

### Mistake 4: Ignoring Model Diagnostics

**Wrong:** Only looking at p-values and R²
**Better:** Always check residual plots, assumptions, and data quality

### Mistake 5: Multiple Comparisons

**Wrong:** Trying many different models and reporting only the "best" results
**Better:** Specify model beforehand (pre-registration) to avoid p-hacking

---

## Quick Reference: Interpreting Effect Sizes

### What's a "Big" Effect?

**For OLS (education → income):**
- $100 = tiny
- $500 = small but meaningful
- $2,000 = moderate
- $5,000+ = large

**For Logit (odds ratios):**
- 1.0 = no effect
- 1.1 = 10% change in odds (small)
- 1.3 = 30% change in odds (moderate)
- 1.5 = 50% change in odds (large)
- 2.0 = 100% change in odds (very large)

### For R² (OLS):
- 0.02 = small (2% variance)
- 0.15 = medium (15% variance)
- 0.35+ = large (35%+ variance)

---

## Presenting Results Professionally

### In a Table:

| Variable | Coefficient (SE) | p-value | 95% CI | 
|----------|------------------|---------|--------|
| Years Education | 3125.45* (245.67) | <.001 | [2640.31, 3610.59] |
| Work Experience | 487.23* (89.54) | <.001 | [311.61, 662.86] |

### In Text:

"Each additional year of education is associated with $3,125 higher annual income (b = 3125.45, SE = 245.67, p < .001). The effect of work experience is smaller but still substantial, with each year associated with $487 higher income (b = 487.23, SE = 89.54, p < .001)."

### Reporting Results:

Always include:
1. Sample size (N)
2. Model specification (dependent variable, predictors)
3. All coefficients with standard errors
4. Statistical significance (p-values or stars)
5. Model fit (R² for OLS, Pseudo R² for Logit)
6. Any missing data handled

---

## Additional Resources

For further reading on interpreting regression:
- Fox, J. (2015). Applied Regression Analysis and Generalized Linear Models
- Stata Learning Modules on Logistic Regression
- "Reading Regression Coefficients" tutorials online

---

**Remember:** Statistical significance ≠ Practical Importance!
**Always consider both p-values AND effect sizes.**

---

*Version 1.0 | Last Updated 2024*
