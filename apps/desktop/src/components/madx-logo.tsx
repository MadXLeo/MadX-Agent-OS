import { PRODUCT } from '../../shared/product.ts'
import madxWordmarkUrl from '../assets/brand/madx-wordmark.png'
import madxMarkUrl from '../assets/brand/herald-mark.png'
import { cn } from '../lib/cn.ts'

/** Original supplied artwork. The compact view clips its existing monogram without redrawing it. */
export function MadxLogo({ height = 20, className, wordmark = false }: { height?: number; className?: string; wordmark?: boolean }) {
  if (wordmark) {
    return <img src={madxWordmarkUrl} alt={PRODUCT.name} width={2172} height={724} draggable={false} className={cn('max-w-full shrink-0 select-none object-contain', className)} style={{ height, width: 'auto' }} />
  }
  return (
    <img src={madxMarkUrl} alt={PRODUCT.name} width={height} height={height} draggable={false} className={cn('shrink-0 select-none', className)} />
  )
}
