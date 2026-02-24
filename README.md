# Elections Scraper 2017

## Popis projektu

Projekt slouží k extrahování výsledků voleb do Poslanecké sněmovny ČR v roce 2017 z webu volby.cz.

Program stáhne výsledky hlasování pro všechny obce vybraného územního celku a uloží je do CSV souboru.

## Instalace knihoven

Knihovny, které jsou použity v kodu jsou uložené v souboru requirements.txt  

Pro instalaci doporučuji použít virtuální prostředí.

### Vytvoření virtuálního prostředí:

python -m venv venv

Aktivace

Windows: venv\Scripts\activate

Linux / Mac: source venv/bin/activate

### Instalace závislostí

pip install -r requirements.txt

## Spuštění projektu

Program se spouští se dvěma povinnými argumenty:

1. URL územního celku

2. Název výstupního CSV souboru

python main.py <URL_okresu> <vystupni_soubor.csv>

Příklad

'python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_benesov.csv'

Následné se vám stáhnou výsledky jako soubor s připonou .csv

Pokud nejsou zadány oba argumenty, program se ukončí a zobrazí nápovědu:
Použití: 'python main.py <URL_okresu> <vystupni_soubor.csv>'
Příklad:
'python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky.csv'

## Ukázka projektu:

Vysledky hlasování pro okres Benešov:
1. argument https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
2. argument vysledky_benesov.csv
Spuštění programu: 'python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_benesov.csv'
Průběh stahování:
Elections Scraper 2017
Stahuji seznam obcí...
Nalezeno obcí: 114
Zpracovávám 
Data uložena do: vysledky_benesov.csv
Celkem zpracováno obcí: 114

## Částečný výstup:
code,location,registered,envelopes,valid
529303,Benešov,13104,8485,8437
532568,Bernartice,191,148,148
530743,Bílkovice,170,121,118

