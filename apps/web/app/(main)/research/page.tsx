"use client"

import { useState } from "react"
import { Search, TrendingUp, TrendingDown, Clock, LineChart as LineChartIcon } from "lucide-react"
import useSWR from "swr"

import { apiClient } from "@/lib/api-client"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Skeleton } from "@/components/ui/skeleton"

const fetcher = (url: string) => apiClient.get(url)

export default function ResearchPage() {
  const [symbol, setSymbol] = useState("AAPL")
  const [searchQuery, setSearchQuery] = useState("")

  const { data: quote, isLoading: isQuoteLoading } = useSWR(
    `/api/v1/market/quote/${symbol}`, 
    fetcher
  )

  const { data: history, isLoading: isHistoryLoading } = useSWR(
    `/api/v1/market/history/${symbol}`,
    fetcher
  )

  const { data: company, isLoading: isCompanyLoading } = useSWR(
    `/api/v1/market/company/${symbol}`,
    fetcher
  )

  const { data: metrics, isLoading: isMetricsLoading } = useSWR(
    `/api/v1/market/metrics/${symbol}`,
    fetcher
  )

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      setSymbol(searchQuery.toUpperCase().trim())
      setSearchQuery("")
    }
  }

  const price = quote?.price
  const previousClose = quote?.previous_close
  const changePercent = quote?.day_change_percent
  const isPositive = changePercent !== null && changePercent >= 0

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Market Research</h2>
      </div>

      <div className="max-w-2xl">
        <form onSubmit={handleSearch} className="flex space-x-2">
          <Input 
            placeholder="Search by symbol (e.g. MSFT, AAPL, TSLA)..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="flex-1"
          />
          <Button type="submit">
            <Search className="mr-2 h-4 w-4" />
            Search
          </Button>
        </form>
      </div>

      <div className="mt-8">
        {isQuoteLoading ? (
          <div className="space-y-4">
            <div className="flex items-center gap-4">
              <Skeleton className="h-12 w-24" />
              <Skeleton className="h-8 w-64" />
            </div>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {Array.from({ length: 4 }).map((_, i) => (
                <Skeleton key={i} className="h-32 w-full" />
              ))}
            </div>
          </div>
        ) : quote ? (
          <div className="space-y-6">
            <div className="flex flex-col space-y-1">
              <div className="flex items-center gap-4">
                <h1 className="text-4xl font-bold">{symbol}</h1>
                {changePercent !== null && changePercent !== undefined ? (
                  <Badge variant={isPositive ? "default" : "destructive"} className="text-sm px-2 py-1">
                    {isPositive ? <TrendingUp className="mr-1 h-4 w-4" /> : <TrendingDown className="mr-1 h-4 w-4" />}
                    {isPositive ? '+' : ''}{(changePercent * 100).toFixed(2)}%
                  </Badge>
                ) : (
                  <Badge variant="secondary" className="text-sm px-2 py-1">
                    N/A
                  </Badge>
                )}
              </div>
              <p className="text-2xl font-semibold text-muted-foreground">
                {price !== null && price !== undefined ? `$${price.toFixed(2)}` : 'N/A'}
              </p>
              <div className="text-sm text-muted-foreground flex items-center pt-2">
                <Clock className="mr-1 h-4 w-4" />
                Data provided by Finnhub. Real-time quote.
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Previous Close</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {previousClose !== null && previousClose !== undefined ? `$${previousClose.toFixed(2)}` : 'N/A'}
                  </div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Open</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">N/A</div>
                  <p className="text-xs text-muted-foreground">Not in basic quote</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Day's Range</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">N/A</div>
                  <p className="text-xs text-muted-foreground">Not in basic quote</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Volume</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">N/A</div>
                  <p className="text-xs text-muted-foreground">Not in basic quote</p>
                </CardContent>
              </Card>
            </div>

            <Tabs defaultValue="chart" className="space-y-4">
              <TabsList>
                <TabsTrigger value="chart">Chart</TabsTrigger>
                <TabsTrigger value="company">Company</TabsTrigger>
                <TabsTrigger value="financials">Financials</TabsTrigger>
              </TabsList>
              <TabsContent value="chart">
                <Card>
                  <CardHeader>
                    <CardTitle>Price History</CardTitle>
                    <CardDescription>
                      {history?.data?.length ? `${history.data.length} data points available` : 'Interactive chart (Mocked for now)'}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="h-[400px] flex items-center justify-center border-t border-muted bg-muted/10">
                    {isHistoryLoading ? (
                       <Skeleton className="h-[300px] w-full" />
                    ) : history?.data ? (
                       <div className="w-full text-center text-sm text-muted-foreground">
                         Data available from {history.data[0]?.timestamp} to {history.data[history.data.length - 1]?.timestamp}
                         <br />
                         (Chart component rendering pending)
                       </div>
                    ) : (
                      <>
                        <LineChartIcon className="h-16 w-16 text-muted-foreground/30" />
                        <span className="ml-4 text-muted-foreground">Chart data unavailable</span>
                      </>
                    )}
                  </CardContent>
                </Card>
              </TabsContent>
              <TabsContent value="company">
                <Card>
                  <CardContent className="min-h-[400px] p-6 text-sm">
                    {isCompanyLoading ? (
                      <Skeleton className="h-[300px] w-full" />
                    ) : company ? (
                      <div className="space-y-4">
                        <h3 className="text-lg font-bold">{company.name || symbol}</h3>
                        <p>{company.description || "Company description unavailable."}</p>
                        <div className="grid grid-cols-2 gap-4 pt-4 border-t">
                          <div>
                            <span className="font-medium">Industry:</span> {company.industry || "N/A"}
                          </div>
                          <div>
                            <span className="font-medium">Sector:</span> {company.sector || "N/A"}
                          </div>
                          <div>
                            <span className="font-medium">Exchange:</span> {company.exchange || "N/A"}
                          </div>
                          <div>
                            <span className="font-medium">Website:</span> {company.website ? <a href={company.website} target="_blank" rel="noreferrer" className="text-blue-500 hover:underline">{company.website}</a> : "N/A"}
                          </div>
                        </div>
                      </div>
                    ) : (
                      <div className="flex h-full items-center justify-center text-muted-foreground">
                        Company profile data unavailable
                      </div>
                    )}
                  </CardContent>
                </Card>
              </TabsContent>
              <TabsContent value="financials">
                <Card>
                  <CardContent className="min-h-[400px] p-6 text-sm">
                    {isMetricsLoading ? (
                      <Skeleton className="h-[300px] w-full" />
                    ) : metrics ? (
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                           <span className="font-medium">52 Week High:</span> {metrics.metric?.['52WeekHigh'] || 'N/A'}
                        </div>
                        <div>
                           <span className="font-medium">52 Week Low:</span> {metrics.metric?.['52WeekLow'] || 'N/A'}
                        </div>
                        <div>
                           <span className="font-medium">Market Cap:</span> {metrics.metric?.marketCapitalization || 'N/A'}
                        </div>
                        <div>
                           <span className="font-medium">P/E Ratio:</span> {metrics.metric?.peBasicExclExtraTTM || 'N/A'}
                        </div>
                      </div>
                    ) : (
                      <div className="flex h-full items-center justify-center text-muted-foreground">
                        Financials data unavailable
                      </div>
                    )}
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        ) : (
          <div className="text-center p-12 border rounded-lg bg-muted/30">
            <h3 className="text-lg font-medium">Could not fetch data for {symbol}</h3>
            <p className="text-muted-foreground mt-2">Please check the symbol and try again.</p>
          </div>
        )}
      </div>
    </div>
  )
}
