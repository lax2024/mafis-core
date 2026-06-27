# MAFIS Dashboard

Frontend for the Multi-Agent Financial Intelligence System. Next.js 14 (App Router) + TypeScript + Tailwind + shadcn/ui, styled as a dark financial terminal.

## Setup

```bash
npm install
cp .env.local.example .env.local
npm run dev
```

Open http://localhost:3000. Make sure your FastAPI backend is running on the URL set in `.env.local` (defaults to `http://127.0.0.1:8000`) and that CORS is enabled for `http://localhost:3000`:

```python
# in your FastAPI app
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

## Structure

```
app/
  layout.tsx          Root layout, fonts, metadata
  page.tsx             Main dashboard - owns fetch state, renders all cards
  globals.css          Theme tokens (dark terminal palette)

components/ui/          Generic shadcn/ui primitives (Card, Badge, Button, Input, Skeleton, Tabs)
components/dashboard/   MAFIS-specific components, one file per card:
  site-header.tsx
  ticker-search.tsx
  recommendation-card.tsx
  fused-score-card.tsx
  technical-card.tsx
  sentiment-card.tsx
  risk-card.tsx
  regime-card.tsx
  reasoning-section.tsx
  stock-chart.tsx
  trade-log-table.tsx
  dashboard-skeleton.tsx   loading state
  error-state.tsx          error state
  empty-state.tsx          pre-search state

lib/
  types.ts             AnalyzeResponse + all nested types - keep in sync with backend Pydantic models
  api.ts                fetchAnalysis() - typed fetch wrapper with timeout/abort/error handling
  format.ts             number/percent/color formatting helpers shared by cards
  utils.ts              cn() class merger used by shadcn components
```

## Backend contract assumed

`GET /analyze/{ticker}` → `AnalyzeResponse` (see `lib/types.ts`). Two fields are optional and degrade gracefully if your backend doesn't send them yet:

- `price_history: PricePoint[]` — populates the stock chart. Without it, the chart shows an empty state telling you what shape to send.
- `weights: AgentWeights` — populates the per-agent weight bars under the fused score gauge. Without it, the gauge still renders.

## Extending for the backtesting dashboard

`lib/types.ts` already defines `TradeLogEntry`, and `components/dashboard/trade-log-table.tsx` already renders an array of them — it's just fed `[]` from `app/page.tsx` right now. To wire up a `/backtest/{ticker}` endpoint:

1. Add `fetchBacktest(ticker)` to `lib/api.ts` following the same pattern as `fetchAnalysis`.
2. Call it from `app/page.tsx` (or a new `app/backtest/page.tsx` route) and pass the result into `<TradeLogTable entries={...} />`.
3. The `Tabs` primitive (`components/ui/tabs.tsx`) is already in the project if you want a tabbed Live Analysis / Backtest view on one page instead of a separate route.

## Notes

- This was hand-built and type-checked (`tsc` in multi-file project mode against all 26 source files, zero errors) but **not run through a live `next build`** — the sandbox used to produce it had no network access to the npm registry. Run `npm run build` yourself before deploying; it's standard Next.js 14 so it should build clean, but verify on your machine.
- No light mode — the dark terminal theme is the only theme by design (see `app/globals.css`).
