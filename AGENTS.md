# Working context
Read this file, docs/PLAN.md, docs/MODEL.md and DESIGN.md before relevant changes.

## Requirement
Use real MWQ issues. Never substitute original scenarios. Keep missing information and inferred behavior visible.

## Commands
- python3 scripts/fetch-archive.py — resumable, rate-limited HTTP source fetch; cache in ignored data/raw.
- python3 scripts/import-archive.py — generate catalogue, chunks, policy records, hashes and coverage manifest.
- python3 tests/parser_test.py — fixture tests against actual archived pages.
- npm test — engine tests including 10,000 decisions.
- REQUIRE_COMPLETE_ARCHIVE=1 npm run verify — require all playable issue pages to have detailed records.
- npm run build — dist/ for Pages.
- npm run dev — local server on 5173.
No dependency installation or API key needed. GitHub Actions handles the full durable import and publication.

## File map
src/catalogue.js and src/data are generated factual records; edit the importer instead. src/engine.js handles state, eligibility and effects. src/eligibility.js is the explicitly sourced validity subset. src/personalize.js handles archive placeholders. src/app.js handles rendering and saves. tests/parser_test.py and data/fixtures cover actual source structure.

## Rules
Keep provenance, original option numbers and definite/conditional distinctions. Preserve duplicate option-number variants. Do not claim official formula or full validity parity. No invented dialogue. No random policy triggers. Escape user/source strings before HTML interpolation. Schema changes need migration tests. Read docs/PLAN.md for source limitations.

## Deployment
Pages is enabled with GitHub Actions. Workflow imports, tests, commits generated data and deploys. Confirm its outcome before claiming live changes. Browser smoke test on 2026-10-16 verified the prototype's creation/decision/save flows; repeat after the archive edition publishes.
