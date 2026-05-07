# App 1 — Realtime Stock Dashboard

Live price streaming for up to 50 companies using Server-Sent Events (SSE).  
Single-file HTML app — no installation, no server needed.

---

## Prerequisites

- Any modern web browser (Chrome 60+, Firefox 55+, Edge 79+, Safari 13+)
- A valid API key from `https://add.piotrkojalowicz.dev/`
- Python 3 (for the local proxy)

---

## Installation

```bash
git clone <repository-url>
```

---

## Configuration

The API key is entered at runtime via the UI form — it is **never stored in any file**.  
On your first visit it will be stored in your browser's `localStorage` for convenience.  
To clear it, open DevTools → Application → Local Storage → delete `add_api_key`.

> The key is passed as a query parameter (`?api_key=...`) — the standard browser-compatible method for SSE authentication.

---

## How to Run

The API does not allow cross-origin browser requests, so use the local proxy and a local file server.

```bash
# Terminal 1: start the proxy
python proxy_server.py

# Terminal 2: serve the files
python -m http.server 8080
```

Open: `http://localhost:8080/app1-dashboard/`

---

## How It Works

1. Enter your API key and select one or more tickers from the 50-company list
2. Click **Connect & Stream Live**
3. The app opens an `EventSource` connection to `/stream?ticker=X` for each selected ticker
4. Each card updates in real-time showing:
   - **Ticker symbol** and company name
   - **Current price** with ▲/▼ change indicator and percentage
   - **Timestamp** of the last tick
   - **Volume** and sequence number
   - **Sparkline chart** of the last 30 price ticks (green = rising, red = falling)
5. On connection error, the app automatically reconnects after 5 seconds

---

## API Endpoint Used

| Endpoint | Purpose |
|----------|---------|
| `GET /api/stream?ticker=X&api_key=KEY` | Live SSE tick stream for ticker X (via local proxy) |

Events format:
```
event: tick
data: {"ticker":"ACME","ts":"2026-05-07T15:30:00+02:00","price":123.45,"currency":"PLN","volume":1200,"seq":42}
```

---

## Screenshots

See the [`screenshots/`](screenshots/) folder.
