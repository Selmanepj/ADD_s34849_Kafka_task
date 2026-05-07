# App 2 — Stock History Downloader / Viewer

Collects live tick data via SSE streaming, displays it as an interactive multi-line chart and
sortable table, and lets you export the data as CSV or JSON.  
Single-file HTML app — no installation, no server needed.

---

## Prerequisites

- Any modern web browser (Chrome 60+, Firefox 55+, Edge 79+, Safari 13+)
- A valid API key from `https://add.piotrkojalowicz.dev/`

No Python, Node.js, or any other runtime required.

---

## Installation

```bash
git clone <repository-url>
# No npm install or pip install needed
```

---

## Configuration

The API key is entered at runtime via the sidebar form — it is **never stored in any file**.  
On first use it is saved to browser `localStorage` for convenience.  
To clear it: DevTools → Application → Local Storage → delete `add_api_key`.

---

## How to Run

Open the file directly in your browser:

```
app2-history/index.html
```

Double-click in Explorer, or serve locally:

```bash
# Python 3
python -m http.server 8080
# then open http://localhost:8080/app2-history/
```

---

## How to Use

1. **Enter your API key** in the sidebar
2. **Select tickers** from the list (use the search box to filter; "Top 5" picks a preset)
3. **Set the view range** with the slider (1–10 minutes — filters chart and table display)
4. Click **▶ Start Collecting**
5. The app opens SSE streams for each selected ticker and accumulates tick data
6. The **chart** and **table** auto-refresh every 2 seconds, filtered to the selected time range
7. When you have enough data, click **Download CSV** or **Download JSON** to export

---

## API Endpoint Used

| Endpoint | Purpose |
|----------|---------|
| `GET /api/stream?ticker=X&api_key=KEY` | SSE live stream — used to accumulate history |

Data retention note: the server discards ticks older than ~10 minutes, so the app collects
real-time data and you should download before the session ends.

---

## Export Format

**CSV** — `stocks_history.csv`:
```
ticker,ts,price,currency,volume,seq
ACME,2026-05-07T15:30:00+02:00,123.45,PLN,1200,42
```

**JSON** — `stocks_history.json`:
```json
[
  {"ticker":"ACME","ts":"2026-05-07T15:30:00+02:00","price":123.45,"currency":"PLN","volume":1200,"seq":42}
]
```

Both exports are filtered to the currently selected time range.

---

## Screenshots

See the [`screenshots/`](screenshots/) folder.
