"use client"

import { useAuth } from "@/lib/auth-context"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Sparkles, ArrowRight, PieChart, LineChart } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  const { user } = useAuth()

  return (
    <div className="flex-1 space-y-4 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Welcome back
            </CardTitle>
            <Sparkles className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{user?.first_name || 'User'}</div>
            <p className="text-xs text-muted-foreground">
              Your financial intelligence center is ready.
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7 mt-4">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Overview</CardTitle>
          </CardHeader>
          <CardContent className="pl-2 flex h-[350px] items-center justify-center border-t border-muted bg-muted/10">
            <p className="text-sm text-muted-foreground">Select a portfolio to view performance</p>
          </CardContent>
        </Card>
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>
              Get started with FinMitra AI
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4">
            <Link href="/portfolio">
              <div className="flex items-center justify-between rounded-lg border p-4 hover:bg-muted/50 transition-colors">
                <div className="flex items-center space-x-4">
                  <div className="bg-primary/10 p-2 rounded-full">
                    <PieChart className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <p className="text-sm font-medium leading-none">View Portfolios</p>
                    <p className="text-sm text-muted-foreground mt-1">Manage your multi-asset allocations</p>
                  </div>
                </div>
                <ArrowRight className="h-4 w-4 text-muted-foreground" />
              </div>
            </Link>
            
            <Link href="/research">
              <div className="flex items-center justify-between rounded-lg border p-4 hover:bg-muted/50 transition-colors">
                <div className="flex items-center space-x-4">
                  <div className="bg-primary/10 p-2 rounded-full">
                    <LineChart className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <p className="text-sm font-medium leading-none">Market Research</p>
                    <p className="text-sm text-muted-foreground mt-1">Analyze stocks and market data</p>
                  </div>
                </div>
                <ArrowRight className="h-4 w-4 text-muted-foreground" />
              </div>
            </Link>

            <Link href="/assistant">
              <div className="flex items-center justify-between rounded-lg border p-4 hover:bg-muted/50 transition-colors">
                <div className="flex items-center space-x-4">
                  <div className="bg-primary/10 p-2 rounded-full">
                    <Sparkles className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <p className="text-sm font-medium leading-none">AI Assistant</p>
                    <p className="text-sm text-muted-foreground mt-1">Ask complex financial questions</p>
                  </div>
                </div>
                <ArrowRight className="h-4 w-4 text-muted-foreground" />
              </div>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
