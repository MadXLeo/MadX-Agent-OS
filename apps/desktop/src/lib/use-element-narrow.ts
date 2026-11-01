import { useEffect, useState, type RefObject } from 'react'

/** Follow the actual tile width, including niri tiling and display scaling, without saving a preference. */
export function useElementNarrow(ref: RefObject<HTMLElement | null>, threshold: number): boolean {
  const [narrow, setNarrow] = useState(false)
  useEffect(() => {
    const element = ref.current
    if (!element) return
    const update = () => setNarrow(element.clientWidth > 0 && element.clientWidth < threshold)
    update()
    const observer = new ResizeObserver(update)
    observer.observe(element)
    return () => observer.disconnect()
  }, [ref, threshold])
  return narrow
}
