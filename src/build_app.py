#!/usr/bin/env python3
"""
TrolMaster Product Portal — Build Script
=========================================
Reads config, fetches live Google Sheets data (with fallback),
inlines CSS/JS/logo, and produces a self-contained build/index.html.
Also saves a versioned snapshot under build/versions/.

Usage:
    python3 src/build_app.py [--desc "brief description"]

Options:
    --desc      Short description for the version changelog entry
    --no-fetch  Skip live data fetch, use empty fallback only
"""

import json
import os
import re
import sys
import base64
import shutil
import datetime
import argparse
import urllib.request
import urllib.error

# ──────────────────────────────────────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_PATH        = os.path.join(ROOT, "src", "config.json")
I18N_DIR           = os.path.join(ROOT, "src", "i18n")
STYLES_PATH        = os.path.join(ROOT, "src", "static", "styles.css")
APP_JS_PATH        = os.path.join(ROOT, "src", "static", "app.js")
TEMPLATE_PATH      = os.path.join(ROOT, "src", "templates", "index.html.template")

BUILD_DIR          = os.path.join(ROOT, "build")
OUTPUT_HTML        = os.path.join(BUILD_DIR, "index.html")
VERSIONS_DIR       = os.path.join(BUILD_DIR, "versions")
CHANGELOG_JSON     = os.path.join(BUILD_DIR, "changelog_entries.json")
VERSION_HISTORY_MD = os.path.join(ROOT, "docs", "VERSION_HISTORY.md")


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────
def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_i18n():
    bundle = {}
    for lang_file in ["en.json", "zh-Hant.json", "th.json"]:
        lang = lang_file.replace(".json", "")
        fpath = os.path.join(I18N_DIR, lang_file)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                bundle[lang] = json.load(f)
    return bundle


def load_product_translations():
    """Load product translations from i18n/product_translations_zh.json and th.json."""
    result = {}
    for lang, fname in [("zh-Hant", "product_translations_zh.json"), ("th", "product_translations_th.json")]:
        fpath = os.path.join(I18N_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                result[lang] = json.load(f)
                print(f"  ✓ Product translations loaded: {fname}")
        else:
            print(f"  [WARN] Product translations not found: {fname}")
            result[lang] = {}
    return result


def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def logo_to_data_uri(logo_path):
    """Convert logo PNG to base64 data URI."""
    if not os.path.exists(logo_path):
        print(f"  [WARN] Logo not found: {logo_path}")
        return ""
    with open(logo_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{data}"


def fetch_url(url, timeout=10):
    """Fetch URL and return text content, or None on failure."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TrolMaster-Build/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        print(f"  [WARN] Fetch failed {url[:60]}… : {e}")
        return None


def parse_gviz(text):
    """Parse Google Visualization JSON response."""
    # Strip protective prefix
    text = re.sub(r"^/\*.*?\*/\s*", "", text, flags=re.DOTALL)
    text = re.sub(r"^google\.visualization\.Query\.setResponse\(", "", text)
    text = re.sub(r"\);\s*$", "", text)
    return json.loads(text)


def gviz_to_rows(gviz_data, col_map, skip_header=0, detect_categories=False):
    """Convert gviz table to list of dicts using column index mapping.

    Note: gviz API's table.rows does NOT include header rows (those are in table.cols),
    so skip_header defaults to 0. Only set skip_header > 0 if the sheet has
    an extra non-header data row at the top that should be skipped.

    When detect_categories=True: rows where model has a value but short_desc and msrp
    are empty are treated as brand/category separators. Products after a category row
    get that category name assigned to a 'category' field.
    """
    rows_raw = gviz_data.get("table", {}).get("rows", [])
    result = []
    start_idx = skip_header if skip_header > 0 else 0
    current_category = ""

    for row in rows_raw[start_idx:]:
        cells = row.get("c", [])

        def get(key):
            idx = col_map.get(key)
            if idx is None or idx >= len(cells):
                return ""
            cell = cells[idx]
            if cell is None:
                return ""
            v = cell.get("v")
            return str(v) if v is not None else ""

        model = get("model").strip()

        if detect_categories:
            short_desc = get("short_desc").strip()
            msrp = get("msrp").strip()
            # Detect category rows: model has value, but short_desc and msrp are empty
            if model and not short_desc and not msrp:
                current_category = model
                continue  # Skip category row itself, don't add as product

        if model:
            record = {k: get(k) for k in col_map}
            if detect_categories:
                record["category"] = current_category
            result.append(record)
    return result


# ──────────────────────────────────────────────────────────────────────────────
# Data Fetching
# ──────────────────────────────────────────────────────────────────────────────
def fetch_products(cfg, no_fetch=False):
    prod_cfg = cfg["google_sheets"]["product"]
    col_map  = prod_cfg["columns"]

    if no_fetch:
        print("  [INFO] --no-fetch: skipping product data")
        return []

    url = prod_cfg.get("gviz_url", "")
    if not url:
        return []

    print(f"  Fetching products from Google Sheets...")
    text = fetch_url(url)
    if not text:
        print("  [WARN] Products: using empty fallback")
        return []

    try:
        gviz = parse_gviz(text)
        rows = gviz_to_rows(gviz, col_map, skip_header=0, detect_categories=True)
        print(f"  ✓ Products: {len(rows)} rows loaded")
        return rows
    except Exception as e:
        print(f"  [WARN] Products parse error: {e}")
        return []


def fetch_inventory(cfg, no_fetch=False):
    inv_cfg = cfg["google_sheets"]["inventory"]
    col_map = inv_cfg["columns"]

    if no_fetch:
        print("  [INFO] --no-fetch: skipping inventory data")
        return []

    url = inv_cfg.get("gviz_url", "")
    if not url:
        return []

    print(f"  Fetching inventory from Google Sheets...")
    text = fetch_url(url)
    if not text:
        print("  [WARN] Inventory: using empty fallback")
        return []

    try:
        gviz = parse_gviz(text)
        rows = gviz_to_rows(gviz, col_map, skip_header=0)
        print(f"  ✓ Inventory: {len(rows)} rows loaded")
        return rows
    except Exception as e:
        print(f"  [WARN] Inventory parse error: {e}")
        return []


# ──────────────────────────────────────────────────────────────────────────────
# HTML Building
# ──────────────────────────────────────────────────────────────────────────────
def build_popular_tags(models):
    tags = []
    for m in models:
        safe = m.replace('"', '&quot;')
        tags.append(f'<button class="popular-tag" data-model="{safe}">{safe}</button>')
    return "\n        ".join(tags)


def build_config_for_js(cfg):
    """Build the runtime config object for window.__TM_CONFIG__."""
    prod_cfg = cfg["google_sheets"]["product"]
    inv_cfg  = cfg["google_sheets"]["inventory"]
    return {
        "gviz_product":       prod_cfg.get("gviz_url", ""),
        "gviz_inventory":     inv_cfg.get("gviz_url", ""),
        "product_columns":    prod_cfg.get("columns", {}),
        "inventory_columns":  inv_cfg.get("columns", {}),
        "popular_models":     cfg.get("popular_models", []),
        "fallback_rates":     cfg.get("exchange_rate", {}).get("fallback_rates", {}),
        "lang_currency_map":  cfg.get("exchange_rate", {}).get("lang_currency_map", {}),
    }


def build_html(cfg, i18n_bundle, products, inventory, product_translations, desc=""):
    template   = load_text(TEMPLATE_PATH)
    styles_css = load_text(STYLES_PATH)
    app_js     = load_text(APP_JS_PATH)

    logo_path = os.path.join(ROOT, cfg["paths"]["logo"])
    logo_uri  = logo_to_data_uri(logo_path)

    js_config = build_config_for_js(cfg)

    popular_tags = build_popular_tags(cfg.get("popular_models", []))

    html = template
    html = html.replace("{{STYLES_CSS}}",    styles_css)
    html = html.replace("{{APP_JS}}",        app_js)
    html = html.replace("{{LOGO_DATA_URI}}", logo_uri)
    html = html.replace("{{DEFAULT_LANG}}",  cfg["app"].get("default_lang", "en"))
    html = html.replace("{{POPULAR_TAGS}}",  popular_tags)
    html = html.replace("{{CONFIG_JSON}}",   json.dumps(js_config,    ensure_ascii=False))
    html = html.replace("{{I18N_JSON}}",     json.dumps(i18n_bundle,  ensure_ascii=False))
    html = html.replace("{{PRODUCTS_JSON}}", json.dumps(products,     ensure_ascii=False))
    html = html.replace("{{INVENTORY_JSON}}", json.dumps(inventory,   ensure_ascii=False))
    html = html.replace("{{PRODUCT_TRANSLATIONS_JSON}}", json.dumps(product_translations, ensure_ascii=False))
    
    return html


# ──────────────────────────────────────────────────────────────────────────────
# Version Control
# ──────────────────────────────────────────────────────────────────────────────
def save_version_snapshot(html_content, cfg, desc=""):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")

    # Determine next version number from changelog
    changelog = []
    if os.path.exists(CHANGELOG_JSON):
        try:
            with open(CHANGELOG_JSON, "r", encoding="utf-8") as f:
                changelog = json.load(f)
        except Exception:
            changelog = []

    # Simple auto-increment of patch version
    if changelog:
        last = changelog[-1].get("version", "1.0.0")
        parts = last.split(".")
        try:
            parts[-1] = str(int(parts[-1]) + 1)
        except Exception:
            parts = ["1", "0", str(len(changelog) + 1)]
        version = ".".join(parts)
    else:
        version = cfg["app"].get("version", "1.0.0")

    safe_desc = re.sub(r"[^\w\-]", "_", desc or "build")[:40]
    snapshot_name = f"{date_str}_{time_str}_v{version}_{safe_desc}.html"

    day_dir = os.path.join(VERSIONS_DIR, now.strftime("%Y-%m-%d"))
    os.makedirs(day_dir, exist_ok=True)

    snapshot_path = os.path.join(day_dir, snapshot_name)
    with open(snapshot_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  ✓ Snapshot saved: build/versions/{now.strftime('%Y-%m-%d')}/{snapshot_name}")

    # Update changelog JSON
    entry = {
        "version": version,
        "timestamp": now.isoformat(),
        "description": desc or "build",
        "snapshot": f"build/versions/{now.strftime('%Y-%m-%d')}/{snapshot_name}",
    }
    changelog.append(entry)
    with open(CHANGELOG_JSON, "w", encoding="utf-8") as f:
        json.dump(changelog, f, ensure_ascii=False, indent=2)

    # Update VERSION_HISTORY.md
    update_version_history_md(entry)

    return version, snapshot_path


def update_version_history_md(entry):
    """Append a new version entry to docs/VERSION_HISTORY.md."""
    line = (
        f"\n## v{entry['version']} — {entry['timestamp'][:10]}\n"
        f"- **Description**: {entry['description']}\n"
        f"- **Snapshot**: `{entry['snapshot']}`\n"
    )
    mode = "a" if os.path.exists(VERSION_HISTORY_MD) else "w"
    with open(VERSION_HISTORY_MD, mode, encoding="utf-8") as f:
        if mode == "w":
            f.write("# TrolMaster Product Portal — Version History\n\n")
            f.write("_Auto-generated. To roll back: copy the snapshot file to `build/index.html` and redeploy._\n")
        f.write(line)


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Build TrolMaster Product Portal HTML")
    parser.add_argument("--desc", default="", help="Short description for this build")
    parser.add_argument("--no-fetch", action="store_true", help="Skip live data fetch")
    args = parser.parse_args()

    print("\n🔨 TrolMaster Product Portal — Build\n" + "─" * 44)

    # Load config
    cfg = load_config()
    print("  ✓ Config loaded")

    # Load i18n
    i18n_bundle = load_i18n()
    print(f"  ✓ i18n loaded: {list(i18n_bundle.keys())}")

    # Load product translations
    product_translations = load_product_translations()

    # Fetch data
    products  = fetch_products(cfg, no_fetch=args.no_fetch)
    inventory = fetch_inventory(cfg, no_fetch=args.no_fetch)

    # Build HTML
    print("  Building HTML…")
    html = build_html(cfg, i18n_bundle, products, inventory, product_translations, desc=args.desc)

    # Ensure build dir
    os.makedirs(BUILD_DIR, exist_ok=True)

    # Write main output
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    size_kb = os.path.getsize(OUTPUT_HTML) / 1024
    print(f"  ✓ Output: build/index.html ({size_kb:.1f} KB)")

    # Save version snapshot
    version, snapshot = save_version_snapshot(html, cfg, desc=args.desc or "build")
    print(f"  ✓ Version: v{version}")

    print("\n✅ Build complete!\n")
    print(f"   Preview locally:  open {OUTPUT_HTML}")
    print(f"   Deploy command:   netlify deploy --dir=build --site={cfg['netlify']['site_id']}")
    print()


if __name__ == "__main__":
    main()
