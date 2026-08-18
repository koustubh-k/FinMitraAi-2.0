import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex flex-col items-center justify-center p-8 font-sans">
      <main className="max-w-2xl w-full border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm bg-white dark:bg-slate-900 overflow-hidden">
        
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b border-slate-100 dark:border-slate-800">
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
            FinMitra
          </h1>
          <button className="text-sm font-medium text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition-colors">
            Sign In
          </button>
        </div>

        {/* Hero Content */}
        <div className="p-12 text-center space-y-6">
          <div className="space-y-2">
            <h2 className="text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">
              Financial Intelligence
            </h2>
            <p className="text-lg text-slate-500 dark:text-slate-400">
              powered by evidence
            </p>
          </div>

          <div className="flex justify-center gap-4 text-sm font-medium text-slate-600 dark:text-slate-300 pt-4">
            <span>Research</span>
            <span className="text-slate-300 dark:text-slate-700">•</span>
            <span>Portfolio</span>
            <span className="text-slate-300 dark:text-slate-700">•</span>
            <span>Insights</span>
          </div>
        </div>

        {/* CTA */}
        <div className="p-8 bg-slate-50 dark:bg-slate-900/50 flex justify-center border-t border-slate-100 dark:border-slate-800">
          <Link 
            href="#"
            className="inline-flex h-10 items-center justify-center rounded-md bg-slate-900 px-8 text-sm font-medium text-slate-50 shadow transition-colors hover:bg-slate-900/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-slate-950 disabled:pointer-events-none disabled:opacity-50 dark:bg-slate-50 dark:text-slate-900 dark:hover:bg-slate-50/90 dark:focus-visible:ring-slate-300"
          >
            Get Started
          </Link>
        </div>

      </main>
    </div>
  )
}
