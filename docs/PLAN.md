# Archive implementation status

## User requirement
Use the actual issues at http://www.mwq.dds.nl/ns/results/, with https://nationsofns.fandom.com/wiki/Policies as the policy reference. Original scenarios are not acceptable substitutes.

## Source retrieval
HTTP works; HTTPS requests through the development environment failed. Use the exact HTTP base in scripts/fetch-archive.py. It fetches the index, combined outcome list, policies page and every indexed detailed issue page. Downloads are cached and rate limited; failures are retried and reported. GitHub Actions performs the durable full import, so an interrupted chat does not cancel it.

## What the archive contains
1,871 indexed issue records at the first retrieval, numbered outcomes, measured statistic min/mean/max/sample counts, confirmation dates, and policy transitions. The archive does not publish the full original opening stories or speaker arguments. The app therefore offers an explicitly labeled outcome mode using actual recorded outcomes. It does not write fictional substitutes.

## Implementation
- 85 actual policy definitions; 2,897 option-to-policy relations from the archive's policy page.
- Preserve original option numbers, duplicate-number result variants and source URLs.
- Detailed observations retained in lazy-loaded chunks; nine mapped local indicators use observed means directly, clamped to local 0–100 bounds.
- Definite policy changes applied. Conditional observations are disclosed but not automatically applied, since their triggers are unknown.
- Documented eligibility rules are separate in src/eligibility.js. Other issues explicitly have unknown eligibility. Broad sandbox includes them; verified-only mode restricts the pool.
- Version 1 prototype saves migrate, preserving a legacy backup but clearing fictional policies/history.
- Import fixtures verify real issue #0 and #65, numeric mean parsing, sample counts, and definite/conditional policy distinctions.
- Workflow gates publication on complete detailed-page coverage, parser tests, model tests, source integrity and build.

## Remaining fidelity limits
Most validity conditions and official numerical formulas are not public in this source. Observed means do not reproduce those formulas. Only two issue prerequisites have currently been curated. Full debate prose is absent. The requested Fandom policy page is blocked to retrieval in this environment; its role was established through the available search excerpt, while actual policy definitions and mappings come from MWQ's policies page. Do not claim complete official-game rule parity.

## Deployment
.github/workflows/pages.yml imports the full archive, validates it, commits the generated snapshot, and deploys Pages. Cached downloads survive reruns. The existing live version stays unchanged if import or verification fails. Inspect the workflow result before claiming publication.
