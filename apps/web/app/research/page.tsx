"use client";

import { useState } from "react";

export default function ResearchPage() {
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [answer, setAnswer] = useState<string | null>(null);
  const [citations, setCitations] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setStatus("Starting research...");
    setAnswer(null);
    setCitations([]);

    try {
      const response = await fetch("http://localhost:8000/research/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!response.body) {
        throw new Error("No body in response");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          const events = chunk.split("\n\n");
          
          for (const event of events) {
            if (event.startsWith("data:")) {
              const dataStr = event.replace("data: ", "").trim();
              if (dataStr) {
                const data = JSON.parse(dataStr);
                if (data.status) {
                    // Safe workflow state mapping
                    const stateMessages: Record<string, string> = {
                        "analyzing_query": "Analyzing query...",
                        "retrieving_evidence": "Searching financial sources...",
                        "generating_answer": "Synthesizing evidence...",
                        "validating_citations": "Validating citations...",
                    };
                    setStatus(stateMessages[data.status] || data.status);
                } else if (data.answer) {
                    setAnswer(data.answer);
                    setCitations(data.citations || []);
                    setStatus(null);
                }
              }
            }
          }
        }
      }
    } catch (error) {
      console.error(error);
      setStatus("An error occurred during research.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">FinMitra AI Research</h1>
      
      <form onSubmit={handleSubmit} className="mb-8">
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a financial question..."
            className="flex-1 p-3 border rounded-lg shadow-sm"
            disabled={isLoading}
          />
          <button 
            type="submit" 
            disabled={isLoading || !query}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            Research
          </button>
        </div>
      </form>

      {status && (
        <div className="p-4 mb-4 bg-gray-100 rounded-lg text-gray-700 animate-pulse">
          <p className="flex items-center gap-2">
            <span className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></span>
            {status}
          </p>
        </div>
      )}

      {answer && (
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          <div className="prose max-w-none">
            <h2 className="text-xl font-semibold mb-4">Research Findings</h2>
            <div className="text-gray-800 whitespace-pre-wrap">{answer}</div>
          </div>
          
          {citations.length > 0 && (
            <div className="mt-6 pt-4 border-t border-gray-100">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Sources Cited</h3>
              <ul className="list-disc pl-5 text-sm text-gray-600">
                {citations.map((cite, i) => (
                  <li key={i}>{cite}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
