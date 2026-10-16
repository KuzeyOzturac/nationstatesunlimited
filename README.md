# NationStates Unlimited — archive edition
Create a country and play the actual numbered outcomes from [Milo's NationStates results archive](http://www.mwq.dds.nl/ns/results/) without a daily timer.

The original 36 fictional scenarios have been removed from the new source implementation. The archive has titles and outcome lines, not the original debate text; the app clearly offers an outcome-based mode. Observed statistical means drive nine local indicators. Named policy changes are sourced, with conditional changes disclosed rather than guessed.

[Play](https://kuzeyozturac.github.io/nationstatesunlimited/) · [Implementation status](docs/PLAN.md) · [Model](docs/MODEL.md)

## Setup
Node 22+ and Python 3; no package install or API key.
```
python3 scripts/fetch-archive.py
python3 scripts/import-archive.py
python3 tests/parser_test.py
npm test
REQUIRE_COMPLETE_ARCHIVE=1 npm run verify
npm run build
npm run dev
```
Open http://localhost:5173. Generated data is committed by Actions after a successful complete import. Detailed source ranges/sample counts are loaded only when inspected. Raw HTML is cached locally and in Actions, not published as part of the app.

## Verification and deployment
The Pages workflow fetches every indexed detailed record with caching/rate limiting, tests the real HTML parser and engine, requires complete playable-record coverage, commits the generated snapshot, then publishes. A failed import does not replace the existing live app. Check Actions before assuming the new edition is live.

## Fidelity
The archive does not expose official hidden formulas or most validity conditions. Means are observations, not exact future predictions. Broad mode marks unknown eligibility; verified-only mode restricts to the small documented subset. Policies marked “sometimes” are not automatically enacted. Government classifications remain simplified local labels. No official account is accessed or modified.

Policy reference requested by the user: https://nationsofns.fandom.com/wiki/Policies . The accessible search excerpt explains how issues enact/cancel policies and how policies affect later issues; the full Fandom page was blocked. Actual definitions and option mappings are imported from http://www.mwq.dds.nl/ns/results/policies.html .

## Saves
Browser-local progress with JSON export/import. Version 1 prototype saves migrate with the legacy data preserved in the export. Fictional laws/history are cleared from active play. Export backups before changing devices.

## Attribution
Observed data and outcome records compiled by Milo (Milostein / Trotterdam); source links and per-page hashes are retained. NationStates issue titles/outcomes belong to their respective creators. Independent fan project, not affiliated with NationStates or Max Barry. See the [official technical discussion](https://forum.nationstates.net/viewtopic.php?f=15&t=556705) about secret effect calculations.
