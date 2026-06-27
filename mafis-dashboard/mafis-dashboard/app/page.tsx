"use client";

import * as React from "react";
import { SiteHeader } from "@/components/dashboard/site-header";
import { TickerSearch } from "@/components/dashboard/ticker-search";
import { RecommendationCard } from "@/components/dashboard/recommendation-card";
import { FusedScoreCard } from "@/components/dashboard/fused-score-card";
import { TechnicalCard } from "@/components/dashboard/technical-card";
import { SentimentCard } from "@/components/dashboard/sentiment-card";
import { RiskCard } from "@/components/dashboard/risk-card";
import { RegimeCard } from "@/components/dashboard/regime-card";
import { ReasoningSection } from "@/components/dashboard/reasoning-section";
import { StockChart } from "@/components/dashboard/stock-chart";
import { TradeLogTable } from "@/components/dashboard/trade-log-table";
import { DashboardSkeleton } from "@/components/dashboard/dashboard-skeleton";
import { ErrorState } from "@/components/dashboard/error-state";
import { EmptyState } from "@/components/dashboard/empty-state";
import { fetchAnalysis } from "@/lib/api";
import { AnalyzeResponse, MafisApiError, TradeLogEntry } from "@/lib/types";

type ViewState = "idle" | "loading" | "success" | "error";

export default function Home() {
  const [state, setState] = React.useState<ViewState>("idle");
  const [data, setData] = React.useState<AnalyzeResponse | null>(null);
  const [errorMessage, setErrorMessage] = React.useState<string>("");
  const [lastTicker, setLastTicker] = React.useState<string>("");

  const abortRef = React.useRef<AbortController | null>(null);

  const runAnalysis = React.useCallback(async (ticker: string) => {
    // Cancel any in-flight request before starting a new one.
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    setLastTicker(ticker);
    setState("loading");
    setErrorMessage("");

    try {
      const result = await fetchAnalysis(ticker, controller.signal);
      setData(result);
      setState("success");
    } catch (err) {
      if (controller.signal.aborted) return; // superseded by a newer request
      const message =
        err instanceof MafisApiError ? err.message : "Something went wrong while analyzing this ticker.";
      setErrorMessage(message);
      setState("error");
    }
  }, []);

  // Placeholder trade log derived from the current analysis until a real
  // /backtest or /trades endpoint exists on the backend. Swap this out
  // for a fetched TradeLogEntry[] when that endpoint ships.
  const tradeLogEntries: TradeLogEntry[] = React.useMemo(() => {
    if (!data) return [];
    return [];
  }, [data]);

  return (
    <main className="min-h-screen bg-background">
      <SiteHeader isLive={state === "success"} />
      <TickerSearch onSearch={runAnalysis} isLoading={state === "loading"} initialValue={lastTicker} />

      <div className="container py-6">
        {state === "idle" && <EmptyState />}

        {state === "loading" && <DashboardSkeleton />}

        {state === "error" && (
          <ErrorState message={errorMessage} onRetry={() => runAnalysis(lastTicker)} />
        )}

        {state === "success" && data && (
          <div className="space-y-4">
            <RecommendationCard
              ticker={data.ticker}
              recommendation={data.recommendation}
              timestamp={data.timestamp}
            />

            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
              <FusedScoreCard fusedScore={data.fused_score} weights={data.weights} />
              <TechnicalCard technical={data.technical} />
              <SentimentCard sentiment={data.sentiment} />
              <RiskCard risk={data.risk} />
            </div>

            <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
              <div className="lg:col-span-1">
                <RegimeCard regime={data.regime} />
              </div>
              <div className="lg:col-span-2">
                <StockChart ticker={data.ticker} priceHistory={data.price_history} />
              </div>
            </div>

            <ReasoningSection reasoning={data.reasoning} />

            <TradeLogTable entries={tradeLogEntries} />
          </div>
        )}
      </div>
    </main>
  );
}
