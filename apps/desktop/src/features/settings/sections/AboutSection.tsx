import { PRODUCT } from '../../../../shared/product.ts'
import { useStore } from '@nanostores/react'
import { IconDownload, IconFileText, IconInfoCircle, IconServer } from '@tabler/icons-react'
import { useState } from 'react'
import { GlassButton, Pill } from '../../../components/ui/glass.tsx'
import { type HermesStatusPayload, rest } from '../../../lib/rest.ts'
import { useBackendData, useLocalData } from '../../../lib/use-async.ts'
import { $backend, $env } from '../../../store/backend.ts'
import { openApp } from '../../../store/windows.ts'
import { AboutIdentity, BrandingSettings } from './BrandingSettings.tsx'
import { useT } from '../../../store/i18n.ts'
import { LogView, SectionTitle, SettingsGroup, SettingsRow } from './shared.tsx'

export function AboutSection() {
  const t = useT()
  const env = useStore($env)
  const backend = useStore($backend)
  const status = useBackendData(() => rest.get<HermesStatusPayload>('/api/status'))
  const [showLog, setShowLog] = useState(false)
  const log = useLocalData(() => (showLog ? window.heraldOS.backend.logTail(300) : Promise.resolve<string[]>([])), [showLog, backend.phase])

  return (
    <>
      <SectionTitle title={t('settings.section.about')} subtitle={t('settings.about.subtitle')} />

      <AboutIdentity />

      <SettingsGroup title="Versions">
        <SettingsRow icon={<IconInfoCircle />} label={PRODUCT.name} description={env?.isDev ? 'Development build.' : 'Agent-native operating system.'} keywords="version build shell">
          <Pill tone="accent">{env?.version ?? '—'}</Pill>
        </SettingsRow>
        <SettingsRow icon={<IconServer />} label="Hermes runtime" description={<span className="selectable">{backend.runtime?.label ?? 'Not resolved yet.'}</span>} keywords="hermes agent version runtime">
          <Pill>{status.data?.version && status.data.version !== 'unknown' ? `v${String(status.data.version).replace(/^v/, '')}` : status.loading ? '…' : 'unknown'}</Pill>
          {backend.runtime && <Pill>{backend.runtime.kind}</Pill>}
        </SettingsRow>
      </SettingsGroup>

      <BrandingSettings />

      <SettingsGroup title="Legal and open source">
        <SettingsRow icon={<IconInfoCircle />} label={PRODUCT.ecosystem} description={`${PRODUCT.name} is a distribution derived from Herald OS. Upstream copyright © 2026 Luke The Dev; MIT license. See the bundled LICENSE and NOTICE for full terms and third-party notices.`} keywords="legal license copyright upstream" />
        <SettingsRow icon={<IconServer />} label="Hermes Agent" description={`The independently maintained agent engine from Nous Research, used under its MIT license. ${PRODUCT.name} is not an official Nous Research product and is not endorsed by Nous Research.`} keywords="legal hermes nous license" />
      </SettingsGroup>

      <SettingsGroup title="Maintenance">
        <SettingsRow icon={<IconDownload />} label="Check for updates" description={`${PRODUCT.name} runs whatever Hermes is installed. Run “hermes update” in Terminal, then restart Hermes from Network.`} keywords="upgrade update hermes update terminal">
          <GlassButton size="sm" onClick={() => openApp('terminal')} aria-label="Open Terminal">
            Open Terminal
          </GlassButton>
        </SettingsRow>
        <SettingsRow
          icon={<IconFileText />}
          label="Open logs"
          description="The last 300 lines from the Hermes backend this shell started."
          keywords="log output debug backend"
          below={showLog ? <LogView lines={log.data ?? []} empty={log.loading ? 'Loading…' : 'No log output yet.'} className="animate-rise" /> : undefined}
        >
          {showLog && (
            <GlassButton size="sm" variant="ghost" onClick={log.reload}>
              Refresh
            </GlassButton>
          )}
          <GlassButton size="sm" onClick={() => setShowLog(o => !o)} aria-label={showLog ? 'Hide logs' : 'Open logs'}>
            {showLog ? 'Hide logs' : 'Open logs'}
          </GlassButton>
        </SettingsRow>
      </SettingsGroup>
    </>
  )
}
