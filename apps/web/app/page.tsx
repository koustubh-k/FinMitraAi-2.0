import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, BarChart3, BrainCircuit, ShieldCheck, Zap } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-black text-slate-50 selection:bg-indigo-500/30">
      {/* Background Gradients */}
      <div className="pointer-events-none fixed inset-0 flex justify-center bg-black [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)]"></div>
      <div className="pointer-events-none fixed top-[-20%] left-[-10%] h-[500px] w-[500px] rounded-full bg-indigo-500/20 blur-[120px] mix-blend-screen" />
      <div className="pointer-events-none fixed top-[20%] right-[-10%] h-[400px] w-[400px] rounded-full bg-blue-500/10 blur-[120px] mix-blend-screen" />

      {/* Navigation */}
      <header className="relative z-50 flex items-center justify-between px-6 py-6 lg:px-12">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-indigo-500 to-blue-600 shadow-[0_0_15px_rgba(99,102,241,0.5)]">
            <BarChart3 className="h-5 w-5 text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight">FinMitra 2.0</span>
        </div>
        <nav className="flex items-center gap-6">
          <Link href="/login" className="text-sm font-medium text-slate-300 transition-colors hover:text-white">
            Log in
          </Link>
          <Link href="/register">
            <Button className="bg-indigo-600 text-white hover:bg-indigo-500 shadow-[0_0_15px_rgba(99,102,241,0.3)] border-0">
              Get Started
            </Button>
          </Link>
        </nav>
      </header>

      <main className="relative z-10 mx-auto max-w-7xl px-6 pt-24 pb-32 sm:pt-32 lg:px-8">
        {/* Hero Section */}
        <div className="mx-auto max-w-4xl text-center">
          <div className="mb-8 inline-flex items-center rounded-full border border-indigo-500/30 bg-indigo-500/10 px-3 py-1 text-sm font-medium text-indigo-300 ring-1 ring-inset ring-indigo-500/20">
            <span className="flex h-2 w-2 rounded-full bg-indigo-500 mr-2 animate-pulse"></span>
            FinMitra 2.0 is now live
          </div>
          <h1 className="text-5xl font-extrabold tracking-tight sm:text-7xl bg-gradient-to-br from-white to-slate-400 bg-clip-text text-transparent pb-4">
            Next-Generation <br className="hidden sm:block" /> Financial Intelligence
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-400">
            Advanced portfolio management and market research, powered by deterministic engines and state-of-the-art AI. Experience the future of finance today.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <Link href="/register">
              <Button size="lg" className="h-14 rounded-full bg-indigo-600 px-8 text-base text-white hover:bg-indigo-500 shadow-[0_0_25px_rgba(99,102,241,0.4)] border-0 group">
                Open App 
                <ArrowRight className="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
            <Link href="/login">
              <Button variant="outline" size="lg" className="h-14 rounded-full border-slate-700 bg-transparent px-8 text-base text-white hover:bg-slate-800">
                Sign in to account
              </Button>
            </Link>
          </div>
        </div>

        {/* Feature Grid */}
        <div className="mx-auto mt-32 max-w-5xl sm:mt-40">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {/* Feature 1 */}
            <div className="group relative rounded-2xl border border-slate-800 bg-slate-900/50 p-8 backdrop-blur-xl transition-colors hover:border-indigo-500/50">
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-indigo-500/20 text-indigo-400">
                <BrainCircuit className="h-6 w-6" />
              </div>
              <h3 className="mb-2 text-lg font-semibold text-white">Multi-Agent AI</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Interact with autonomous financial agents that research markets, analyze documents, and execute tasks on your behalf.
              </p>
            </div>
            
            {/* Feature 2 */}
            <div className="group relative rounded-2xl border border-slate-800 bg-slate-900/50 p-8 backdrop-blur-xl transition-colors hover:border-blue-500/50">
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-blue-500/20 text-blue-400">
                <BarChart3 className="h-6 w-6" />
              </div>
              <h3 className="mb-2 text-lg font-semibold text-white">Real-Time Data</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Connects directly to global exchanges for real-time quotes, historical data, and fundamental analysis.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="group relative rounded-2xl border border-slate-800 bg-slate-900/50 p-8 backdrop-blur-xl transition-colors hover:border-emerald-500/50">
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-emerald-500/20 text-emerald-400">
                <ShieldCheck className="h-6 w-6" />
              </div>
              <h3 className="mb-2 text-lg font-semibold text-white">Enterprise Security</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Built with a deterministic financial engine, robust safety layers, and end-to-end encryption for your portfolio.
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-slate-800 py-8">
        <div className="mx-auto max-w-7xl px-6 flex items-center justify-between lg:px-8">
          <p className="text-sm text-slate-500">
            © {new Date().getFullYear()} FinMitra AI. All rights reserved.
          </p>
          <div className="flex items-center gap-4 text-sm text-slate-500">
            <a href="#" className="hover:text-white transition-colors">Privacy</a>
            <a href="#" className="hover:text-white transition-colors">Terms</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
