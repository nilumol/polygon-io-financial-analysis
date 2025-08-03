# GitHub Setup Guide

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name your repository (e.g., "polygon-io-financial-analysis")
5. Make it public or private (your choice)
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

## Step 2: Connect Your Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote repository (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push your code to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Verify Your Setup

1. Go to your GitHub repository page
2. You should see all your files there
3. Check that sensitive files (API.env, CSV files) are NOT visible

## Step 4: Set Up Your Environment

1. Clone the repository on any machine where you want to work:
```bash
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:
```bash
# Copy the example file
cp env.example .env

# Edit .env and add your API key
# POLYGON_API_KEY=your_actual_api_key_here
```

## Step 5: Future Development

When you make changes:

```bash
# Add your changes
git add .

# Commit with a descriptive message
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## Security Notes

✅ **What's Protected:**
- Your API key (stored in .env, not tracked by Git)
- All CSV data files (excluded by .gitignore)
- Any other sensitive files

✅ **What's Public:**
- Your Python code
- README and documentation
- Requirements and project structure

## Troubleshooting

If you accidentally committed sensitive information:
1. Remove the file from Git tracking: `git rm --cached API.env`
2. Commit the removal: `git commit -m "Remove sensitive file"`
3. Push the changes: `git push`

The file will remain in your local directory but won't be tracked by Git anymore. 