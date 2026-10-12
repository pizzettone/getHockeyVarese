# getHockeyVarese

Script Python per cercare su [Diretta.it](https://www.diretta.it) i risultati di **Hockey Varese** (o di un'altra squadra, se specificata).

## Requisiti

- Python 3.9+
- pip
- Browser Chromium per Playwright

## Installazione

```bash
pip install playwright
playwright install chromium
```

## Utilizzo

### Ricerca base (default: Hockey Varese)

```bash
python main.py
```

### Ricerca esplicita squadra

```bash
python main.py "Hockey Varese"
```

### Numero massimo risultati

```bash
python main.py "Hockey Varese" --max 10
```

### Modalità con browser visibile (debug)

```bash
python main.py "Hockey Varese" --show
```

## Come funziona

1. Apre la pagina di ricerca di Diretta.it.
2. Cerca link squadra (`/squadra/`).
3. Seleziona la corrispondenza migliore.
4. Apre la sezione `/risultati/` della squadra.
5. Estrae e stampa gli ultimi match trovati.

## Note importanti

- Diretta.it è un sito dinamico: i selettori HTML/CSS possono cambiare nel tempo.
- Se un giorno lo script smette di funzionare, probabilmente vanno aggiornati i selettori nel codice.
- In caso di più squadre simili, viene scelta la prima corrispondenza utile.

## Risoluzione problemi

### `ModuleNotFoundError: No module named 'playwright'`

Installa il pacchetto:

```bash
pip install playwright
```

### Browser non installato / errore Playwright

Installa Chromium:

```bash
playwright install chromium
```

### Nessun risultato trovato

- Prova con nome più specifico della squadra.
- Avvia con `--show` per vedere cosa succede nel browser.

## Disclaimer

Usa lo script in modo responsabile e nel rispetto dei termini del sito.
