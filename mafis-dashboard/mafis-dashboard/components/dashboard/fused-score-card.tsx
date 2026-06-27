import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Gauge } from "lucide-react";
import { AgentWeights } from "@/lib/types";
import { formatSigned, formatPercent, scoreToGaugePosition, scoreColor } from "@/lib/format";

interface FusedScoreCardProps {
  fusedScore: number;
  weights?: AgentWeights;
}

const AGENT_LABELS: Record<string, string> = {
  technical: "Technical",
  sentiment: "Sentiment",
  risk: "Risk",
};

export function FusedScoreCard({ fusedScore, weights }: FusedScoreCardProps) {
  const gaugePos = scoreToGaugePosition(fusedScore);

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <Gauge className="h-3.5 w-3.5" />
          Fused Score
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-baseline gap-2">
          <span className={`font-mono text-3xl font-bold ${scoreColor(fusedScore)}`}>
            {formatSigned(fusedScore, 3)}
          </span>
          <span className="text-xs text-muted-foreground">range −1.00 to +1.00</span>
        </div>

        {/* Gauge bar: bearish (left) -> caution (center) -> bullish (right) */}
        <div className="relative h-2 w-full overflow-hidden rounded-full bg-gradient-to-r from-bearish via-caution to-bullish">
          <div
            className="absolute top-1/2 h-4 w-1.5 -translate-y-1/2 rounded-sm bg-foreground shadow-[0_0_0_2px_hsl(var(--background))]"
            style={{ left: `calc(${gaugePos}% - 3px)` }}
            aria-hidden
          />
        </div>
        <div className="flex justify-between text-[10px] uppercase tracking-wider text-muted-foreground">
          <span>Bearish</span>
          <span>Neutral</span>
          <span>Bullish</span>
        </div>

        {weights && (
          <div className="space-y-2 border-t border-border pt-3">
            <p className="text-[10px] uppercase tracking-wider text-muted-foreground">
              Adaptive Agent Weights
            </p>
            {Object.entries(weights).map(([key, val]) => (
              <div key={key} className="flex items-center gap-2">
                <span className="w-20 shrink-0 text-xs text-muted-foreground">
                  {AGENT_LABELS[key] || key}
                </span>
                <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-secondary">
                  <div
                    className="h-full rounded-full bg-primary"
                    style={{ width: `${Math.min(100, Math.max(0, val * 100))}%` }}
                  />
                </div>
                <span className="w-10 shrink-0 text-right font-mono text-xs text-muted-foreground">
                  {formatPercent(val, 0)}
                </span>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
