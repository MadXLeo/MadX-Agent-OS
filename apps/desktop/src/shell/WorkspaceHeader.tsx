import { useStore } from '@nanostores/react'
import { IconCommand, IconCpu, IconSearch } from '@tabler/icons-react'
import { PRODUCT } from '../../shared/product.ts'
import { focusSettings } from '../features/settings/sections/shared.tsx'
import { shortcutLabel } from '../lib/platform-labels.ts'
import { $connection } from '../store/gateway.ts'
import { useT } from '../store/i18n.ts'
import { $activeSpace, spaceLabel } from '../store/spaces.ts'
import { toggleCommandBar } from '../store/surface.ts'
import { $page, showPage } from '../store/windows.ts'
import { appById, appName } from './apps.ts'

export function WorkspaceHeader() {
  const t = useT()
  const page = useStore($page)
  const space = useStore($activeSpace)
  const connection = useStore($connection)
  return (
    <header className="madx-workspace-header">
      <div className="madx-breadcrumb"><span>{spaceLabel(space)}</span><span aria-hidden="true">/</span><strong>{appName(appById(page))}</strong></div>
      <button type="button" className="madx-command-trigger" onClick={() => toggleCommandBar(true)}>
        <IconSearch size={16} aria-hidden="true" /><span>{t('madx.search')}</span><kbd>{shortcutLabel('K')}</kbd>
      </button>
      <div className="madx-header-actions">
        <button type="button" className="madx-icon-action" title={PRODUCT.apps.models} aria-label={PRODUCT.apps.models} onClick={() => { focusSettings({ section: 'agents' }); showPage('settings') }}><IconCpu size={18} /></button>
        <span className="madx-engine-state" data-online={connection === 'open'} title={t(connection === 'open' ? 'madx.engineReady' : 'madx.engineOffline')}><IconCommand size={14} /><span>Hermes</span></span>
      </div>
    </header>
  )
}
