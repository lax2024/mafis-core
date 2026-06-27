"use client";

import { Activity } from "lucide-react";

interface SiteHeaderProps {
  isLive?: boolean;
}

export function SiteHeader({ isLive }: SiteHeaderProps) {
  return (
    <header className="border-b border-border bg-background">
      <div className="container flex items-center justify-between py-4">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-sm bg-primary/10 border border-primary/30">
            <Activity className="h-4 w-4 text-primary" />
          </div>
          <div>
            <p className="font-mono text-sm font-bold tracking-wide text-foreground">MAFIS</p>
            <p className="text-[10px] uppercase tracking-wider text-muted-foreground">
              Multi-Agent Financial Intelligence System
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span
            className={`h-1.5 w-1.5 rounded-full ${
              isLive ? "bg-bullish animate-pulse-dot" : "bg-muted-foreground/40"
            }`}
          />
          {isLive ? "Backend connected" : "Backend idle"}
        </div>
      </div>
    </header>
  );
}
