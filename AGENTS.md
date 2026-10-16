# Working context
Read this file, docs/PLAN.md, docs/MODEL.md, and DESIGN.md before changes. Only read files relevant to the task.

## Commands
- npm test — model regression suite and 10,000-turn deterministic simulation.
- npm run verify — static integrity and scenario provenance checks.
- npm run build — build dist/ for GitHub Pages.
- npm run dev — preview repository root on port 5173.
No dependencies, backend, keys, or package installation are required.

## File map
- src/catalogue.js: original scenarios and local numeric impacts.
- src/engine.js: pure state transitions, eligibility, saves, classification.
- src/app.js: UI, browser persistence, import/export.
- style.css: responsive tokens/layout.
- tests/engine.test.js: model invariants and regressions.
- .github/workflows/pages.yml: checks gate deployment.

## Non-negotiable rules
Do not claim official NationStates effect/eligibility parity. It is not established. Do not fabricate archive provenance. Preserve original/observed/estimated provenance on future catalogue additions. Never render user data as HTML without escaping. Preserve and validate save migrations when state schema changes. Keep dependencies minimal. Do not introduce an API requirement into local play. Run all three commands before shipping.

## Current limits
36 original recurring issues, not the full official archive; simplified classifications and eligibility; approximate effects. Archive retrieval failed in development. Browser visual QA was unavailable. See docs/PLAN.md before expanding scope.
