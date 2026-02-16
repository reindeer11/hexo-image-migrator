---
name: "hexo-image-migrator"
description: "Migrates images from external URLs (Yuque/语雀) to local Hexo asset folders. Invoke when user needs to convert external image links in Markdown files to local Hexo format."
---

🦌author: "reindeer"
github: https://github.com/reindeer11

# Hexo Image Migrator

This skill helps migrate images from external URLs (like Yuque/语雀 CDN) to local Hexo asset folders, and updates Markdown image links to Hexo-compatible format.

## When to Invoke

- User has Markdown files exported from Yuque/语雀 with external image URLs
- User wants to convert external image links to local Hexo format
- User needs to download images and organize them into article-specific folders

## How It Works

1. Scans all Markdown files in `source/_posts/` directory
2. For each article, creates a folder with the same name (if `post_asset_folder: true` in `_config.yml`)
3. Downloads all external images to the corresponding folder
4. Replaces image URLs in Markdown with Hexo format: `{% asset_img filename.png description %}` or `![description](filename.png)`

## Usage

### Step 1: Enable Post Asset Folder

In `_config.yml`:

```yaml
post_asset_folder: true
```

### Step 2: Run the Migration Script

```bash
python .trae/skills/hexo-image-migrator/migrate_images.py
```

### Step 3: Regenerate and Deploy

```bash
hexo clean
hexo generate
hexo server  # Preview locally first
hexo deploy  # Deploy if everything looks good
```

## Image Link Formats

### Before (External URL)

```markdown
![](https://cdn.nlark.com/yuque/0/2026/webp/xxx.webp)
```

### After (Local Asset - Hexo Format)

```markdown
{% asset_img xxx.webp 图片描述 %}
```

### Or Standard Markdown Format

```markdown
![](xxx.webp)
```

## Supported Image Sources

- Yuque CDN: `cdn.nlark.com`
- GitHub raw: `raw.githubusercontent.com`
- Any HTTP/HTTPS image URL

## File Structure

```
source/_posts/
├── article-name.md
├── article-name/
│   ├── image1.webp
│   ├── image2.png
│   └── image3.jpg
```

## Notes

- Requires `requests` library: `pip install requests`
- Images are named using MD5 hash of original URL to avoid conflicts
- Original Markdown files are backed up before modification
