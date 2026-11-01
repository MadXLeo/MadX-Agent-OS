import { useStore } from '@nanostores/react'
import { effectiveVisualQuality, normalizeVisualQuality, type VisualQuality } from '../../../../shared/visual-quality.ts'
import { $env, $prefs, updatePrefs } from '../../../store/backend.ts'
import { useT } from '../../../store/i18n.ts'
import { notify } from '../../../store/notifications.ts'
import { errorText, Filterable, markSaved, SettingsGroup } from './shared.tsx'

const MODES = ['auto', 'full', 'balanced', 'performance'] as const

export function VisualQualitySettings() {
  const t = useT()
  const prefs = useStore($prefs)
  const env = useStore($env)
  const selected = normalizeVisualQuality(prefs.visualQuality)
  const effective = effectiveVisualQuality(selected, env?.rendering)
  const choose = async (visualQuality: VisualQuality) => {
    try { await updatePrefs({ visualQuality }); markSaved() }
    catch (error) { notify({ title: t('madx.quality.saveFailed'), body: errorText(error), level: 'error' }) }
  }
  return (
    <SettingsGroup title={t('madx.quality.title')}>
      <Filterable label={t('madx.quality.title')} keywords="glass graphics performance blur rendering automatic balanced">
      <fieldset className="madx-quality">
        <legend className="sr-only">{t('madx.quality.title')}</legend>
        <div className="madx-quality-options">
          {MODES.map(mode => <label key={mode} data-selected={selected === mode}>
            <input type="radio" name="madx-visual-quality" value={mode} checked={selected === mode} onChange={() => void choose(mode)} />
            <span><strong>{t(`madx.quality.${mode}`)}</strong><small>{t(`madx.quality.${mode}Hint`)}</small></span>
          </label>)}
        </div>
        <p aria-live="polite">{t('madx.quality.active', { mode: t(`madx.quality.${effective}`) })} · {t(`madx.quality.${env?.rendering ?? 'unknown'}`)}</p>
        {env?.shellMode === 'panels' && <p>{t('madx.quality.panels')}</p>}
      </fieldset>
      </Filterable>
    </SettingsGroup>
  )
}
