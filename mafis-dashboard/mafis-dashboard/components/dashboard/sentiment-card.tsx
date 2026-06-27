import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Newspaper } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { SentimentResult } from "@/lib/types";
import { formatNumber, formatPercent, sentimentColor } from "@/lib/format";

interface SentimentCardProps {
  sentiment: SentimentResult;
}

function badgeVariantFor(label: string | undefined): "bullish" | "bearish" | "caution" | "muted" {
  switch ((label || "").toLowerCase()) {
    case "positive":
      return "bullish";
    case "negative":
      return "bearish";
    case "neutral":
      return "caution";
    default:
      return "muted";
  }
}

export function SentimentCard({ sentiment }: SentimentCardProps) {
  const headlines = sentiment.top_headlines ?? [];

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <Newspaper className="h-3.5 w-3.5" />
          News Sentiment (FinBERT)
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <Badge variant={badgeVariantFor(sentiment.label)}>{sentiment.label || "unknown"}</Badge>
          <span className={`font-mono text-sm font-semibold ${sentimentColor(sentiment.label)}`}>
            score {formatNumber(sentiment.score, 2)}
          </span>
        </div>

        {sentiment.confidence !== undefined && (
          <div>
            <div className="mb-1 flex justify-between text-xs text-muted-foreground">
              <span>Model confidence</span>
              <span className="font-mono">{formatPercent(sentiment.confidence)}</span>
            </div>
            <div className="h-1.5 w-full overflow-hidden rounded-full bg-secondary">
              <div
                className="h-full rounded-full bg-primary"
                style={{ width: `${Math.min(100, Math.max(0, sentiment.confidence * 100))}%` }}
              />
            </div>
          </div>
        )}

        {sentiment.headline_count !== undefined && (
          <p className="text-xs text-muted-foreground">
            Based on{" "}
            <span className="font-mono font-medium text-foreground">{sentiment.headline_count}</span>{" "}
            recent headlines
          </p>
        )}

        {headlines.length > 0 && (
          <ul className="space-y-1.5 border-t border-border pt-3">
            {headlines.slice(0, 4).map((h, i) => (
              <li key={i} className="line-clamp-2 text-xs leading-relaxed text-muted-foreground">
                <span className="text-foreground">·</span> {h}
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
