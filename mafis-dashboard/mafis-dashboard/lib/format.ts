import { Recommendation, Regime } from "./types";

export function formatNumber(value: number | undefined | null, decimals = 2): string {
  if (value === undefined || value === null || Number.isNaN(value)) return "—";
  return value.toFixed(decimals);
}

export function formatPercent(value: number | undefined | null, decimals = 1): string {
  if (value === undefined || value === null || Number.isNaN(value)) return "—";
  return `${(value * 100).toFixed(decimals)}%`;
}

export function formatSigned(value: number | undefined | null, decimals = 2): string {
  if (value === undefined || value === null || Number.isNaN(value)) return "—";
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(decimals)}`;
}

export function formatPrice(value: number | undefined | null): string {
  if (value === undefined || value === null || Number.isNaN(value)) return "—";
  return value.toLocaleString("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 2,
  });
}

/** Tailwind text-color class for a recommendation badge/text. */
export function recommendationColor(rec: string | undefined): string {
  switch ((rec || "").toUpperCase()) {
    case "BUY":
      return "text-bullish";
    case "SELL":
      return "text-bearish";
    case "HOLD":
      return "text-caution";
    default:
      return "text-muted-foreground";
  }
}

export function recommendationBg(rec: string | undefined): string {
  switch ((rec || "").toUpperCase()) {
    case "BUY":
      return "bg-bullish/10 border-bullish/30";
    case "SELL":
      return "bg-bearish/10 border-bearish/30";
    case "HOLD":
      return "bg-caution/10 border-caution/30";
    default:
      return "bg-muted border-border";
  }
}

export function regimeColor(regime: string | undefined): string {
  switch ((regime || "").toUpperCase()) {
    case "BULLISH":
      return "text-bullish";
    case "BEARISH":
      return "text-bearish";
    case "SIDEWAYS":
      return "text-caution";
    default:
      return "text-muted-foreground";
  }
}

/** Maps a fused score in roughly [-1, 1] to a position 0-100 for the gauge bar. */
export function scoreToGaugePosition(score: number): number {
  const clamped = Math.max(-1, Math.min(1, score));
  return ((clamped + 1) / 2) * 100;
}

export function scoreColor(score: number): string {
  if (score > 0.15) return "text-bullish";
  if (score < -0.15) return "text-bearish";
  return "text-caution";
}

export function riskLevelColor(level: string | undefined): string {
  switch ((level || "").toUpperCase()) {
    case "LOW":
      return "text-bullish border-bullish/30 bg-bullish/10";
    case "MEDIUM":
      return "text-caution border-caution/30 bg-caution/10";
    case "HIGH":
      return "text-bearish border-bearish/30 bg-bearish/10";
    default:
      return "text-muted-foreground border-border bg-muted";
  }
}

export function sentimentColor(label: string | undefined): string {
  switch ((label || "").toLowerCase()) {
    case "positive":
      return "text-bullish";
    case "negative":
      return "text-bearish";
    case "neutral":
      return "text-caution";
    default:
      return "text-muted-foreground";
  }
}
