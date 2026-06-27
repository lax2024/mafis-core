import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ActivitySquare } from "lucide-react";
import { TechnicalIndicators } from "@/lib/types";
import { formatNumber, formatSigned } from "@/lib/format";

interface TechnicalCardProps {
  technical: TechnicalIndicators;
}

function rsiZoneColor(rsi: number): string {
  if (rsi >= 70) return "text-bearish";
  if (rsi <= 30) return "text-bullish";
  return "text-caution";
}

function rsiZoneLabel(rsi: number): string {
  if (rsi >= 70) return "Overbought";
  if (rsi <= 30) return "Oversold";
  return "Neutral";
}

export function TechnicalCard({ technical }: TechnicalCardProps) {
  const rsi = technical.rsi ?? 50;

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <ActivitySquare className="h-3.5 w-3.5" />
          Technical Analysis
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <div className="mb-1 flex items-center justify-between">
            <span className="text-xs text-muted-foreground">RSI (14)</span>
            <span className={`font-mono text-xs font-semibold ${rsiZoneColor(rsi)}`}>
              {formatNumber(rsi, 1)} · {rsiZoneLabel(rsi)}
            </span>
          </div>
          <div className="relative h-1.5 w-full rounded-full bg-secondary">
            <div className="absolute inset-y-0 left-0 w-[30%] rounded-l-full bg-bullish/30" />
            <div className="absolute inset-y-0 right-0 w-[30%] rounded-r-full bg-bearish/30" />
            <div
              className="absolute top-1/2 h-3 w-1 -translate-y-1/2 rounded-sm bg-foreground"
              style={{ left: `calc(${Math.min(100, Math.max(0, rsi))}% - 2px)` }}
            />
          </div>
        </div>

        <dl className="grid grid-cols-2 gap-x-3 gap-y-3 border-t border-border pt-3">
          <div>
            <dt className="text-xs text-muted-foreground">MACD</dt>
            <dd className={`font-mono text-sm font-medium ${(technical.macd ?? 0) >= 0 ? "text-bullish" : "text-bearish"}`}>
              {formatSigned(technical.macd, 2)}
            </dd>
          </div>
          <div>
            <dt className="text-xs text-muted-foreground">Signal</dt>
            <dd className="font-mono text-sm font-medium">{formatNumber(technical.macd_signal, 2)}</dd>
          </div>
          <div>
            <dt className="text-xs text-muted-foreground">SMA (short)</dt>
            <dd className="font-mono text-sm font-medium">{formatNumber(technical.sma_short, 2)}</dd>
          </div>
          <div>
            <dt className="text-xs text-muted-foreground">SMA (long)</dt>
            <dd className="font-mono text-sm font-medium">{formatNumber(technical.sma_long, 2)}</dd>
          </div>
          <div>
            <dt className="text-xs text-muted-foreground">ATR</dt>
            <dd className="font-mono text-sm font-medium">{formatNumber(technical.atr, 2)}</dd>
          </div>
          <div>
            <dt className="text-xs text-muted-foreground">Trend</dt>
            <dd className="font-mono text-sm font-medium capitalize">{technical.trend || "—"}</dd>
          </div>
        </dl>
      </CardContent>
    </Card>
  );
}
