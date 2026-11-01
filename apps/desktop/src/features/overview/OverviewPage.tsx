import { useStore } from '@nanostores/react'
import { IconActivity, IconBell, IconPalette, IconSunHigh, IconTargetArrow } from '@tabler/icons-react'
import { useEffect, useState } from 'react'
import { EmptyGlass, LinkAction, Section, StatusDot } from '../../components/ui/glass.tsx'
import { greetingFor } from '../../lib/format.ts'
import { startConversation } from '../../store/bots.ts'
import { $activeChat, $chats, createChat, runSlash, sendPrompt } from '../../store/chat.ts'
import { $pendingRequests } from '../../store/requests.ts'
import { $agents } from '../../store/agents.ts'
import { runCommand } from '../../store/os-commands.ts'
import { focusSettings } from '../settings/sections/shared.tsx'
import { PRODUCT } from '../../../shared/product.ts'
import { $connection } from '../../store/gateway.ts'
import { useT } from '../../store/i18n.ts'
import { $activeMissions, $reviewMissions } from '../../store/missions.ts'
import { useSystemInfo } from '../../store/system.ts'
import { showPage } from '../../store/windows.ts'
import { BotChip } from '../hermes/BotPicker.tsx'
import { MissionCard } from './MissionCard.tsx'
import { OverviewComposer } from './OverviewComposer.tsx'
import { PickUp } from './PickUp.tsx'
import { RecentWork } from './RecentWork.tsx'
import { titleCase } from './shared.tsx'
import { TodayPanel } from './TodayPanel.tsx'
import { SystemHealth } from './SystemHealth.tsx'

const MISSIONS_SHOWN = 3

/** Home of the main window: greeting, prompt, what is in motion and what needs the user. */
export function OverviewPage() {
  const t = useT()
  const connection = useStore($connection)
  const active = useStore($activeMissions)
  const review = useStore($reviewMissions)
  const chats = useStore($chats)
  const chat = useStore($activeChat)
  const agents = useStore($agents)
  const pending = useStore($pendingRequests)
  const working = Object.values(chats).filter(item => item.streaming).length + Object.values(agents).filter(item => item.status === 'running' || item.status === 'queued').length
  const info = useSystemInfo()
  const [now, setNow] = useState(() => new Date())
  const [draft, setDraft] = useState<{ text: string; id: number }>()

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 60_000)

    return () => clearInterval(timer)
  }, [])

  const online = connection === 'open'
  const firstName = titleCase((info?.fullName || info?.userName || '').trim().split(/[\s._-]+/)[0] ?? '')
  const greeting = firstName ? t('overview.greeting.named', { greeting: greetingFor(now), name: firstName }) : t('overview.greeting.plain', { greeting: greetingFor(now) })
  const missions = [...active, ...review].slice(0, MISSIONS_SHOWN)

  const submit = async (text: string, attachments: string[] = []) => {
    if (attachments.length === 0) {
      showPage('hermes')
      await (text.startsWith('/') ? runSlash(text) : sendPrompt(text))

      return
    }

    // The Overview stays until the files have reached Hermes, so a failure comes back to its composer.
    await sendPrompt(text, { attachments })
    showPage('hermes')
  }

  const startMission = async () => {
    showPage('hermes')
    await createChat()
  }

  // With no conversation open, the composer starts one with the bot beside it.
  const ask: typeof submit = async (...args) => {
    if (!$activeChat.get()) {
      await startConversation()
    }

    await submit(...args)
  }

  return (
    <main className="madx-home">
      <header className="madx-home-heading">
        <div><div className="madx-eyebrow">{t('app.overview')} / {PRODUCT.ecosystem}</div><h1>{greeting}</h1></div>
        <time dateTime={now.toISOString()}>{now.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })}</time>
      </header>
      <div className="madx-activity-strip">
        <Activity label={t('madx.working')} value={online ? working : null} icon={<IconActivity size={20} />} onClick={() => showPage('hermes')} />
        <Activity label={t('madx.attention')} value={online ? pending.length + review.length : null} icon={<IconBell size={20} />} onClick={() => pending.length ? void runCommand('requests.focus', {}, { source: 'ui' }) : showPage('missions')} />
        <Activity label={t('madx.missions')} value={online ? active.length : null} icon={<IconTargetArrow size={20} />} onClick={() => showPage('missions')} />
      </div>
      <div className="madx-home-workspace">
        <section className="madx-home-compose">
          <h2>{t('madx.workspace')}</h2>
          <p>{t(online ? 'madx.workspaceHint' : 'madx.offlineHint')}</p>
          <OverviewComposer disabled={!online} placeholder={online ? t('overview.composerPlaceholder') : t('madx.engineOffline')} onSubmit={ask} draft={draft} />
          <div className="madx-home-tools">
            <BotChip disabled={!online} />
            <QuickAction icon={<IconSunHigh />} label={t('overview.planMyDay')} disabled={!online} onClick={() => void ask(t('overview.planMyDayPrompt'))} />
            <QuickAction icon={<IconTargetArrow />} label={t('overview.startMission')} disabled={!online} onClick={() => void startMission()} />
            <QuickAction icon={<IconPalette />} label={t('overview.makeTheme')} disabled={!online} onClick={() => setDraft({ text: t('overview.makeThemeDraft'), id: Date.now() })} />
          </div>
        </section>
        <section className="madx-home-status" aria-label={t('madx.status')}>
          <h2>{t('madx.status')}</h2>
          <dl>
            <div><dt>{t('madx.engine')}</dt><dd className="flex items-center gap-2"><StatusDot tone={online ? 'ok' : 'muted'} />{online ? 'Hermes Agent' : t('madx.engineOffline')}</dd></div>
            <div><dt>{t('madx.model')}</dt><dd>{chat?.info.model || t('madx.noModel')}</dd></div>
            <div><dt>{t('madx.account')}</dt><dd>{info?.fullName || info?.userName || t('madx.localAccount')}</dd></div>
            <SystemHealth />
          </dl>
          <button type="button" onClick={() => { focusSettings({ section: 'agents' }); showPage('settings') }}>{PRODUCT.apps.models} ↗</button>
        </section>
      </div>
      <PickUp />
      <div className="madx-home-work">
        <Section title={t('overview.activeMissions')} action={<LinkAction onClick={() => showPage('missions')}>{t('overview.seeAll')}</LinkAction>}>
          {!online && <p className="mb-3 text-xs text-fg-3">{t('madx.cachedMissions')}</p>}
          {missions.length === 0 ? <EmptyGlass title={t(online ? 'overview.noMissions' : 'madx.unavailable')} description={t(online ? 'overview.noMissionsHint' : 'madx.engineOffline')} /> : <div className="stagger flex flex-col gap-3">{missions.map(mission => <MissionCard key={mission.id} mission={mission} />)}</div>}
        </Section>
        <RecentWork />
      </div>
      <div className="madx-home-context"><TodayPanel now={now} stacked /></div>
    </main>
  )
}

function Activity({ label, value, icon, onClick }: { label: string; value: number | null; icon: React.ReactNode; onClick: () => void }) {
  const t = useT()
  return <button type="button" className="madx-activity-card" onClick={onClick}>{icon}<div><strong aria-label={value === null ? t('madx.unavailable') : undefined}>{value ?? '—'}</strong><span>{label}</span></div></button>
}

function QuickAction({ icon, label, onClick, disabled }: { icon: React.ReactNode; label: string; onClick: () => void; disabled?: boolean }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className="inline-flex h-8 items-center gap-2 rounded-full border border-line bg-white/6 px-3.5 text-[12.5px] text-fg transition-colors duration-120 hover:border-line-strong hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-40 [&_svg]:size-[15px] [&_svg]:text-accent-strong"
    >
      {icon}
      {label}
    </button>
  )
}
