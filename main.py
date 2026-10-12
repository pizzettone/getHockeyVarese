#!/usr/bin/env python3
"""Cerca i risultati di Hockey Varese su diretta.it.

Installazione:
    pip install playwright
    playwright install chromium

Uso:
    python main.py "Hockey Varese" --max 10
"""

import argparse
import re
import sys
from urllib.parse import quote

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

BASE_URL = "https://www.diretta.it"


def accept_cookies(page):
    try:
        page.locator("#onetrust-accept-btn-handler").click(timeout=4000)
    except PWTimeout:
        pass
    except Exception:
        pass


def search_team_url(page, query: str):
    page.goto(f"{BASE_URL}/cerca/?q={quote(query)}", wait_until="domcontentloaded")
    accept_cookies(page)
    page.wait_for_timeout(2000)

    links = page.eval_on_selector_all(
        "a[href*='/squadra/']",
        "els => els.map(e => ({ href: e.href, text: (e.innerText || '').trim() }))",
    )

    if not links:
        return None

    q = query.lower()
    q_parts = [p for p in re.split(r"\s+", q) if p]

    matches = []
    for item in links:
        text = item["text"].lower()
        href = item["href"].lower()
        if all(part in text or part in href for part in q_parts):
            matches.append(item["href"])

    if matches:
        return matches[0]

    return links[0]["href"]


def get_results_for_team(page, team_url: str, max_results: int):
    page.goto(f"{team_url.rstrip('/')}/risultati/", wait_until="domcontentloaded")
    accept_cookies(page)

    try:
        page.wait_for_selector("div.event__match", timeout=15000)
    except PWTimeout:
        return []

    rows = page.eval_on_selector_all(
        "div.event__match",
        """els => els.map(e => {
            const q = (s) => {
                const el = e.querySelector(s);
                return el ? (el.innerText || '').trim() : '';
            };
            return {
                time: q('.event__time'),
                home: q('.event__homeParticipant') || q('.event__participant--home'),
                away: q('.event__awayParticipant') || q('.event__participant--away'),
                score_home: q('.event__score--home'),
                score_away: q('.event__score--away'),
            };
        })""",
    )

    output = []
    for row in rows[:max_results]:
        time = re.sub(r"\s+", " ", row.get("time", "")).strip()
        home = re.sub(r"\s+", " ", row.get("home", "")).strip()
        away = re.sub(r"\s+", " ", row.get("away", "")).strip()
        sh = re.sub(r"\s+", " ", row.get("score_home", "")).strip()
        sa = re.sub(r"\s+", " ", row.get("score_away", "")).strip()

        if not home and not away:
            continue

        output.append(f"{time:<14} {home} {sh} - {sa} {away}")

    return output


def main():
    parser = argparse.ArgumentParser(description="Cerca risultati di Hockey Varese su Diretta.it")
    parser.add_argument("team", nargs="?", default="Hockey Varese", help="Nome da cercare")
    parser.add_argument("--max", type=int, default=10, help="Numero massimo di risultati da mostrare")
    parser.add_argument("--show", action="store_true", help="Mostra il browser durante la ricerca")
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.show)
        context = browser.new_context(locale="it-IT")
        page = context.new_page()

        try:
            team_url = search_team_url(page, args.team)
            if not team_url:
                print(f"Nessuna squadra trovata per: {args.team}")
                return 1

            print(f"Squadra trovata: {team_url}\n")
            results = get_results_for_team(page, team_url, args.max)

            if not results:
                print("Nessun risultato trovato.")
                return 0

            for item in results:
                print(item)
            return 0
        except Exception as exc:
            print(f"Errore: {exc}", file=sys.stderr)
            return 1
        finally:
            browser.close()


if __name__ == "__main__":
    raise SystemExit(main())
