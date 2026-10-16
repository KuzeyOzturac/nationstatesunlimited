import {readFile} from 'node:fs/promises';import assert from 'node:assert/strict';import {issues,stats,policyCatalogue,coverage} from '../src/catalogue.js';
const files=['index.html','style.css','src/app.js','src/engine.js','src/catalogue.js','src/eligibility.js','src/personalize.js','.github/workflows/pages.yml','AGENTS.md','DESIGN.md','docs/PLAN.md'];for(const file of files)await readFile(file);
const known=new Set(policyCatalogue.map(p=>p.name));let observations=0;for(let c=0;c<Math.ceil(coverage.issues/100);c++){
 const chunk=JSON.parse(await readFile(`src/data/issues-${String(c).padStart(2,'0')}.json`));for(const i of chunk){for(const o of i.options){for(const p of o.policyChanges)assert.ok(known.has(p.policy),`Unknown policy: ${p.policy}`);for(const r of o.observations){assert.ok(Number.isFinite(r.mean));assert.ok(r.min<=r.max);assert.ok(r.samples===null||Number.isInteger(r.samples));observations++;}}}
}
for(const issue of issues){assert.equal(issue.provenance,'mwq-observed');for(const o of issue.options)for(const [k,v]of Object.entries(o.effects)){assert.ok(Object.hasOwn(stats,k));assert.ok(Number.isFinite(v));}}
if(process.env.REQUIRE_COMPLETE_ARCHIVE==='1')assert.equal(coverage.missingDetailIds.length,0,`Missing detailed pages: ${coverage.missingDetailIds.join(',')}`);
console.log(`Verified ${issues.length} sourced issues, ${policyCatalogue.length} policies and ${observations} observed statistical records. Missing detailed pages: ${coverage.missingDetailIds.length}.`);
