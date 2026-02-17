import os
import re
import requests
import hashlib
import shutil

POSTS_DIR = r"G:\blog\source\_posts"

IMAGE_PATTERN = r'!\[([^\]]*)\]\((https?://[^)]+)\)'

def download_image(url, save_path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": url
        }
        response = requests.get(url, headers=headers, timeout=30, verify=True)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"  [OK] Downloaded: {os.path.basename(save_path)}")
            return True
        else:
            print(f"  [FAIL] HTTP {response.status_code}: {url}")
    except Exception as e:
        print(f"  [FAIL] {e}: {url}")
    return False

def get_filename_from_url(url, index):
    ext = url.split(".")[-1].split("?")[0].lower()
    if ext not in ["webp", "png", "jpg", "jpeg", "gif", "svg", "bmp"]:
        ext = "webp"
    hash_name = hashlib.md5(url.encode()).hexdigest()[:10]
    return f"img_{index:02d}_{hash_name}.{ext}"

def process_markdown_file(md_path):
    md_dir = os.path.dirname(md_path)
    md_name = os.path.splitext(os.path.basename(md_path))[0]
    
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    matches = re.findall(IMAGE_PATTERN, content)
    
    external_images = [(alt, url) for alt, url in matches if url.startswith("http")]
    
    if not external_images:
        print(f"[SKIP] No external images: {md_name}")
        return
    
    asset_dir = os.path.join(md_dir, md_name)
    os.makedirs(asset_dir, exist_ok=True)
    
    print(f"\n[PROCESS] {md_name}")
    print(f"  Found {len(external_images)} external images")
    print(f"  Asset folder: {asset_dir}")
    
    url_to_local = {}
    
    for index, (alt_text, url) in enumerate(external_images, 1):
        filename = get_filename_from_url(url, index)
        local_path = os.path.join(asset_dir, filename)
        
        if download_image(url, local_path):
            url_to_local[url] = filename
    
    if not url_to_local:
        print(f"  [WARN] No images downloaded, skipping file update")
        return
    
    backup_path = md_path + ".bak"
    shutil.copy2(md_path, backup_path)
    print(f"  [BACKUP] {backup_path}")
    
    new_content = content
    for old_url, filename in url_to_local.items():
        pattern = re.compile(r'!\[[^\]]*\]\(' + re.escape(old_url) + r'\)')
        new_content = pattern.sub(f"{{% asset_img {filename} %}}", new_content)
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"  [UPDATED] {len(url_to_local)} image links replaced")

def main():
    print("=" * 60)
    print("Hexo Image Migrator - Yuque to Local")
    print("=" * 60)
    print(f"Posts directory: {POSTS_DIR}")
    print()
    
    if not os.path.exists(POSTS_DIR):
        print(f"[ERROR] Directory not found: {POSTS_DIR}")
        return
    
    md_files = [f for f in os.listdir(POSTS_DIR) if f.endswith(".md")]
    print(f"Found {len(md_files)} Markdown files\n")
    
    for md_file in sorted(md_files):
        md_path = os.path.join(POSTS_DIR, md_file)
        process_markdown_file(md_path)
    
    print("\n" + "=" * 60)
    print("Migration Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run 'hexo clean'")
    print("2. Run 'hexo generate'")
    print("3. Run 'hexo server' to preview")
    print("4. Check images are displayed correctly")
    print("5. Run 'hexo deploy' to publish")

if __name__ == "__main__":
    main()
