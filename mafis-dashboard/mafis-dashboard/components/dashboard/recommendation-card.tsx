import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { recommendationColor, recommendationBg } from "@/lib/format";

interface RecommendationCardProps {
  ticker: string;
  recommendation: string;
  timestamp?: string;
}

const ICONS: Record<string, typeof TrendingUp> = {
  BUY: TrendingUp,
  SELL: TrendingDown,
  HOLD: Minus,
};

export function RecommendationCard({ ticker, recommendation, timestamp }: RecommendationCardProps) {
  const rec = (recommendation || "").toUpperCase();
  const Icon = ICONS[rec] || Minus;

  return (
    <Card className={`${recommendationBg(rec)} border`}>
      <CardContent className="flex items-center justify-between py-6">
        <div>
          <p className="text-xs uppercase tracking-wider text-muted-foreground">
            MAFIS Recommendation · {ticker}
          </p>
          <p className={`mt-1 font-mono text-4xl font-bold tracking-tight ${recommendationColor(rec)}`}>
            {rec || "—"}
          </p>
          {timestamp && (
            <p className="mt-1 text-xs text-muted-foreground">
              As of {new Date(timestamp).toLocaleString("en-IN")}
            </p>
          )}
        </div>
        <Icon className={`h-12 w-12 shrink-0 ${recommendationColor(rec)}`} strokeWidth={1.5} />
      </CardContent>
    </Card>
  );
}
