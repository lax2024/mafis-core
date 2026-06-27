import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ShieldAlert } from "lucide-react";
import { RiskMetrics } from "@/lib/types";
import { formatPercent, formatNumber, riskLevelColor } from "@/lib/format";

interface RiskCardProps {
  risk: RiskMetrics;
}

export function RiskCard({ risk }: RiskCardProps) {
  return (
    <Card>
      <CardHeader className="flex-row items-center justify-between space-y-0">
        <CardTitle>
          <ShieldAlert className="h-3.5 w-3.5" />
          Risk Assessment
        </CardTitle>
        {risk.risk_level && (
          <span
            className={`rounded-sm border px-2 py-0.5 font-mono text-[10px] font-semibold uppercase tracking-wide ${riskLevelColor(
              risk.risk_level
            )}`}
          >
            {risk.risk_level}
          </span>
        )}
      </CardHeader>
      <CardContent>
        <dl className="grid grid-cols-2 gap-x-3 gap-y-3">
          <div>
            <dt className="text-xs text-muted-foreground">VaR (95%)</dt>
            <dd className="font-mono text-sm font-medium text-bearish">{formatPercent(risk.var_95)}</dd>
          </div>
          <div>
            <dt className="text-xs text-muted-foreground">CVaR (95%)</dt>
            <dd className="font-mono text-sm font-medium text-bearish">{formatPercent(risk.cvar_95)}</dd>
          </div>
          <div>
            <dt className="text-xs text-muted-foreground">Sharpe Ratio</dt>
            <dd className="font-mono text-sm font-medium">{formatNumber(risk.sharpe_ratio, 2)}</dd>
          </div>
          <div>
            <dt className="text-xs text-muted-foreground">Max Drawdown</dt>
            <dd className="font-mono text-sm font-medium text-bearish">{formatPercent(risk.max_drawdown)}</dd>
          </div>
          {risk.volatility !== undefined && (
            <div className="col-span-2 border-t border-border pt-3">
              <dt className="text-xs text-muted-foreground">Annualized Volatility</dt>
              <dd className="font-mono text-sm font-medium">{formatPercent(risk.volatility)}</dd>
            </div>
          )}
        </dl>
      </CardContent>
    </Card>
  );
}
