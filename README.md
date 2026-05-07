# s34849_kafka — Real-time Stock Data (Kafka / SSE)

**Student:** s34849  
**Assignment:** Additional Assignment — Real-time Stock Data  
**API Base:** `https://add.piotrkojalowicz.dev`

---

## Overview

Two browser-based apps that consume live fictitious stock price ticks for 50 companies from a Kafka-backed SSE API.  
Both apps are **zero-dependency single HTML files** — just open in any modern browser.

| App | Folder | Description |
|-----|--------|-------------|
| #1 Realtime Dashboard | [`app1-dashboard/`](app1-dashboard/) | Live SSE stream · per-ticker sparkline charts · price-change indicators |
| #2 History Downloader | [`app2-history/`](app2-history/) | Accumulates tick history · multi-line chart · table view · CSV/JSON export |

---

## Quick Start

1. **Get your API key** from `https://add.piotrkojalowicz.dev/` (class password: `A@d-$01`)
2. **Start the local proxy** (required because the API does not allow browser CORS):
    ```bash
    python proxy_server.py
    ```
3. **Serve the files**:
    ```bash
    python -m http.server 8080
    ```
4. **Open** `http://localhost:8080/app1-dashboard/` or `http://localhost:8080/app2-history/`
5. **Paste your API key** into the UI form — it is never stored in the code
6. Select tickers and connect

---

## API Endpoints Used

| Endpoint | Used by |
|----------|---------|
| `GET /api/stream?ticker=X` | App 1 (live updates), App 2 (history collection) |
| `GET /api/latest?ticker=X` | App 2 (optional fallback polling) |

Authentication: `api_key=<KEY>` query parameter (browser-compatible). The local proxy also forwards
the key via `X-API-Key` for compatibility.

---

## Repository Structure

```
s34849_kafka/
├── .gitignore
├── README.md
├── app1-dashboard/
│   ├── index.html          ← App 1 (open in browser)
│   ├── README.md
│   └── screenshots/
└── app2-history/
    ├── index.html          ← App 2 (open in browser)
    ├── README.md
    └── screenshots/
```

---

## Rate Limit Note

The API limits requests per key (after the first few, about 1 request every 10 seconds). If you
open many streams at once, you can hit HTTP 429. Start with 1-2 tickers and add more slowly.

---

## Security Note

The API key is entered at runtime via the browser UI form.  
It is stored in `localStorage` for convenience (cleared by closing private browsing).  
It is **never hardcoded**, never in any file committed to this repository.
