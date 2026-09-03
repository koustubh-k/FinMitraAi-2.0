"use client";

import { useEffect, useState } from "react";
import { BadgeDelta, Card as TremorCard, Flex, Grid, Metric, Text } from "@tremor/react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { config } from "@/lib/config";

export default function Home() {
  const [backendStatus, setBackendStatus] = useState<
    "checking" | "connected" | "unavailable"
  >("checking");
  const [responseTime, setResponseTime] = useState<number | null>(null);

  const checkBackendHealth = async () => {
    setBackendStatus("checking");
    const startTime = performance.now();
    try {
      const response = await fetch(config.healthEndpoint, {
        cache: "no-store",
      });
      const duration = Math.round(performance.now() - startTime);
      setResponseTime(duration);

      if (response.ok) {
        const data = await response.json();
        if (data.status === "ok") {
          setBackendStatus("connected");
          return;
        }
      }
      setBackendStatus("unavailable");
    } catch {
      setBackendStatus("unavailable");
      setResponseTime(null);
    }
  };

  useEffect(() => {
    checkBackendHealth();
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50 p-6 md:p-12 lg:p-16">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Top Bar */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-3xl font-extrabold tracking-tight">
                FinMitra 2.0
              </h1>
              <Badge variant="outline" className="text-blue-400 border-blue-900 bg-blue-950/40">
                Phase 0 Foundation
              </Badge>
            </div>
            <p className="text-slate-400 text-sm mt-1">
              Evidence-First Financial Intelligence Platform
            </p>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400">System Status:</span>
              {backendStatus === "connected" && (
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-950/80 text-emerald-400 border border-emerald-800">
                  <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                  Backend connected
                </span>
              )}
              {backendStatus === "unavailable" && (
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-rose-950/80 text-rose-400 border border-rose-800">
                  <span className="h-2 w-2 rounded-full bg-rose-500" />
                  Backend unavailable
                </span>
              )}
              {backendStatus === "checking" && (
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-slate-900 text-slate-300 border border-slate-700">
                  <span className="h-2 w-2 rounded-full bg-slate-400 animate-spin" />
                  Checking connection...
                </span>
              )}
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={checkBackendHealth}
              disabled={backendStatus === "checking"}
            >
              Re-check Health
            </Button>
          </div>
        </div>

        {/* Tremor KPI Metrics Grid */}
        <div>
          <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400 mb-4">
            Financial Dashboard Preview (Tremor Components)
          </h2>
          <Grid numItemsSm={1} numItemsMd={2} numItemsLg={3} className="gap-6">
            <TremorCard className="bg-slate-900/80 border-slate-800 ring-0 p-6 rounded-xl">
              <Flex alignItems="start">
                <div>
                  <Text className="text-slate-400 text-xs uppercase font-medium">
                    Backend Health Status
                  </Text>
                  <Metric className="text-2xl font-bold text-slate-100 mt-1">
                    {backendStatus === "connected"
                      ? "Healthy"
                      : backendStatus === "unavailable"
                      ? "Offline"
                      : "Verifying"}
                  </Metric>
                </div>
                <BadgeDelta
                  deltaType={
                    backendStatus === "connected"
                      ? "increase"
                      : backendStatus === "unavailable"
                      ? "decrease"
                      : "unchanged"
                  }
                  size="xs"
                >
                  {backendStatus === "connected" ? "200 OK" : "Health Check"}
                </BadgeDelta>
              </Flex>
              <Flex className="mt-4 pt-4 border-t border-slate-800/80">
                <Text className="text-xs text-slate-400">Response Latency</Text>
                <Text className="text-xs font-mono text-slate-300">
                  {responseTime !== null ? `${responseTime} ms` : "N/A"}
                </Text>
              </Flex>
            </TremorCard>

            <TremorCard className="bg-slate-900/80 border-slate-800 ring-0 p-6 rounded-xl">
              <Flex alignItems="start">
                <div>
                  <Text className="text-slate-400 text-xs uppercase font-medium">
                    PostgreSQL Infrastructure
                  </Text>
                  <Metric className="text-2xl font-bold text-slate-100 mt-1">
                    Port 5433
                  </Metric>
                </div>
                <BadgeDelta deltaType="increase" size="xs">
                  pgvector/pg16
                </BadgeDelta>
              </Flex>
              <Flex className="mt-4 pt-4 border-t border-slate-800/80">
                <Text className="text-xs text-slate-400">Alembic Migrations</Text>
                <Text className="text-xs font-mono text-emerald-400">
                  Head (fa95eccbeedb)
                </Text>
              </Flex>
            </TremorCard>

            <TremorCard className="bg-slate-900/80 border-slate-800 ring-0 p-6 rounded-xl">
              <Flex alignItems="start">
                <div>
                  <Text className="text-slate-400 text-xs uppercase font-medium">
                    Distributed Redis Cache
                  </Text>
                  <Metric className="text-2xl font-bold text-slate-100 mt-1">
                    Port 6380
                  </Metric>
                </div>
                <BadgeDelta deltaType="increase" size="xs">
                  Redis 7
                </BadgeDelta>
              </Flex>
              <Flex className="mt-4 pt-4 border-t border-slate-800/80">
                <Text className="text-xs text-slate-400">Persistence</Text>
                <Text className="text-xs font-mono text-slate-300">
                  redis_data volume
                </Text>
              </Flex>
            </TremorCard>
          </Grid>
        </div>

        {/* shadcn/ui Architecture Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base font-semibold">
                Monorepo Decoupled Architecture
              </CardTitle>
              <CardDescription>
                Next.js 14 frontend and FastAPI backend communicating via asynchronous REST endpoints
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              <div className="flex justify-between items-center py-1.5 border-b border-slate-800">
                <span className="text-slate-400">Target API URL:</span>
                <code className="text-xs font-mono text-blue-400 bg-slate-950 px-2 py-0.5 rounded">
                  {config.apiUrl}
                </code>
              </div>
              <div className="flex justify-between items-center py-1.5 border-b border-slate-800">
                <span className="text-slate-400">UI Component Library:</span>
                <span className="text-xs font-medium text-slate-200">
                  shadcn/ui + Tremor React Hybrid
                </span>
              </div>
              <div className="flex justify-between items-center py-1.5">
                <span className="text-slate-400">TypeScript Mode:</span>
                <span className="text-xs font-medium text-emerald-400">
                  Strict Mode Enforced
                </span>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base font-semibold">
                Phase 0 Foundation Checklist
              </CardTitle>
              <CardDescription>
                Zero technical debt baseline ready for Phase 1 domain modeling
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2.5 text-xs">
              <div className="flex items-center gap-2">
                <span className="text-emerald-400 font-bold">✓</span>
                <span>FastAPI with centralized error handling & CORS</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-emerald-400 font-bold">✓</span>
                <span>SQLAlchemy async engine & Alembic baseline migration</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-emerald-400 font-bold">✓</span>
                <span>Custom host ports: PostgreSQL 5433, Redis 6380</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-emerald-400 font-bold">✓</span>
                <span>DevSecOps: Pre-commit, strict .gitignore, Gitleaks</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
}
