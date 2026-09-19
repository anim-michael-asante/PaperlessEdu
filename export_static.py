"""
Export script for PaperlessEdu static site generation.
Renders the Django welcome template to pure HTML and copies static assets
to a self-contained static directory ready for GitHub Pages hosting.
"""

import os
import sys
import shutil
import re

# Add paperlessedu to python path
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(REPO_ROOT, "paperlessedu")
sys.path.insert(0, PROJECT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paperlessedu.settings")

import django
django.setup()

from django.test import RequestFactory
from core.views import welcome


def build_static_site(output_dir="_site"):
    output_path = os.path.join(REPO_ROOT, output_dir)
    print(f"Building static site in: {output_path}")

    # Remove and recreate output directory
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path, exist_ok=True)

    # 1. Render Django view
    rf = RequestFactory()
    request = rf.get("/", HTTP_HOST="127.0.0.1")
    response = welcome(request)
    html_content = response.content.decode("utf-8")

    # 2. Make static and relative paths robust for GitHub Pages
    # Replace absolute home link href="/" with href="./"
    html_content = re.sub(r'href="/"', 'href="./"', html_content)
    # Make sure static references use relative paths ./static/
    html_content = re.sub(r'href="/static/', 'href="./static/', html_content)
    html_content = re.sub(r'src="/static/', 'src="./static/', html_content)
    html_content = re.sub(r'href="static/', 'href="./static/', html_content)
    html_content = re.sub(r'src="static/', 'src="./static/', html_content)

    # 3. Detect deployment site URL for Open Graph & social link previews
    site_url = os.environ.get("SITE_URL")
    if not site_url and os.environ.get("GITHUB_REPOSITORY"):
        repo = os.environ.get("GITHUB_REPOSITORY")
        if "/" in repo:
            owner, repo_name = repo.split("/", 1)
            site_url = f"https://{owner}.github.io/{repo_name}"

    if site_url:
        site_url = site_url.rstrip("/")
        html_content = re.sub(
            r'content="http://127\.0\.0\.1/static/',
            f'content="{site_url}/static/',
            html_content,
        )
        html_content = re.sub(
            r'content="http://127\.0\.0\.1/"',
            f'content="{site_url}/"',
            html_content,
        )

    # 4. Write index.html
    index_file = os.path.join(output_path, "index.html")
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated {index_file} ({len(html_content)} bytes)")

    # 5. Copy static assets to _site/static/core/
    src_static = os.path.join(PROJECT_DIR, "core", "static", "core")
    dest_static = os.path.join(output_path, "static", "core")
    if os.path.exists(src_static):
        shutil.copytree(src_static, dest_static)
        print(f"Copied static assets from {src_static} to {dest_static}")

    # 6. Copy root-level favicon files to _site/ root for standard browser fallback
    for icon_name in [
        "favicon.ico",
        "favicon-32x32.png",
        "favicon-16x16.png",
        "apple-touch-icon.png",
        "paperlessedu-icon.png",
        "site.webmanifest",
    ]:
        icon_src = os.path.join(src_static, icon_name)
        if os.path.exists(icon_src):
            shutil.copy(icon_src, os.path.join(output_path, icon_name))

    # 7. Add .nojekyll so GitHub Pages does not ignore files with underscores or bypass processing
    nojekyll_file = os.path.join(output_path, ".nojekyll")
    with open(nojekyll_file, "w", encoding="utf-8") as f:
        f.write("")
    print("Created .nojekyll")

    print("\nStatic site export completed successfully!")
    return output_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "_site"
    build_static_site(out)
