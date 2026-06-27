"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ListOrdered } from "lucide-react";
import { TradeLogEntry } from "@/lib/types";
import { formatPrice, formatPercent } from "@/lib/format";

interface TradeLogTableProps {
  entries: TradeLogEntry[];
}

function recBadgeVariant(rec: string): "bullish" | "bearish" | "caution" {
  const r = rec.toUpperCase();
  if (r === "BUY") return "bullish";
  if (r === "SELL") return "bearish";
  return "caution";
}

function outcomeBadgeVariant(outcome?: string): "bullish" | "bearish" | "muted" {
  if (outcome === "WIN") return "bullish";
  if (outcome === "LOSS") return "bearish";
  return "muted";
}

export function TradeLogTable({ entries }: TradeLogTableProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <ListOrdered className="h-3.5 w-3.5" />
          Trade Log
        </CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        {entries.length === 0 ? (
          <div className="flex flex-col items-center justify-center gap-2 py-12 text-center">
            <ListOrdered className="h-8 w-8 text-muted-foreground/50" />
            <p className="text-sm text-muted-foreground">No trade history yet.</p>
            <p className="max-w-sm text-xs text-muted-foreground/70">
              This table is wired to render a <code className="font-mono">TradeLogEntry[]</code>{" "}
              — connect it to your backtesting endpoint to populate it.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-border text-xs uppercase tracking-wider text-muted-foreground">
                  <th className="px-4 py-2 font-medium">Date</th>
                  <th className="px-4 py-2 font-medium">Ticker</th>
                  <th className="px-4 py-2 font-medium">Signal</th>
                  <th className="px-4 py-2 text-right font-medium">Price</th>
                  <th className="px-4 py-2 text-right font-medium">Return</th>
                  <th className="px-4 py-2 font-medium">Outcome</th>
                </tr>
              </thead>
              <tbody className="font-mono">
                {entries.map((entry, i) => (
                  <tr
                    key={`${entry.ticker}-${entry.date}-${i}`}
                    className="border-b border-border/60 last:border-0 hover:bg-secondary/30"
                  >
                    <td className="px-4 py-2.5 text-muted-foreground">{entry.date}</td>
                    <td className="px-4 py-2.5 font-medium">{entry.ticker}</td>
                    <td className="px-4 py-2.5">
                      <Badge variant={recBadgeVariant(entry.recommendation)}>
                        {entry.recommendation}
                      </Badge>
                    </td>
                    <td className="px-4 py-2.5 text-right">{formatPrice(entry.price)}</td>
                    <td
                      className={`px-4 py-2.5 text-right ${
                        (entry.return_pct ?? 0) >= 0 ? "text-bullish" : "text-bearish"
                      }`}
                    >
                      {entry.return_pct !== undefined ? formatPercent(entry.return_pct) : "—"}
                    </td>
                    <td className="px-4 py-2.5">
                      {entry.outcome && (
                        <Badge variant={outcomeBadgeVariant(entry.outcome)}>{entry.outcome}</Badge>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
