import * as React from "react"

const MOBILE_BREAKPOINT = 768

export function useIsMobile() {
  const [isMobile, setIsMobile] = React.useState<boolean | undefined>(undefined)

  React.useEffect(() => {
    const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`)
    const onChange = () => {
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    }
    mql.addEventListener("change", onChange)
    
    // Use a timeout or just set it if we want it initially, wait the warning says "Calling setState synchronously within an effect can trigger cascading renders".
    // It's actually better to just initialize it in state or use a timeout. Or use window.matchMedia().matches.
    // Let's just do it in onChange and initialize it in state if possible, but window is undefined in SSR.
    // So we can wrap the initial set in requestAnimationFrame.
    requestAnimationFrame(() => {
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    })
    
    return () => mql.removeEventListener("change", onChange)
  }, [])

  return !!isMobile
}
