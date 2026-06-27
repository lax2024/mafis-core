import { Network } from "lucide-react";

export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-md border border-dashed border-border py-24 text-center">
      <Network className="h-10 w-10 text-muted-foreground/40" strokeWidth={1.5} />
      <div className="space-y-1">
        <p className="text-sm font-medium text-foreground">No ticker analyzed yet</p>
        <p className="max-w-sm text-sm text-muted-foreground">
          Search a symbol above to run it through the Technical, Sentiment, and Risk agents.
        </p>
      </div>
    </div>
  );
}
