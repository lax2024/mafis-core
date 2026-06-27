"use client";

import * as React from "react";
import { Search, ArrowRight } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface TickerSearchProps {
  onSearch: (ticker: string) => void;
  isLoading: boolean;
  initialValue?: string;
}

const QUICK_PICKS = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK"];

export function TickerSearch({ onSearch, isLoading, initialValue = "" }: TickerSearchProps) {
  const [value, setValue] = React.useState(initialValue);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (value.trim()) onSearch(value.trim().toUpperCase());
  }

  return (
    <div className="sticky top-0 z-20 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80">
      <div className="container py-4">
        <form onSubmit={handleSubmit} className="flex flex-col gap-3 sm:flex-row sm:items-center">
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              value={value}
              onChange={(e) => setValue(e.target.value.toUpperCase())}
              placeholder="Enter ticker symbol — e.g. RELIANCE, TCS, INFY"
              className="h-11 pl-9 text-base tracking-wide"
              autoComplete="off"
              spellCheck={false}
              aria-label="Ticker symbol"
            />
          </div>
          <Button type="submit" size="lg" disabled={isLoading || !value.trim()} className="font-mono">
            {isLoading ? (
              <>
                <span className="h-2 w-2 animate-pulse-dot rounded-full bg-primary-foreground" />
                ANALYZING
              </>
            ) : (
              <>
                ANALYZE
                <ArrowRight className="h-4 w-4" />
              </>
            )}
          </Button>
        </form>

        <div className="mt-3 flex flex-wrap items-center gap-2">
          <span className="text-xs uppercase tracking-wider text-muted-foreground">Quick pick:</span>
          {QUICK_PICKS.map((sym) => (
            <button
              key={sym}
              type="button"
              onClick={() => {
                setValue(sym);
                onSearch(sym);
              }}
              disabled={isLoading}
              className="rounded-sm border border-border px-2 py-0.5 font-mono text-xs text-muted-foreground transition-colors hover:border-primary/50 hover:text-foreground disabled:opacity-50"
            >
              {sym}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
