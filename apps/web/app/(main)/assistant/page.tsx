"use client"

import { useState, useRef, useEffect } from "react"
import { Send, Bot, User, FileText, ChevronDown, CheckCircle2, CircleDashed, Wrench, Sparkles } from "lucide-react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

import { useAuth } from "@/lib/auth-context"
import { API_BASE_URL } from "@/lib/api-client"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Badge } from "@/components/ui/badge"

interface ToolResult {
  name: string
  data: any
}

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  toolResults?: ToolResult[]
  citations?: string[]
  status?: string
}

export default function AssistantPage() {
  const { user } = useAuth()
  const [query, setQuery] = useState("")
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content: `Hello ${user?.first_name || ''}. I'm FinMitra, your AI financial analyst. I can help you analyze market data, review your portfolio, or research specific companies. How can I assist you today?`
    }
  ])
  const [isLoading, setIsLoading] = useState(false)
  const [currentStatus, setCurrentStatus] = useState<string | null>(null)
  
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, currentStatus])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim() || isLoading) return

    const userMsg: Message = { id: Date.now().toString(), role: "user", content: query }
    setMessages(prev => [...prev, userMsg])
    setQuery("")
    setIsLoading(true)
    setCurrentStatus("Thinking...")

    const assistantMsgId = (Date.now() + 1).toString()
    let currentAssistantMsg: Message = { id: assistantMsgId, role: "assistant", content: "", toolResults: [], citations: [] }
    
    setMessages(prev => [...prev, currentAssistantMsg])

    try {
      const token = localStorage.getItem("token")
      const response = await fetch(`${API_BASE_URL}/api/v1/assistant/chat`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ query: userMsg.content }),
      })

      if (!response.ok) {
        const errData = await response.json().catch(() => null)
        const errMsg = errData?.detail || "Assistant service unavailable. Please check backend configuration."
        throw new Error(errMsg)
      }
      
      if (!response.body) throw new Error("No response body")

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let done = false

      while (!done) {
        const { value, done: readerDone } = await reader.read()
        done = readerDone
        if (value) {
          const chunk = decoder.decode(value, { stream: true })
          const events = chunk.split("\n\n")
          
          for (const event of events) {
            if (event.startsWith("event: ")) {
              const lines = event.split("\n")
              const eventType = lines[0].replace("event: ", "").trim()
              const dataLine = lines.find(l => l.startsWith("data: "))
              
              if (dataLine) {
                const dataStr = dataLine.replace("data: ", "").trim()
                const data = JSON.parse(dataStr)
                
                if (eventType === "status") {
                  setCurrentStatus(data.status.replace(/_/g, ' '))
                } else if (eventType === "tool_results") {
                  currentAssistantMsg = {
                    ...currentAssistantMsg,
                    toolResults: data.map((res: any) => {
                      const name = Object.keys(res)[0];
                      return { name, data: res[name] }
                    })
                  }
                  setMessages(prev => prev.map(msg => msg.id === assistantMsgId ? currentAssistantMsg : msg))
                } else if (eventType === "citations") {
                  currentAssistantMsg = {
                    ...currentAssistantMsg,
                    citations: data
                  }
                  setMessages(prev => prev.map(msg => msg.id === assistantMsgId ? currentAssistantMsg : msg))
                } else if (eventType === "error") {
                  currentAssistantMsg = {
                    ...currentAssistantMsg,
                    content: `Error: ${data.detail || "An unknown error occurred during generation."}`
                  }
                  setMessages(prev => prev.map(msg => msg.id === assistantMsgId ? currentAssistantMsg : msg))
                  setCurrentStatus(null)
                } else if (eventType === "complete") {
                  currentAssistantMsg = {
                    ...currentAssistantMsg,
                    content: data.answer,
                    citations: data.citations || currentAssistantMsg.citations,
                    status: data.route ? `Routed via ${data.route} agent` : undefined
                  }
                  setMessages(prev => prev.map(msg => msg.id === assistantMsgId ? currentAssistantMsg : msg))
                  setCurrentStatus(null)
                }
              }
            }
          }
        }
      }
    } catch (error: any) {
      console.error(error)
      setMessages(prev => prev.map(msg => msg.id === assistantMsgId ? { ...msg, content: `Sorry, I encountered an error: ${error.message || "An unexpected error occurred."}` } : msg))
    } finally {
      setIsLoading(false)
      setCurrentStatus(null)
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      <div className="flex items-center p-4 border-b bg-card">
        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-primary-foreground">
          <Sparkles className="h-5 w-5" />
        </div>
        <div className="ml-3">
          <h2 className="text-lg font-semibold">FinMitra Intelligence</h2>
          <p className="text-sm text-muted-foreground">Ask anything about your portfolio or the markets</p>
        </div>
      </div>

      <ScrollArea className="flex-1 p-4">
        <div className="max-w-3xl mx-auto space-y-6 pb-20">
          {messages.map((msg) => (
            <div key={msg.id} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : ''}`}>
              {msg.role === 'assistant' && (
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground mt-1">
                  <Bot className="h-4 w-4" />
                </div>
              )}
              
              <div className={`flex flex-col gap-2 max-w-[85%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                {msg.status && msg.role === 'assistant' && (
                  <Badge variant="outline" className="text-xs bg-muted/50">{msg.status}</Badge>
                )}
                
                <div className={`rounded-xl p-4 shadow-sm ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-card border'}`}>
                  {msg.role === 'user' ? (
                    <div className="whitespace-pre-wrap">{msg.content}</div>
                  ) : (
                    <div className="prose prose-sm dark:prose-invert max-w-none">
                      {msg.content ? (
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {msg.content}
                        </ReactMarkdown>
                      ) : (
                        <div className="flex items-center gap-2 text-muted-foreground h-6">
                          <CircleDashed className="h-4 w-4 animate-spin" />
                          <span className="text-sm capitalize">{currentStatus || 'Processing...'}</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {msg.toolResults && msg.toolResults.length > 0 && (
                  <div className="w-full mt-2">
                    <Accordion className="w-full bg-muted/30 rounded-lg border">
                      <AccordionItem value="tools" className="border-b-0">
                        <AccordionTrigger className="px-4 py-2 text-sm hover:no-underline">
                          <div className="flex items-center gap-2 text-muted-foreground">
                            <Wrench className="h-4 w-4" />
                            <span>Analysis Tools Used ({msg.toolResults.length})</span>
                          </div>
                        </AccordionTrigger>
                        <AccordionContent className="px-4 pb-4">
                          <div className="grid gap-2 mt-2">
                            {msg.toolResults.map((tool, idx) => (
                              <Card key={idx} className="bg-background shadow-none border-dashed">
                                <CardContent className="p-3">
                                  <div className="text-xs font-semibold text-primary uppercase mb-1">{tool.name.replace(/_/g, ' ')}</div>
                                  <pre className="text-xs text-muted-foreground overflow-auto max-h-32">
                                    {typeof tool.data === 'string' ? tool.data : JSON.stringify(tool.data, null, 2)}
                                  </pre>
                                </CardContent>
                              </Card>
                            ))}
                          </div>
                        </AccordionContent>
                      </AccordionItem>
                    </Accordion>
                  </div>
                )}

                {msg.citations && msg.citations.length > 0 && (
                  <div className="w-full mt-2 bg-muted/30 rounded-lg border p-4">
                    <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground mb-3">
                      <FileText className="h-4 w-4" />
                      Sources & Evidence
                    </div>
                    <ul className="space-y-2">
                      {msg.citations.map((cite, idx) => (
                        <li key={idx} className="flex gap-2 text-sm text-muted-foreground">
                          <CheckCircle2 className="h-4 w-4 text-primary shrink-0 mt-0.5" />
                          <span>{cite}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {msg.role === 'user' && (
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-muted mt-1 border">
                  <User className="h-4 w-4 text-muted-foreground" />
                </div>
              )}
            </div>
          ))}
          
          {isLoading && !currentStatus && (
            <div className="flex gap-4">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-primary-foreground mt-1">
                <Bot className="h-4 w-4" />
              </div>
              <div className="rounded-xl p-4 bg-card border shadow-sm flex items-center h-12">
                <div className="flex gap-1">
                  <span className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce"></span>
                  <span className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce delay-75"></span>
                  <span className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce delay-150"></span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </ScrollArea>

      <div className="p-4 bg-background border-t">
        <div className="max-w-3xl mx-auto relative flex items-center">
          <form onSubmit={handleSubmit} className="w-full flex gap-2">
            <Textarea 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a financial question..." 
              className="min-h-[60px] resize-none pr-12 text-sm"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            <Button 
              type="submit" 
              size="icon"
              disabled={!query.trim() || isLoading} 
              className="absolute right-2 top-2 h-10 w-10 shrink-0 rounded-full"
            >
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}
