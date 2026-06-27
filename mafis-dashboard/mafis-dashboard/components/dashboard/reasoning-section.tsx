import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { BrainCircuit } from "lucide-react";

interface ReasoningSectionProps {
  reasoning: string[];
}

export function ReasoningSection({ reasoning }: ReasoningSectionProps) {
  if (!reasoning || reasoning.length === 0) return null;

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <BrainCircuit className="h-3.5 w-3.5" />
          Orchestrator Reasoning
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ol className="space-y-3">
          {reasoning.map((step, i) => (
            <li key={i} className="flex gap-3 text-sm leading-relaxed">
              <span className="mt-0.5 shrink-0 font-mono text-xs text-muted-foreground">
                {String(i + 1).padStart(2, "0")}
              </span>
              <span className="text-foreground/90">{step}</span>
            </li>
          ))}
        </ol>
      </CardContent>
    </Card>
  );
}
