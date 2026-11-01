# Reminders, notices and weather

Small things MadX Agent OS Linux tells you when you ask, as a notification.

## Reminders

Say or type "remind me in 20 minutes to stretch", or use Trigger > Reminder… in the MadX Agent OS menu
(`Super+M`). From a terminal:

```bash
madx reminder 20m stretch          # also 90s, 1h, 1h30m
madx reminder list                 # what is coming, and when
madx reminder clear                # cancel them all
```

When it is time, a notification says what you asked to be reminded of. Reminders are kept until you
log out or restart; for something every day or at a set time, make an
[automation](automations.md) instead ("every weekday at 9, remind me to check the post").

## Notices

The Trigger section of the MadX Agent OS menu shows a notice of the time and date, the battery (charge
and whether it is charging), or the weather, for when the menu bar is hidden or you would rather
hear it: with Settings > Voice > Speak notifications on, Hermes reads it out. `madx notice time`,
`madx notice battery` and `madx notice weather` do the same.

## Weather

The weather comes from [wttr.in](https://wttr.in), for the place your network appears to be in. To
set the place yourself:

```bash
madx weather location --set Melbourne     # a city, an airport code, or ~a landmark
madx weather location --clear             # back to automatic
madx weather                              # the weather now
```

Or ask Hermes: "what's the weather like?"

## On a Mac

These commands are part of MadX Agent OS Linux. On a Mac, ask Hermes, or make an automation for anything
that repeats.
