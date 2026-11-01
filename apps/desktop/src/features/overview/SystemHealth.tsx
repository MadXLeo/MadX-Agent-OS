import { useEffect, useState } from 'react'
import { formatPercent } from '../../lib/format.ts'
import { useT } from '../../store/i18n.ts'
import { useSystemStats } from '../../store/system.ts'

/** Reuse the reference-counted native sampler; an old sample is not current health. */
export function SystemHealth() {
  const t = useT()
  const stats = useSystemStats()
  const [now, setNow] = useState(Date.now)
  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), 10_000)
    return () => clearInterval(timer)
  }, [])
  const fresh = stats && Math.max(now, Date.now()) - stats.sampledAt < 15_000
  const cpu = fresh && Number.isFinite(stats.cpuPercent) && stats.cpuPercent >= 0 && stats.cpuPercent <= 100 ? formatPercent(stats.cpuPercent) : t('madx.unavailable')
  const memory = fresh && stats.memoryTotal > 0 && stats.memoryUsed >= 0 && stats.memoryUsed <= stats.memoryTotal ? formatPercent(stats.memoryUsed / stats.memoryTotal * 100) : t('madx.unavailable')
  return <div><dt>{t('madx.systemHealth')}</dt><dd>{t('madx.systemReadings', { cpu, memory })}</dd></div>
}
