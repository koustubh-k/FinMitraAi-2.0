"use client"

import { use, useState } from "react"
import useSWR, { mutate } from "swr"
import { ArrowLeft, ArrowUpRight, ArrowDownRight, DollarSign, Activity, TrendingUp, Plus } from "lucide-react"
import Link from "next/link"
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip as RechartsTooltip,
  Legend,
} from "recharts"

import { apiClient } from "@/lib/api-client"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Skeleton } from "@/components/ui/skeleton"
import { Badge } from "@/components/ui/badge"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface PortfolioDetailsProps {
  params: Promise<{ portfolioId: string }>
}

const fetcher = (url: string) => apiClient.get(url)

export default function PortfolioDetails({ params }: PortfolioDetailsProps) {
  const { portfolioId } = use(params)
  const [activeTab, setActiveTab] = useState("overview")
  const [isTxDialogOpen, setIsTxDialogOpen] = useState(false)
  const [txForm, setTxForm] = useState({ symbol: "", transaction_type: "BUY", quantity: "", price: "", transaction_date: new Date().toISOString().slice(0, 16) })

  const { data: summary, isLoading: isLoadingSummary } = useSWR(
    `/api/v1/portfolios/${portfolioId}/summary`,
    fetcher
  )

  const { data: allocation, isLoading: isLoadingAllocation } = useSWR(
    `/api/v1/portfolios/${portfolioId}/allocation`,
    fetcher
  )

  const { data: transactions, isLoading: isLoadingTransactions } = useSWR(
    `/api/v1/portfolios/${portfolioId}/transactions`,
    fetcher
  )

  const isLoading = isLoadingSummary || isLoadingAllocation

  const COLORS = ['var(--chart-1)', 'var(--chart-2)', 'var(--chart-3)', 'var(--chart-4)', 'var(--chart-5)']

  const allocationData = allocation?.positions?.map((position: any) => ({
    name: position.symbol,
    value: Number(position.weight_percentage ?? 0)
  })) ?? []

  const topHoldings = summary?.positions ? [...summary.positions].sort((a, b) => (Number(b.market_value) || 0) - (Number(a.market_value) || 0)).slice(0, 5) : []

  const handleAddTransaction = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await apiClient.post(`/api/v1/portfolios/${portfolioId}/transactions`, {
        ...txForm,
        quantity: Number(txForm.quantity),
        price: Number(txForm.price),
        transaction_date: new Date(txForm.transaction_date).toISOString()
      })
      setIsTxDialogOpen(false)
      setTxForm({ symbol: "", transaction_type: "BUY", quantity: "", price: "", transaction_date: new Date().toISOString().slice(0, 16) })
      // Revalidate data
      mutate(`/api/v1/portfolios/${portfolioId}/summary`)
      mutate(`/api/v1/portfolios/${portfolioId}/allocation`)
      mutate(`/api/v1/portfolios/${portfolioId}/transactions`)
    } catch (err) {
      console.error(err)
      alert("Failed to add transaction")
    }
  }

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center space-x-4">
        <Link href="/portfolio">
          <Button variant="outline" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <h2 className="text-3xl font-bold tracking-tight">Portfolio Details</h2>
        </div>
        <div className="flex items-center space-x-2">
          <Dialog open={isTxDialogOpen} onOpenChange={setIsTxDialogOpen}>
            <DialogTrigger render={<Button><Plus className="mr-2 h-4 w-4"/> Add Transaction</Button>} />
            <DialogContent>
              <form onSubmit={handleAddTransaction}>
                <DialogHeader>
                  <DialogTitle>Add Transaction</DialogTitle>
                  <DialogDescription>Record a new trade for this portfolio.</DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="symbol" className="text-right">Symbol</Label>
                    <Input id="symbol" value={txForm.symbol} onChange={e => setTxForm({...txForm, symbol: e.target.value.toUpperCase()})} className="col-span-3" required />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="type" className="text-right">Type</Label>
                    <Select value={txForm.transaction_type} onValueChange={v => setTxForm({...txForm, transaction_type: v || ""})}>
                      <SelectTrigger className="col-span-3">
                        <SelectValue placeholder="Select type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="BUY">Buy</SelectItem>
                        <SelectItem value="SELL">Sell</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="quantity" className="text-right">Quantity</Label>
                    <Input id="quantity" type="number" step="any" min="0" value={txForm.quantity} onChange={e => setTxForm({...txForm, quantity: e.target.value})} className="col-span-3" required />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="price" className="text-right">Price</Label>
                    <Input id="price" type="number" step="any" min="0" value={txForm.price} onChange={e => setTxForm({...txForm, price: e.target.value})} className="col-span-3" required />
                  </div>
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="date" className="text-right">Date</Label>
                    <Input id="date" type="datetime-local" value={txForm.transaction_date} onChange={e => setTxForm({...txForm, transaction_date: e.target.value})} className="col-span-3" required />
                  </div>
                </div>
                <DialogFooter>
                  <Button type="submit">Save Transaction</Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="holdings">Holdings</TabsTrigger>
          <TabsTrigger value="transactions">Transactions</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Value</CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                {isLoadingSummary ? (
                  <Skeleton className="h-8 w-24" />
                ) : (
                  <div className="text-2xl font-bold">
                    {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(summary?.market_value || 0)}
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Return</CardTitle>
                <Activity className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                {isLoadingSummary ? (
                  <Skeleton className="h-8 w-24" />
                ) : (
                  <div className={`text-2xl font-bold flex items-center ${(summary?.total_pnl || 0) >= 0 ? 'text-success' : 'text-destructive'}`}>
                    {(summary?.total_pnl || 0) >= 0 ? <ArrowUpRight className="mr-1 h-5 w-5" /> : <ArrowDownRight className="mr-1 h-5 w-5" />}
                    {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(Math.abs(summary?.total_pnl || 0))}
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Return %</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                {isLoadingSummary ? (
                  <Skeleton className="h-8 w-24" />
                ) : (
                  <div className={`text-2xl font-bold ${(summary?.return_percentage || 0) >= 0 ? 'text-success' : 'text-destructive'}`}>
                    {((summary?.return_percentage || 0) * 100).toFixed(2)}%
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Cost Basis</CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                {isLoadingSummary ? (
                  <Skeleton className="h-8 w-24" />
                ) : (
                  <div className="text-2xl font-bold">
                    {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(summary?.cost_basis || 0)}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
            <Card className="col-span-4">
              <CardHeader>
                <CardTitle>Asset Allocation</CardTitle>
              </CardHeader>
              <CardContent className="h-[300px]">
                {isLoadingAllocation ? (
                  <div className="h-full flex items-center justify-center">
                    <Skeleton className="h-[200px] w-[200px] rounded-full" />
                  </div>
                ) : allocationData.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={allocationData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={80}
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {allocationData.map((entry: any, index: number) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <RechartsTooltip 
                        formatter={(value: any) => [`${Number(value).toFixed(2)}%`, 'Allocation']}
                        contentStyle={{ borderRadius: '8px', border: '1px solid var(--border)', background: 'var(--card)' }}
                      />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="flex h-full items-center justify-center text-muted-foreground">
                    No allocation data available
                  </div>
                )}
              </CardContent>
            </Card>
            
            <Card className="col-span-3">
              <CardHeader>
                <CardTitle>Top Holdings</CardTitle>
                <CardDescription>
                  Your largest positions by value
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {isLoadingSummary ? (
                    Array.from({ length: 4 }).map((_, i) => (
                      <div key={i} className="flex items-center">
                        <Skeleton className="h-9 w-9 rounded-full" />
                        <div className="ml-4 space-y-1">
                          <Skeleton className="h-4 w-20" />
                          <Skeleton className="h-3 w-16" />
                        </div>
                        <div className="ml-auto">
                          <Skeleton className="h-4 w-16" />
                        </div>
                      </div>
                    ))
                  ) : topHoldings.length > 0 ? (
                    topHoldings.map((holding: any, i: number) => (
                      <div key={i} className="flex items-center">
                        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary/10">
                          <span className="font-semibold text-primary text-xs">{holding.symbol.substring(0,2)}</span>
                        </div>
                        <div className="ml-4 space-y-1">
                          <p className="text-sm font-medium leading-none">{holding.symbol}</p>
                          <p className="text-xs text-muted-foreground">
                            {Number(holding.quantity).toFixed(2)} shares
                          </p>
                        </div>
                        <div className="ml-auto font-medium">
                          {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(holding.market_value || 0)}
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-sm text-muted-foreground text-center py-4">
                      No holdings found
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="holdings">
          <Card>
            <CardHeader>
              <CardTitle>Holdings</CardTitle>
              <CardDescription>Detailed view of all your assets</CardDescription>
            </CardHeader>
            <CardContent>
              {summary?.positions?.length ? (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm text-left">
                    <thead className="text-xs uppercase bg-muted/50">
                      <tr>
                        <th className="px-4 py-3 rounded-tl-lg">Symbol</th>
                        <th className="px-4 py-3">Quantity</th>
                        <th className="px-4 py-3">Avg Cost</th>
                        <th className="px-4 py-3">Mkt Price</th>
                        <th className="px-4 py-3">Mkt Value</th>
                        <th className="px-4 py-3 rounded-tr-lg">Total P&L</th>
                      </tr>
                    </thead>
                    <tbody>
                      {summary.positions.map((pos: any, i: number) => (
                        <tr key={i} className="border-b last:border-0">
                          <td className="px-4 py-3 font-medium">{pos.symbol}</td>
                          <td className="px-4 py-3">{Number(pos.quantity).toFixed(4)}</td>
                          <td className="px-4 py-3">${Number(pos.average_cost).toFixed(2)}</td>
                          <td className="px-4 py-3">${Number(pos.market_price || 0).toFixed(2)}</td>
                          <td className="px-4 py-3">${Number(pos.market_value || 0).toFixed(2)}</td>
                          <td className={`px-4 py-3 font-medium ${Number(pos.total_pnl) >= 0 ? 'text-success' : 'text-destructive'}`}>
                            ${Number(pos.total_pnl || 0).toFixed(2)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="text-sm text-muted-foreground text-center py-8 border rounded-lg border-dashed">
                  No holdings found
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="transactions">
          <Card>
            <CardHeader>
              <CardTitle>Transaction History</CardTitle>
              <CardDescription>Recent buy and sell orders</CardDescription>
            </CardHeader>
            <CardContent>
              {isLoadingTransactions ? (
                <div className="space-y-2">
                  <Skeleton className="h-10 w-full" />
                  <Skeleton className="h-10 w-full" />
                  <Skeleton className="h-10 w-full" />
                </div>
              ) : transactions?.length ? (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm text-left">
                    <thead className="text-xs uppercase bg-muted/50">
                      <tr>
                        <th className="px-4 py-3 rounded-tl-lg">Date</th>
                        <th className="px-4 py-3">Symbol</th>
                        <th className="px-4 py-3">Type</th>
                        <th className="px-4 py-3">Quantity</th>
                        <th className="px-4 py-3 rounded-tr-lg">Price</th>
                      </tr>
                    </thead>
                    <tbody>
                      {transactions.map((tx: any, i: number) => (
                        <tr key={i} className="border-b last:border-0">
                          <td className="px-4 py-3 text-muted-foreground">{new Date(tx.transaction_date).toLocaleDateString()}</td>
                          <td className="px-4 py-3 font-medium">{tx.symbol}</td>
                          <td className="px-4 py-3">
                            <Badge variant={tx.transaction_type === "BUY" ? "default" : "destructive"}>
                              {tx.transaction_type}
                            </Badge>
                          </td>
                          <td className="px-4 py-3">{Number(tx.quantity).toFixed(4)}</td>
                          <td className="px-4 py-3">${Number(tx.price).toFixed(2)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="text-sm text-muted-foreground text-center py-8 border rounded-lg border-dashed">
                  No transactions found
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
