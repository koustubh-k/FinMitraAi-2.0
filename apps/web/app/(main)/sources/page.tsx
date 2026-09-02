export default function SourcesPage() {
  return (
    <div className="flex-1 space-y-4 p-8 pt-6 h-full flex flex-col">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Data Sources</h2>
      </div>
      <div className="flex flex-1 flex-col items-center justify-center rounded-lg border border-dashed shadow-sm">
        <div className="flex flex-col items-center gap-1 text-center">
          <h3 className="text-2xl font-bold tracking-tight">
            Data Sources & Integrations
          </h3>
          <p className="text-sm text-muted-foreground">
            Connect and manage external data streams, APIs, and databases.
          </p>
          <div className="mt-4">
            <span className="inline-flex items-center rounded-md bg-muted px-2 py-1 text-xs font-medium ring-1 ring-inset ring-gray-500/10">
              Coming Soon
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
