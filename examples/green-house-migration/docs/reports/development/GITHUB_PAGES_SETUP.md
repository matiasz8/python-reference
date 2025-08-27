# 🚀 GitHub Pages Setup Guide

This guide will help you set up GitHub Pages for the Green House documentation.

## 📋 Prerequisites

- GitHub repository with push access

- GitHub Actions enabled

- Repository settings access

## 🔧 Setup Steps

### 1. Enable GitHub Pages

1. Go to your repository on GitHub

2. Navigate to **Settings** → **Pages**

3. Under **Source**, select **GitHub Actions**

4. Click **Save**

### 2. Configure Repository Settings

1. Go to **Settings** → **General**

2. Scroll down to **GitHub Pages** section

3. Ensure **GitHub Actions** is selected as the source

4. Set the **Custom domain** (optional)

### 3. Update Repository Information

Update the following files with your repository information:

#### `docs/_config.yml`

```yaml
# Update these lines with your repository info
repository: your-username/your-repo-name
repository_url: https://github.com/your-username/your-repo-name
```

#### `README.md`

```markdown
# Update the GitHub Pages URL

[GitHub Pages Documentation](https://your-username.github.io/your-repo-name/)
```

### 4. Push Changes

```bash
# Add all changes
git add .

# Commit changes
git commit -m "feat: add GitHub Pages documentation structure"

# Push to main branch
git push origin main
```

### 5. Verify Deployment

1. Go to **Actions** tab in your repository

2. Check that the "Deploy to GitHub Pages" workflow runs successfully

3. Wait for the deployment to complete (usually 2-3 minutes)

4. Visit your GitHub Pages URL: `https://your-username.github.io/your-repo-name/`

## 🎨 Customization Options

### Change Theme

Edit `docs/_config.yml`:

```yaml
# Available themes:
theme: jekyll-theme-cayman # Modern, clean theme
# theme: jekyll-theme-minimal   # Minimal theme
# theme: jekyll-theme-slate     # Dark theme
# theme: jekyll-theme-tactile   # Tactile theme
```

### Custom Domain

1. Add your custom domain to `docs/CNAME`:

```
your-domain.com
```

2. Update `docs/_config.yml`:

```yaml
url: "https://your-domain.com"
```

### Analytics

Add Google Analytics to `docs/_config.yml`:

```yaml
google_analytics: UA-XXXXXXXXX-X
```

## 🔍 Troubleshooting

### Common Issues

#### Build Fails

- Check GitHub Actions logs for errors

- Ensure all dependencies are in `Gemfile`

- Verify Jekyll configuration syntax

#### Pages Not Updating

- Clear browser cache

- Check if GitHub Actions workflow completed

- Verify branch name (should be `main` or `master`)

#### Styling Issues

- Check if CSS files are being served

- Verify asset paths in `_config.yml`

- Test locally with `jekyll serve`

### Local Testing

```bash
# Install Jekyll locally
gem install jekyll bundler

# Navigate to docs directory
cd docs

# Install dependencies
bundle install

# Serve locally
bundle exec jekyll serve

# Visit http://localhost:4000
```

## 📱 Mobile Optimization

The documentation is already optimized for mobile devices with:

- Responsive design

- Touch-friendly navigation

- Optimized typography

- Fast loading times

## 🔒 Security

- All external links open in new tabs

- No sensitive information in documentation

- HTTPS enforced by GitHub Pages

- Content Security Policy headers

## 📊 Performance

- Optimized images and assets

- Minified CSS and JavaScript

- CDN for external resources

- Efficient caching strategies

## 🎯 Next Steps

1. **Customize Content**: Update documentation with your specific information

2. **Add Analytics**: Set up Google Analytics for visitor tracking

3. **SEO Optimization**: Add meta tags and structured data

4. **Regular Updates**: Keep documentation current with code changes

## 📞 Support

- **GitHub Pages Documentation**: <https://docs.github.com/en/pages>

- **Jekyll Documentation**: <https://jekyllrb.com/docs/>

- **GitHub Actions**: <https://docs.github.com/en/actions>

---

**Note**: After setup, your documentation will be available at:
`https://your-username.github.io/your-repo-name/`
