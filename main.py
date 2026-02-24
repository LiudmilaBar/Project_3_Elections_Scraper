import csv
import sys
from typing import Dict, List

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.volby.cz/pls/ps2017nss/"


def get_soup(url: str) -> BeautifulSoup:
    """Stáhne stránku a vrátí BeautifulSoup objekt."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def clean_number(value: str) -> str:
    """Odstraní mezery a neviditelné znaky z čísla."""
    return value.replace("\xa0", "").replace(" ", "").strip()


def get_towns_list(url: str) -> List[Dict[str, str]]:
    """Získá seznam obcí z okresní tabulky."""
    soup = get_soup(url)
    towns: List[Dict[str, str]] = []

    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 2:
            link = cells[0].find("a")
            if link:
                towns.append(
                    {
                        "code": cells[0].text.strip(),
                        "name": cells[1].text.strip(),
                        "url": BASE_URL + link["href"],
                    }
                )
    return towns


def get_voting_data(url: str) -> Dict[str, str]:
    """Získá výsledky hlasování pro jednu obec."""
    soup = get_soup(url)
    tables = soup.find_all("table")
    results: Dict[str, str] = {}

    # Základní údaje
    for row in tables[0].find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 7:
            results["registered"] = clean_number(cells[3].text)
            results["envelopes"] = clean_number(cells[4].text)
            results["valid"] = clean_number(cells[7].text)

    # Výsledky stran
    for table in tables[1:]:
        for row in table.find_all("tr"):
            headers = row.find_all("th")
            cells = row.find_all("td")
            if len(headers) >= 2 and len(cells) >= 2:
                party = headers[1].text.strip()
                votes = clean_number(cells[1].text)
                if party:
                    results[party] = votes

    return results


def normalize_data(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Zajistí, že všechny řádky mají stejné sloupce."""
    all_keys = set()
    for row in data:
        all_keys.update(row.keys())

    for row in data:
        for key in all_keys:
            row.setdefault(key, "0")

    return data


def scrape_district(url: str) -> List[Dict[str, str]]:
    """Vyscrapuje všechny obce v daném okrese."""
    print("Stahuji seznam obcí...")
    towns = get_towns_list(url)
    print(f"Nalezeno obcí: {len(towns)}\n")

    results: List[Dict[str, str]] = []

    for i, town in enumerate(towns, 1):
        print(f"Zpracovávám ({i}/{len(towns)}): {town['name']}")
        voting = get_voting_data(town["url"])

        town_result = {
            "code": town["code"],
            "location": town["name"],
        }
        town_result.update(voting)
        results.append(town_result)

    return results


def save_to_csv(data: List[Dict[str, str]], filename: str) -> None:
    """Uloží data do CSV souboru."""
    if not data:
        print("Žádná data k uložení.")
        return

    basic_keys = ["code", "location", "registered", "envelopes", "valid"]
    party_keys = [
        key for key in data[0].keys() if key not in basic_keys
    ]

    headers = basic_keys + party_keys

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    print(f"\nData uložena do: {filename}")


def main() -> None:
    """Hlavní funkce programu."""
    if len(sys.argv) != 3:
        print("Použití: python main.py <URL_okresu> <vystupni_soubor.csv>")
        print(
            "Příklad:\n"
            "python main.py "
            "'https://www.volby.cz/pls/ps2017nss/"
            "ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101' vysledky.csv"
        )
        sys.exit(1)

    district_url = sys.argv[1]
    output_file = sys.argv[2]

    print("Elections Scraper 2017")
    print("=" * 50)

    results = scrape_district(district_url)
    results = normalize_data(results)
    save_to_csv(results, output_file)

    print(f"Celkem zpracováno obcí: {len(results)}")
    print("=" * 50)


if __name__ == "__main__":
    main()