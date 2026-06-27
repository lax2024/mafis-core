// Types mirroring the MAFIS FastAPI backend response contract.
// Keep this file in sync with the backend's Pydantic response models.

export type Recommendation = "BUY" | "SELL" | "HOLD";

export type Regime = "BULLISH" | "BEARISH" | "SIDEWAYS";

export interface TechnicalIndicators {
  rsi: number;
  macd: number;
  macd_signal?: number;
  sma_short?: number;
  sma_long?: number;
  atr: number;
  trend?: string;
  // Allow the backend to add more indicators without breaking the UI.
  [key: string]: number | string | undefined;
}

export interface SentimentResult {
  label: "positive" | "negative" | "neutral" | string;
  score: number; // -1..1 or 0..1 depending on backend normalization
  confidence?: number;
  headline_count?: number;
  top_headlines?: string[];
  [key: string]: unknown;
}

export interface RiskMetrics {
  var_95: number;
  cvar_95: number;
  sharpe_ratio: number;
  max_drawdown: number;
  volatility?: number;
  risk_level?: "LOW" | "MEDIUM" | "HIGH" | string;
  [key: string]: number | string | undefined;
}

export interface RegimeInfo {
  label: Regime | string;
  confidence: number;
  description?: string;
}

export interface AgentWeights {
  technical: number;
  sentiment: number;
  risk: number;
  [key: string]: number;
}

export interface AnalyzeResponse {
  ticker: string;
  recommendation: Recommendation | string;
  fused_score: number; // expected roughly -1..1, negative = bearish, positive = bullish
  technical: TechnicalIndicators;
  sentiment: SentimentResult;
  risk: RiskMetrics;
  regime: RegimeInfo;
  reasoning: string[];
  weights?: AgentWeights;
  price_history?: PricePoint[];
  timestamp?: string;
}

export interface PricePoint {
  date: string;
  close: number;
  volume?: number;
}

// Shape for a future /backtest endpoint - kept here so the trade log table
// and backtest dashboard can be wired up without touching shared types again.
export interface TradeLogEntry {
  date: string;
  ticker: string;
  recommendation: Recommendation | string;
  price: number;
  outcome?: "WIN" | "LOSS" | "OPEN" | string;
  return_pct?: number;
  notes?: string;
}

export class MafisApiError extends Error {
  status?: number;
  constructor(message: string, status?: number) {
    super(message);
    this.name = "MafisApiError";
    this.status = status;
  }
}
