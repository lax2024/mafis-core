import { AnalyzeResponse, MafisApiError } from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_MAFIS_API_URL || "http://127.0.0.1:8000";

const DEFAULT_TIMEOUT_MS = 20_000;

/**
 * Fetches MAFIS analysis for a given ticker from the FastAPI backend.
 * Throws MafisApiError with a human-readable message on any failure
 * (network down, 4xx/5xx, malformed JSON, timeout).
 */
export async function fetchAnalysis(
  ticker: string,
  signal?: AbortSignal
): Promise<AnalyzeResponse> {
  const cleanTicker = ticker.trim().toUpperCase();
  if (!cleanTicker) {
    throw new MafisApiError("Enter a ticker symbol to analyze.");
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);

  // Combine the caller's abort signal (e.g. component unmount / new search)
  // with our own timeout-based abort.
  if (signal) {
    signal.addEventListener("abort", () => controller.abort());
  }

  let response: Response;
  try {
    response = await fetch(
      `${API_BASE_URL}/analyze/${encodeURIComponent(cleanTicker)}`,
      {
        method: "GET",
        headers: { Accept: "application/json" },
        signal: controller.signal,
        cache: "no-store",
      }
    );
  } catch (err) {
    clearTimeout(timeoutId);
    if (err instanceof DOMException && err.name === "AbortError") {
      throw new MafisApiError(
        `Request timed out reaching the MAFIS backend at ${API_BASE_URL}. Is it running?`
      );
    }
    throw new MafisApiError(
      `Could not reach the MAFIS backend at ${API_BASE_URL}. Check that the FastAPI server is running and CORS is enabled.`
    );
  }
  clearTimeout(timeoutId);

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const body = await response.json();
      detail = body?.detail || body?.message || detail;
    } catch {
      // response wasn't JSON, fall back to statusText
    }

    if (response.status === 404) {
      throw new MafisApiError(
        `No data found for "${cleanTicker}". Check the symbol and try again.`,
        404
      );
    }
    throw new MafisApiError(
      `MAFIS backend returned an error: ${detail}`,
      response.status
    );
  }

  try {
    const data = (await response.json()) as AnalyzeResponse;
    return data;
  } catch {
    throw new MafisApiError(
      "The MAFIS backend returned a response that could not be parsed as JSON."
    );
  }
}
