# Deploying to Streamlit Community Cloud

## Prerequisites

1. GitHub account with repository created
2. Streamlit account (free): https://share.streamlit.io

## Step-by-Step Deployment

### 1. Push to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Regression Analysis Tool"
git branch -M main
git remote add origin https://github.com/yourusername/regression-tool.git
git push -u origin main
```

### 2. Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "Deploy an app"
3. Enter GitHub repository URL: `https://github.com/yourusername/regression-tool`
4. Select branch: `main`
5. Select app file: `app.py`
6. Click "Deploy"

**That's it!** Your app will be live in 2-3 minutes.

### 3. Share the Link

Once deployed, you'll get a URL like:
```
https://yourusername-regression-tool.streamlit.app
```

Share this link with reviewers for live testing.

## Advanced Configuration

### secrets.toml (Optional)

Create `.streamlit/secrets.toml` for configuration:

```toml
[general]
theme = "light"
primaryColor = "#1f77b4"
```

### requirements.txt

Streamlit Cloud automatically installs from `requirements.txt`. Ensure all versions are pinned:

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

## Troubleshooting

**"Import Error"**
- Ensure all imports are in requirements.txt
- Check Python version (3.8+ required)

**"App takes too long to load"**
- First load may take 1-2 minutes
- Subsequent loads are instant

**"Data file not found"**
- Place demo_data.csv in root directory
- Use relative paths: `pd.read_csv('demo_data.csv')`

## Alternative Hosting Platforms

If Streamlit Cloud doesn't work:

### Hugging Face Spaces
1. Go to https://huggingface.co/spaces
2. Create new Space → Streamlit
3. Connect GitHub repo
4. Auto-deploys on push

### Heroku (deprecated but alternative)
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Railway
1. Sign up at railway.app
2. Connect GitHub repo
3. Set start command: `streamlit run app.py`
4. Deploy

### Render
1. Go to render.com
2. Create new Web Service
3. Connect GitHub
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run app.py --server.port 10000`

## GitHub Repository Checklist

- [ ] All source code committed
- [ ] requirements.txt up to date
- [ ] demo_data.csv included
- [ ] Sample outputs included
- [ ] README.md in root (GitHub-focused)
- [ ] LICENSE file
- [ ] .gitignore set up
- [ ] QUICK_START.md with installation
- [ ] TECHNICAL_NOTE.md included
- [ ] Deployed to Streamlit Cloud
- [ ] Demo link working and tested

## Recommended GitHub Structure

```
regression-tool/
├── README.md
├── README_GITHUB.md
├── TECHNICAL_NOTE.md
├── LICENSE
├── .gitignore
├── app.py
├── data_handler.py
├── regression_models.py
├── visualization.py
├── export_results.py
├── requirements.txt
├── demo_data.csv
├── sample_ols_regression_table.csv
├── sample_logit_regression_table.csv
├── QUICK_START.md
├── LIMITATIONS.md
├── MODEL_INTERPRETATION.md
├── docs/
│   └── (additional documentation)
└── .streamlit/
    └── config.toml (optional)
```

## After Deployment

1. Test the live demo thoroughly
2. Share link in submission
3. Monitor Streamlit Cloud for errors
4. Keep repository updated

That's it! Your tool is now accessible to anyone with the link. ✅
