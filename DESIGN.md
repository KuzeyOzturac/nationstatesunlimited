# Design memory
Last updated: 2026-10-16

## Direction
Government briefing desk: warm paper, forest green ink, restrained brass. A country dashboard with tabbed work areas; no marketing card grid. DM Sans, with sans-serif fallback. No imagery is necessary for the task.

## Tokens
Background #f4f2e9; ink #142e2a; muted #62726a; border #d6dbcf; accent #b9a369. Borders 1px, radius 3–4px. Main maximum 1440px; desktop sidebar 255px. 850px breakpoint stacks columns, 450px stacks form controls.

## Interaction
Country creation is the initial screen. Show one issue at a time. Select then enact to prevent accidental choices. Effects are optional previews. Outcomes precede the next issue, so no waiting is required. Keep dismiss clearly separate. Export always available. Destructive local replacement uses keyboard-trapped confirmation with Escape and cancellation.

## Accessibility
Native buttons, visible focus, labeled fields, meter values, live outcome/error feedback, reduced-motion override. Test narrow screens and keyboard navigation before declaring visual QA complete.

## States
No country: founding charter. No history/policy: actionable empty text. Invalid import/corrupt storage/quota failure: visible inline error. Enactment: outcome with exact model deltas. No network dependency for play; external font is optional.

## Archive edition
Keep the briefing desk layout. Show source issue number, archive link and eligibility evidence before choosing. Label recorded outcomes explicitly; do not imply original debate prose. Optional observation tables retain ranges/means/sample counts. Conditional policy changes must be readable in outcomes. Broad versus verified-only eligibility is an explicit setting.
