# Regression Analysis Tool - Installation & Quick Start Guide

## Installation (5 minutes)

### Prerequisites
- **Python 3.8 or higher** (download from python.org if needed)
- **pip** (included with Python)
- Internet connection

### Step-by-Step Installation

#### Windows Users:

1. **Download and extract this folder** to your computer
   - Extract to a location like: `C:\Users\YourName\regression_tool`

2. **Open Command Prompt** in the tool directory
   - Right-click the folder → "Open PowerShell window here" (or Command Prompt)

3. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   You should see `(venv)` appear in your command line

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   This will take 1-2 minutes and show progress

5. **Verify installation** (optional)
   ```bash
   python test_modules.py
   ```
   You should see "✓ ALL TESTS PASSED"

#### macOS/Linux Users:

1. **Extract this folder** to your home directory

2. **Open Terminal** in the tool directory
   ```bash
   cd ~/regression_tool
   ```

3. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Verify installation**
   ```bash
   python test_modules.py
   ```

---

## Running the Tool (30 seconds)

### Start the Application

**In Command Prompt / Terminal:**
```bash
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
```

The tool will automatically open in your web browser. If not, copy the URL above into your browser.

---

## First Time Walkthrough (2 minutes)

### Testing with Demo Data

1. **Navigate to Page 1: Data Upload**
   - Click "📥 Load Demo Dataset"
   - Confirm: "✅ Data loaded successfully!"

2. **Go to Page 2: Data Exploration**
   - Review the summary statistics
   - Check "Missing Data" tab
   - Note: ~5% of Annual_Income is missing (intentional demo)

3. **Go to Page 3: Analysis Setup**
   - Review auto-detected variable types
   - Keep defaults (all should be appropriate)
   - **For OLS Demo:**
     - Dependent Variable: Annual_Income
     - Independent Variables: Years_Education, Work_Experience, Employment_Status, Age
   - Click the page continue indicator

4. **Go to Page 4: Model Estimation**
   - Review data information
   - Click "🚀 Estimate Model"
   - Wait for "✅ Model estimated successfully!"

5. **Go to Page 5: Results & Export**
   - View the regression table
   - Click "📈 Coefficient Plot" tab to see visualization
   - Click "📥 Download as CSV" to export results

### Try the Logit Model

1. Go back to Page 3
2. Change to:
   - Dependent Variable: Higher_Education
   - Independent Variables: Age, Gender, Work_Experience
3. Go to Page 4, select "Logistic Regression"
4. Click "🚀 Estimate Model"
5. View results (odds ratios will appear for logit)

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
# Make sure virtual environment is activated first
# Then:
pip install -r requirements.txt

# Or install manually:
pip install streamlit pandas numpy statsmodels scipy matplotlib seaborn
```

### Issue: "Python not found" or "command not recognized"

**Solution (Windows):**
- Open Python from Start Menu → right-click → Run as administrator
- Type: `pip install streamlit` directly

**Or:**
- Check that Python is installed: `python --version`
- If not installed, download from python.org

### Issue: Port 8501 already in use

**Solution:**
```bash
streamlit run app.py --server.port 8502
```
Use a different port number (8502, 8503, etc.)

### Issue: "Error loading file" when uploading data

**Solutions:**
- Ensure file is CSV or Excel format (.csv, .xlsx, .xls)
- Check file has no encoding issues (save as UTF-8)
- Ensure column headers are in first row
- Try a smaller file first (demo_data.csv)

### Issue: "Logit requires binary dependent variable"

**Solution:**
- Your dependent variable has more than 2 unique values
- For Logit: only use Y with 0/1 or other 2-value coding
- Use OLS instead for continuous variables

### Issue: "No data loaded" or page won't load

**Solution:**
- Reload browser page (F5)
- Make sure you're on http://localhost:8501 (not https)
- Check that Streamlit is still running in terminal

### Issue: Application crashes or shows error

**Solution:**
1. Note the error message
2. Close Streamlit (Ctrl+C in terminal)
3. Restart: `streamlit run app.py`
4. Try the task again from Page 1
5. If error persists, check troubleshooting section in README.md

---

## File Organization

```
regression_tool/
├── app.py                    # Main application (run this)
├── test_modules.py          # Verification test
├── generate_samples.py      # Creates sample outputs
│
├── data_handler.py          # Data loading module
├── regression_models.py     # OLS & Logit models
├── visualization.py         # Charts & plots
├── export_results.py        # Export functionality
│
├── requirements.txt         # Python dependencies
├── demo_data.csv           # Sample dataset for testing
│
├── README.md               # Full documentation
├── LIMITATIONS.md          # Assumptions & limitations
└── QUICK_START.md          # This file
```

---

## Usage Tips

### Data Preparation Tips
- **Before uploading:** Remove unusable columns (ID, names, dates)
- **Variable naming:** Use clear names without spaces (use_underscore_format)
- **Categorical variables:** Code as 0/1 for binary, or numbers 1,2,3... for categories
- **Date variables:** Convert to years or age first

### Analysis Tips
- **Start with fewer predictors:** Add complexity gradually
- **Check correlations:** Variables shouldn't be too highly correlated
- **Interpret effect sizes:** Look at coefficient magnitude, not just p-values
- **Review diagnostics:** Especially residual plots for OLS models

### Interpretation Tips
- **OLS Coefficient:** "For each 1-unit increase in X, Y increases by [coefficient] units"
- **Logit Coefficient:** "For each 1-unit increase in X, log-odds increase by [coefficient]"
- **Odds Ratio:** "For each 1-unit increase in X, odds are multiplied by [odds ratio]"
- **p-value < 0.05:** Typically considered statistically significant
- **R² (OLS):** Proportion of variance explained; 0.30 = 30% explained

---

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.8 | 3.9+ |
| RAM | 2 GB | 4+ GB |
| Disk Space | 500 MB | 1+ GB |
| Internet | No (after install) | No (after install) |

---

## Getting Help

1. **Check README.md** - Full documentation and troubleshooting
2. **Check LIMITATIONS.md** - Understanding assumptions and model interpretation
3. **Review code comments** - Each .py file has documentation
4. **Try demo data** - Use demo_data.csv to test functionality
5. **Verify installation** - Run `python test_modules.py`

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Run `streamlit run app.py`
3. ✅ Load demo data and run a model
4. ✅ Export results
5. 📊 Use with your own data!

---

**Questions?** Check the documentation files or review the inline code comments.

**Happy analyzing!** 📊

---

*Last Updated: 2024*
*Version: 1.0*
