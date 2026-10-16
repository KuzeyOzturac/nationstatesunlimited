# NationStates Unlimited
An independent, browser-local political sandbox. Create a nation, decide issues without a daily timer, see changes, and export your country.

**Fidelity status:** 36 original recurring scenarios, approximate local effects and simplified eligibility. This release does not contain the supplied archive or reproduce the hidden official game rules. The archive was unreachable during development. See [the plan](docs/PLAN.md) for the outstanding catalogue/fidelity work.

## Run
Requires Node 22+ and Python 3 for the optional preview.
```
npm test
npm run verify
npm run build
npm run dev
```
Open http://localhost:5173. No install step or API keys. Built output is dist/. GitHub Pages uses relative assets and ES modules.

## Deployment
The Pages workflow runs tests and verification before building and publishing. Repository Settings → Pages → Source must be GitHub Actions if automatic enablement is denied. Expected URL: https://kuzeyozturac.github.io/nationstatesunlimited/ . Do not assume deployment succeeded until Actions confirms it.

## Data and backups
LocalStorage stores the active country. Export a JSON backup before switching browsers or creating a new country. Imports are validated before confirmation. No data is sent to a server. External Google Fonts may receive standard font requests; play works with a fallback font offline once assets are cached.

## Sources
- Requested observed-effect archive: https://www.mwq.dds.nl/ns/results/
- Official discussion of secret effect formulas: https://forum.nationstates.net/viewtopic.php?f=15&t=556705
All bundled scenario prose and coefficients are original. No affiliation with NationStates or Max Barry.

Read AGENTS.md for focused maintenance context, DESIGN.md for visual decisions, and docs/MODEL.md for the state contract.
