"use client";

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { LineChart as LineChartIcon } from "lucide-react";
import { PricePoint } from "@/lib/types";
import { formatPrice } from "@/lib/format";

interface StockChartProps {
  ticker: string;
  priceHistory?: PricePoint[];
}

function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-sm border border-border bg-popover px-3 py-2 text-xs shadow-md">
      <p className="text-muted-foreground">{label}</p>
      <p className="font-mono font-semibold text-foreground">{formatPrice(payload[0].value)}</p>
    </div>
  );
}

export function StockChart({ ticker, priceHistory }: StockChartProps) {
  const hasData = priceHistory && priceHistory.length > 1;
  const isUp =
    hasData && priceHistory[priceHistory.length - 1].close >= priceHistory[0].close;

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <LineChartIcon className="h-3.5 w-3.5" />
          {ticker} Price Chart
        </CardTitle>
      </CardHeader>
      <CardContent>
        {hasData ? (
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={priceHistory} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="priceFill" x1="0" y1="0" x2="0" y2="1">
                    <stop
                      offset="5%"
                      stopColor={isUp ? "hsl(var(--bullish))" : "hsl(var(--bearish))"}
                      stopOpacity={0.35}
                    />
                    <stop
                      offset="95%"
                      stopColor={isUp ? "hsl(var(--bullish))" : "hsl(var(--bearish))"}
                      stopOpacity={0}
                    />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis
                  dataKey="date"
                  tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
                  tickLine={false}
                  axisLine={{ stroke: "hsl(var(--border))" }}
                  minTickGap={32}
                />
                <YAxis
                  tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
                  tickLine={false}
                  axisLine={false}
                  domain={["auto", "auto"]}
                  width={56}
                />
                <Tooltip content={<CustomTooltip />} />
                <Area
                  type="monotone"
                  dataKey="close"
                  stroke={isUp ? "hsl(var(--bullish))" : "hsl(var(--bearish))"}
                  strokeWidth={1.75}
                  fill="url(#priceFill)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <div className="flex h-72 flex-col items-center justify-center gap-2 rounded-sm border border-dashed border-border text-center">
            <LineChartIcon className="h-8 w-8 text-muted-foreground/50" />
            <p className="text-sm text-muted-foreground">No price history returned for {ticker}.</p>
            <p className="max-w-xs text-xs text-muted-foreground/70">
              Add a <code className="font-mono">price_history</code> array to the{" "}
              <code className="font-mono">/analyze</code> response to populate this chart.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
