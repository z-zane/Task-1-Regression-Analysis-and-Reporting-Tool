# Regression Analysis and Reporting Tool

A web-based regression analysis tool for researchers. Upload data, run OLS or Logistic regression, and generate publication-ready results—all without programming.

## Features

- 📤 **Easy Data Upload** - CSV or Excel files
- 🤖 **Smart Variable Detection** - Automatic type classification
- 📊 **Two Regression Models** - OLS and Logistic regression
- 📈 **Publication-Ready Output** - Tables, plots, exports
- 🎨 **Intuitive Web Interface** - 5-page guided workflow
- ✅ **No Coding Required** - Designed for non-programmers

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Run
streamlit run app.py
```

Load demo data and start analyzing in seconds!

## Documentation

- **[QUICK_START.md](QUICK_START.md)** - Installation & first use
- **[README.md](README.md)** - Complete user guide
- **[MODEL_INTERPRETATION.md](MODEL_INTERPRETATION.md)** - Understanding output
- **[TECHNICAL_NOTE.md](TECHNICAL_NOTE.md)** - Technical overview

## Try It Online

🌐 **[Live Demo](link-to-streamlit-cloud)** (Hosted on Streamlit Community Cloud)

## Project Structure

```
.
├── app.py                    # Main application
├── data_handler.py          # Data processing
├── regression_models.py     # OLS & Logit models
├── visualization.py         # Plots & charts
├── export_results.py        # Export functionality
├── demo_data.csv           # Sample dataset
├── requirements.txt        # Python dependencies
└── docs/                   # Documentation files
```

## Requirements

- Python 3.8+
- pandas, numpy, statsmodels, streamlit, matplotlib, seaborn

See `requirements.txt` for full list.

## Usage

1. **Upload data** - CSV or Excel format
2. **Explore** - Check data quality and missing values
3. **Setup** - Select variables and automatic model suggestion
4. **Analyze** - Fit OLS or Logistic regression
5. **Export** - Save results as CSV, Excel, or PNG

## License

MIT License - See [LICENSE](LICENSE) file

## Citation

If you use this tool, please cite:

```bibtex
@software{regression_tool_2024,
  title = {Regression Analysis and Reporting Tool},
  author = {Contributors},
  year = {2024},
  url = {https://github.com/yourusername/regression-tool}
}
```

## Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.

## Support

- **Questions?** Check the [documentation](README.md)
- **Bug reports?** Open an issue on GitHub
- **Feature requests?** Discuss in Issues section

---

**Version:** 1.0  
**Status:** Ready for production  
**Last Updated:** 2024
