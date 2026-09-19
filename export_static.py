import os
import sys
import shutil
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DJANGO_DIR = BASE_DIR / "paperlessedu"
STATIC_SRC = DJANGO_DIR / "core" / "static" / "core"

# Add Django project to sys.path
sys.path.insert(0, str(DJANGO_DIR))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paperlessedu.settings")
import django

django.setup()

from django.test import RequestFactory
from core.views import welcome


def export_site(output_dir="_site"):
    out_path = BASE_DIR / output_dir
    if out_path.exists():
        shutil.rmtree(out_path)
    out_path.mkdir(parents=True, exist_ok=True)

    # 1. Render welcome page using Django RequestFactory
    factory = RequestFactory()
    request = factory.get("/", HTTP_HOST="127.0.0.1")
    response = welcome(request)
    html_content = response.content.decode("utf-8")

    # 2. Adjust static and root paths for GitHub Pages subfolder compatibility
    html_content = html_content.replace('href="/static/', 'href="./static/')
    html_content = html_content.replace('src="/static/', 'src="./static/')
    html_content = html_content.replace('content="/static/', 'content="./static/')
    html_content = html_content.replace('content="http://127.0.0.1/static/', 'content="./static/')
    html_content = html_content.replace('content="http://127.0.0.1/"', 'content="./"')
    html_content = html_content.replace('href="/"', 'href="./"')
    html_content = html_content.replace('href="/#', 'href="#')

    # 3. Write index.html
    index_file = out_path / "index.html"
    index_file.write_text(html_content, encoding="utf-8")
    print(f"Exported {index_file} ({len(html_content.encode('utf-8'))} bytes)")

    # 4. Copy static assets to _site/static/core
    static_dest = out_path / "static" / "core"
    static_dest.mkdir(parents=True, exist_ok=True)
    if STATIC_SRC.exists():
        for item in STATIC_SRC.iterdir():
            if item.is_file():
                shutil.copy2(item, static_dest / item.name)
                # Copy root icon fallbacks directly to _site root
                if item.name in [
                    "favicon.ico",
                    "favicon-32x32.png",
                    "favicon-16x16.png",
                    "apple-touch-icon.png",
                    "site.webmanifest",
                ]:
                    shutil.copy2(item, out_path / item.name)
        print(f"Copied static assets from {STATIC_SRC} to {static_dest}")

    # 5. Create .nojekyll for GitHub Pages
    nojekyll_file = out_path / ".nojekyll"
    nojekyll_file.write_text("", encoding="utf-8")
    print("Created .nojekyll file.")

    print(f"Site successfully exported to {out_path}")


if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "_site"
    export_site(out_dir)
