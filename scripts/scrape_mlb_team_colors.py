#!/usr/bin/env python3
"""
Scrape ONLY MLB team color HEX codes + names from:
  https://teamcolorcodes.com/mlb-color-codes/

Output JSON (default: mlb_team_colors_with_labels.json):
{
  "Arizona Diamondbacks": [
    {"label":"Color 1","name":"Sedona Red","hex":"#A71930"},
    {"label":"Color 2","name":"Sonoran Sand","hex":"#E3D4AD"},
    {"label":"Color 3","name":"Black","hex":"#000000"},
    {"label":"Color 4","name":"Teal","hex":"#30CED8"},
    {"label":"Color 5","name":"White","hex":"#FFFFFF"}
  ],
  ...
}

Usage:
  pip install requests beautifulsoup4
  python scrape_mlb_team_colors.py [out.json]
"""

import json
import re
import sys
import time
from typing import Dict, List, Tuple

import requests
from bs4 import BeautifulSoup

INDEX_URL = "https://teamcolorcodes.com/mlb-color-codes/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
PAUSE_SEC = 0.6  # be polite

# Match team pages like ".../<team>-color-codes/"
TEAM_LINK_RE = re.compile(r"^https://teamcolorcodes\.com/.+?-color-codes/?$")
HEX_RE = re.compile(r"#([0-9A-Fa-f]{6})")
# Matches "Label: #RRGGBB" or "Label – #RRGGBB", allowing "Hex Color Code(s)" suffixes we strip off.
LABEL_AND_HEX_RE = re.compile(
    r"(?P<label>[A-Za-z][A-Za-z0-9\s\-/&\.'()]+?)"
    r"(?:\s+(?:hex|HEX)\s+color(?:\s+code)?s?)?"
    r"\s*[:\-–]\s*(?P<hex>#[0-9A-Fa-f]{6})"
)

# Strict list of MLB teams as shown on the site
MLB_TEAMS = {
    "Arizona Diamondbacks", "Atlanta Braves", "Baltimore Orioles", "Boston Red Sox",
    "Chicago Cubs", "Chicago White Sox", "Cincinnati Reds", "Cleveland Guardians",
    "Colorado Rockies", "Detroit Tigers", "Houston Astros", "Kansas City Royals",
    "Los Angeles Angels", "Los Angeles Dodgers", "Miami Marlins", "Milwaukee Brewers",
    "Minnesota Twins", "New York Mets", "New York Yankees", "Oakland Athletics",
    "Philadelphia Phillies", "Pittsburgh Pirates", "San Diego Padres", "San Francisco Giants",
    "Seattle Mariners", "St. Louis Cardinals", "Tampa Bay Rays", "Texas Rangers",
    "Toronto Blue Jays", "Washington Nationals"
}


def soup(url: str) -> BeautifulSoup:
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


def find_mlb_team_links() -> List[Tuple[str, str]]:
    """
    Parse the MLB index to collect (team_name, url) for MLB only.
    """
    s = soup(INDEX_URL)
    links: Dict[str, str] = {}
    for a in s.select("a[href]"):
        href = a.get("href", "").strip()
        text = a.get_text(strip=True)
        if TEAM_LINK_RE.match(href):
            name = text.replace(" Color Codes", "").strip()
            if name in MLB_TEAMS:
                links[href] = name
    return [(links[u], u) for u in sorted(links.keys())]


def clean_label(text: str) -> str:
    """
    Trim generic suffixes and whitespace from a color label/name.
    Example: "Sedona Red Hex Color Code" -> "Sedona Red"
    """
    t = re.sub(r"\s+", " ", text).strip()
    t = re.sub(r"\s*(?:hex|HEX)\s+color(?:\s+code)?s?\s*$", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s*(?:color|colou?r)\s*$", "", t, flags=re.IGNORECASE)
    return t.strip()


def extract_from_hex_table(team_soup: BeautifulSoup) -> List[Dict[str, str]]:
    """
    Parse tables (especially ones near headings that mention 'HEX') to extract
    rows that look like "<Name> ... #RRGGBB".
    Returns a list of {"name": str or None, "hex": "#RRGGBB"}.
    """
    results = []
    tables_to_check = []

    # Prefer tables following headings that mention 'hex'
    for h in team_soup.find_all(["h2", "h3", "h4"]):
        if "hex" in h.get_text(" ", strip=True).lower():
            sib = h.find_next_sibling()
            # walk to the first sibling that contains a table
            while sib and not (sib.find("table") if hasattr(sib, "find") else None):
                sib = sib.find_next_sibling()
            if sib:
                tbl = sib.find("table")
                if tbl:
                    tables_to_check.append(tbl)

    # Fallback: any table on the page
    if not tables_to_check:
        tables_to_check = team_soup.find_all("table")

    for tbl in tables_to_check:
        for tr in tbl.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]
            if not cells:
                continue
            name_cell = None
            hex_cell = None
            for c in cells:
                m = HEX_RE.search(c)
                if m:
                    hex_cell = "#" + m.group(1).upper()
                else:
                    if c and not name_cell:
                        name_cell = c
            if hex_cell:
                label = clean_label(name_cell or "")
                if label and not label.lower().startswith(("hex", "color")):
                    results.append({"name": label, "hex": hex_cell})
                else:
                    results.append({"name": None, "hex": hex_cell})

    # Deduplicate (name, hex)
    seen = set()
    dedup = []
    for item in results:
        key = (item["name"] or "", item["hex"])
        if key not in seen:
            seen.add(key)
            dedup.append(item)
    return dedup


def extract_colors(team: str, url: str) -> List[Dict[str, str]]:
    """
    Extract colors with BOTH a numeric 'label' ("Color N") and a human 'name' when available.
    Returns a list of {"label": "Color N", "name": <str>, "hex": "#RRGGBB"}.
    """
    s = soup(url)

    # Strategy A: parse dedicated HEX tables
    rows = extract_from_hex_table(s)

    # Strategy B: scan for "Name: #HEX" pairs
    if not rows:
        pairs = []
        for el in s.select("li, p, td, th, span, strong, em"):
            text = el.get_text(" ", strip=True)
            for m in LABEL_AND_HEX_RE.finditer(text):
                name = clean_label(m.group("label"))
                hexv = m.group("hex").upper()
                if name and not name.lower().startswith(("hex", "color")):
                    pairs.append({"name": name, "hex": hexv})
                else:
                    pairs.append({"name": None, "hex": hexv})
        rows = pairs

    # Strategy C: last resort—collect unique hexes without names
    if not rows:
        seen_hexes = []
        for el in s.select("li, p, td, th, span, strong, em"):
            text = el.get_text(" ", strip=True)
            for m in HEX_RE.finditer(text):
                hv = "#" + m.group(1).upper()
                if hv not in seen_hexes:
                    seen_hexes.append(hv)
        rows = [{"name": None, "hex": hv} for hv in seen_hexes]

    # Build final list with both numeric label and name (fallback to Color N as name if missing)
    out = []
    for idx, item in enumerate(rows, start=1):
        human = item["name"] or f"Color {idx}"
        out.append({
            "label": f"Color {idx}",
            "name": human,
            "hex": item["hex"]
        })
    return out


def main(out_path: str = "mlb_team_colors_with_labels.json") -> None:
    teams = find_mlb_team_links()
    data = {}
    for name, url in teams:
        try:
            colors = extract_colors(name, url)
            data[name] = colors
            print(f"✓ {name}: " + ", ".join([f"{c['label']}={c['name']} {c['hex']}" for c in colors]))
        except Exception as e:
            print(f"⚠️  {name}: failed to parse ({e})", file=sys.stderr)
        time.sleep(PAUSE_SEC)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(data)} MLB teams to {out_path}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "mlb_team_colors_with_labels.json"
    main(out_path=out)
