"use client"

import { useState } from "react"
import Link from "next/link"
import useSWR, { mutate } from "swr"
import { Plus, Briefcase, ArrowRight } from "lucide-react"

import { apiClient } from "@/lib/api-client"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
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

interface Portfolio {
  id: string
  name: string
  description?: string
  total_value?: number
  cash_balance?: number
}

const fetcher = (url: string) => apiClient.get(url)

export default function PortfoliosPage() {
  const { data: portfolios, error, isLoading } = useSWR<Portfolio[]>("/api/v1/portfolios/", fetcher)
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [portfolioName, setPortfolioName] = useState("")

  const handleCreatePortfolio = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await apiClient.post("/api/v1/portfolios/", { name: portfolioName })
      setIsDialogOpen(false)
      setPortfolioName("")
      mutate("/api/v1/portfolios/")
    } catch (err) {
      console.error(err)
      alert("Failed to create portfolio")
    }
  }

  if (error) return <div className="p-8 text-destructive">Failed to load portfolios</div>

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Portfolios</h2>
        <div className="flex items-center space-x-2">
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger render={
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Create Portfolio
              </Button>
            } />
            <DialogContent>
              <form onSubmit={handleCreatePortfolio}>
                <DialogHeader>
                  <DialogTitle>Create Portfolio</DialogTitle>
                  <DialogDescription>Create a new portfolio to track your investments.</DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="name" className="text-right">Name</Label>
                    <Input id="name" value={portfolioName} onChange={e => setPortfolioName(e.target.value)} className="col-span-3" required />
                  </div>
                </div>
                <DialogFooter>
                  <Button type="submit">Create</Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {isLoading ? (
          Array.from({ length: 3 }).map((_, i) => (
            <Card key={i} className="flex flex-col">
              <CardHeader>
                <Skeleton className="h-6 w-1/2 mb-2" />
                <Skeleton className="h-4 w-full" />
              </CardHeader>
              <CardContent className="flex-1">
                <Skeleton className="h-8 w-1/3 mb-4" />
                <Skeleton className="h-4 w-1/4" />
              </CardContent>
            </Card>
          ))
        ) : portfolios?.length === 0 ? (
          <div className="col-span-3 flex h-[300px] flex-col items-center justify-center rounded-lg border border-dashed text-center">
            <Briefcase className="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 className="mt-4 text-lg font-semibold">No portfolios</h3>
            <p className="mb-4 mt-2 text-sm text-muted-foreground">
              You haven't created any portfolios yet.
            </p>
            <Button onClick={() => setIsDialogOpen(true)}>
              <Plus className="mr-2 h-4 w-4" />
              Create Portfolio
            </Button>
          </div>
        ) : (
          portfolios?.map((portfolio) => (
            <Card key={portfolio.id} className="flex flex-col hover:border-primary/50 transition-colors">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  {portfolio.name}
                  <Briefcase className="h-4 w-4 text-muted-foreground" />
                </CardTitle>
                <CardDescription className="line-clamp-1">
                  {portfolio.description || "No description provided"}
                </CardDescription>
              </CardHeader>
              <CardContent className="flex-1">
                <div className="text-2xl font-bold">
                  {portfolio.total_value !== undefined 
                    ? new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(portfolio.total_value)
                    : "$0.00"
                  }
                </div>
                <div className="text-sm text-muted-foreground mt-1 flex items-center">
                  Cash Balance: {portfolio.cash_balance !== undefined 
                    ? new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(portfolio.cash_balance)
                    : "$0.00"
                  }
                </div>
              </CardContent>
              <CardFooter>
                <Link href={`/portfolio/${portfolio.id}`} className="w-full">
                  <Button variant="ghost" className="w-full justify-between">
                    View Details
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </CardFooter>
            </Card>
          ))
        )}
      </div>
    </div>
  )
}
