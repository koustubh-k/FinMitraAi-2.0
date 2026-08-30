"use client";

import { useState } from "react";
import { getAuthToken } from "@/lib/auth"; // Assuming some auth helper exists

export default function AssistantPage() {
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState<string | null>(null);
  const [answer, setAnswer] = useState<string | null>(null);
  const [toolResults, setToolResults] = useState<any[]>([]);
  const [citations, setCitations] = useState<string[]>([]);
  const [route, setRoute] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
    e.preventDefault();
    setIsLoading(true);
    setStatus("Starting assistant...");
    setAnswer(null);
    setCitations([]);
    setToolResults([]);
    setRoute(null);

    try {
      const token = getAuthToken(); // Replace with actual token retrieval
      const response = await fetch("http://localhost:8000/assistant/chat", {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
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
            if (event.startsWith("event: ")) {
              const lines = event.split("\n");
              const eventType = lines[0].replace("event: ", "").trim();
              const dataLine = lines.find(l => l.startsWith("data: "));
              if (dataLine) {
                const dataStr = dataLine.replace("data: ", "").trim();
                const data = JSON.parse(dataStr);
                
                if (eventType === "status") {
                    const stateMessages: Record<string, string> = {
                        "routing": "Understanding your question...",
                        "analyzing_portfolio": "Analyzing your portfolio...",
                        "explaining": "Preparing explanation...",
                        "analyzing_query": "Analyzing query...",
                        "retrieving_evidence": "Searching financial sources...",
                        "generating_answer": "Synthesizing evidence...",
                        "validating_citations": "Validating citations...",
                    };
                    if (data.status.startsWith("running_tool_")) {
                        setStatus(`Checking ${data.status.replace("running_tool_", "")}...`);
                    } else {
                        setStatus(stateMessages[data.status] || data.status);
                    }
                } else if (eventType === "tool_results") {
                    setToolResults(data);
                } else if (eventType === "citations") {
                    setCitations(data);
                } else if (eventType === "complete") {
                    setAnswer(data.answer);
                    if (data.citations) setCitations(data.citations);
                    setRoute(data.route);
                    setStatus(null);
                }
              }
            }
          }
        }
      }
    } catch (error) {
      console.error(error);
      setStatus("An error occurred. Please ensure you are logged in and the service is available.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">FinMitra AI Assistant</h1>
      
      <form onSubmit={handleSubmit} className="mb-8">
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a financial question, research a stock, or check your portfolio..."
            className="flex-1 p-3 border rounded-lg shadow-sm"
            disabled={isLoading}
          />
          <button 
            type="submit" 
            disabled={isLoading || !query}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            Ask
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
      
      {toolResults.length > 0 && (
        <div className="mb-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          {toolResults.map((result, idx) => {
             const toolName = Object.keys(result)[0];
             let toolData = result[toolName];
             try { if (typeof toolData === 'string') toolData = JSON.parse(toolData); } catch(e) {}
             
             return (
              <div key={idx} className="p-4 border border-blue-200 bg-blue-50 rounded-lg shadow-sm">
                <h4 className="font-semibold text-blue-800 text-sm mb-2 uppercase tracking-wide">{toolName.replace(/_/g, ' ')}</h4>
                {toolData.error ? (
                  <p className="text-red-600 text-sm">{toolData.error}</p>
                ) : (
                  <pre className="text-xs text-blue-900 overflow-auto">{JSON.stringify(toolData, null, 2)}</pre>
                )}
              </div>
            );
          })}
        </div>
      )}

      {answer && (
        <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
          {route && (
            <div className="mb-4 inline-block px-3 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full uppercase tracking-wide">
              {route} Agent
            </div>
          )}
          <div className="prose max-w-none">
            <div className="text-gray-800 whitespace-pre-wrap">{answer}</div>
          </div>
          
          {citations.length > 0 && (
            <div className="mt-6 pt-4 border-t border-gray-100 bg-gray-50 p-4 rounded-lg">
              <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-2">Sources & Evidence</h3>
              <ul className="list-disc pl-5 text-sm text-gray-600">
                {citations.map((cite, i) => (
                  <li key={i} className="mb-1">{cite}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
