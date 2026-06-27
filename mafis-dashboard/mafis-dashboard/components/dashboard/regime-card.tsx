import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Waves } from "lucide-react";
import { RegimeInfo } from "@/lib/types";
import { regimeColor, formatPercent } from "@/lib/format";

interface RegimeCardProps {
  regime: RegimeInfo;
}

export function RegimeCard({ regime }: RegimeCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <Waves className="h-3.5 w-3.5" />
          Market Regime
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <p className={`font-mono text-2xl font-bold tracking-tight ${regimeColor(regime.label)}`}>
          {regime.label || "—"}
        </p>

        <div>
          <div className="mb-1 flex justify-between text-xs text-muted-foreground">
            <span>Detector confidence</span>
            <span className="font-mono">{formatPercent(regime.confidence)}</span>
          </div>
          <div className="h-1.5 w-full overflow-hidden rounded-full bg-secondary">
            <div
              className="h-full rounded-full bg-primary"
              style={{ width: `${Math.min(100, Math.max(0, regime.confidence * 100))}%` }}
            />
          </div>
        </div>

        {regime.description && (
          <p className="border-t border-border pt-3 text-xs leading-relaxed text-muted-foreground">
            {regime.description}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
