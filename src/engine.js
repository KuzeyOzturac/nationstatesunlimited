import {issues,stats} from './catalogue.js';
export const VERSION=1;
export function createNation(input){
 const name=String(input.name||'').trim(); if(name.length<2||name.length>48)throw Error('Country name must contain 2–48 characters.');
 const base={pluralist:[72,75,55],balanced:[50,50,50],authoritarian:[25,20,45],market:[55,55,80]}[input.start]||[50,50,50];
 return {version:VERSION,name,motto:String(input.motto||'A future of our own.').slice(0,120),currency:String(input.currency||'crown').slice(0,30),animal:String(input.animal||'fox').slice(0,30),color:/^#[0-9a-f]{6}$/i.test(input.color)?input.color:'#b9a369',turn:0,population:5000000,stats:Object.fromEntries(Object.keys(stats).map((k,i)=>[k,i<3?base[i]:50])),policies:{},history:[],recent:[],active:null};
}
export function eligible(n,issue){return !issue.requires||Object.entries(issue.requires).every(([k,v])=>n.policies[k]===v);}
export function availableOptions(n,issue){return issue.options.map((o,index)=>({...o,index})).filter(o=>n.policies[issue.topic]!==o.policy);}
export function nextIssue(n,rng=Math.random){
 const pool=issues.filter(i=>eligible(n,i)&&!n.recent.slice(-12).includes(i.id));
 if(!pool.length)throw Error('No eligible issues. Check catalogue rules.');
 const issue=pool[Math.min(pool.length-1,Math.floor(rng()*pool.length))];return {...n,active:issue.id};
}
export function preview(n,option){return Object.fromEntries(Object.entries(option.effects).map(([k,v])=>{const current=n.stats[k];const change=v*(v>0?(100-current)/100:current/100);return [k,Math.round((Math.max(0,Math.min(100,current+change))-current)*100)/100];}));}
export function decide(n,index){
 const issue=issues.find(i=>i.id===n.active);if(!issue||!eligible(n,issue))throw Error('This issue is no longer eligible.');
 const option=index===null?null:availableOptions(n,issue).find(o=>o.index===index);if(index!==null&&!option)throw Error('Invalid or already enacted option.');
 const delta=option?preview(n,option):{};const updated={...n.stats};for(const [k,v]of Object.entries(delta))updated[k]=Math.round((updated[k]+v)*100)/100;
 const record={turn:n.turn+1,id:issue.id,title:issue.title,choice:option?.text||'Dismissed',result:option?.result||'No policy was changed.',delta};
 return {...n,turn:n.turn+1,population:option?Math.round(n.population*1.001):n.population,stats:updated,policies:option?{...n.policies,[issue.topic]:option.policy}:n.policies,history:[record,...n.history].slice(0,500),recent:[...n.recent,issue.id].slice(-24),active:null};
}
export function classification(n){const {civil:c,political:p,economic:e}=n.stats;if(p<33)return c<33?'Authoritarian State':'Benevolent Autocracy';if(p>66&&c>66)return e>66?'Capitalist Democracy':'Civil Rights Democracy';if(e>66)return 'Market Republic';if(c>66)return 'Liberal Republic';return 'Constitutional Republic';}
export function validateSave(n){
 if(!n||n.version!==VERSION||typeof n.name!=='string'||n.name.length<2||n.name.length>48||!Number.isSafeInteger(n.turn)||n.turn<0||!Number.isFinite(n.population)||n.population<1||!n.stats||!n.policies||typeof n.policies!=='object'||Array.isArray(n.policies)||!Array.isArray(n.history)||n.history.length>500||!Array.isArray(n.recent)||n.recent.length>24)throw Error('Invalid or unsupported save file.');
 for(const k of Object.keys(stats))if(!Number.isFinite(n.stats[k])||n.stats[k]<0||n.stats[k]>100)throw Error('Invalid national statistics.');
 for(const key of ['motto','currency','animal','color'])if(typeof n[key]!=='string'||n[key].length>120)throw Error('Invalid country details.');
 for(const [key,value]of Object.entries(n.policies))if(!issues.some(i=>i.topic===key&&i.options.some(o=>o.policy===value)))throw Error('Unknown policy in save.');
 if(n.active!==null&&!issues.some(i=>i.id===n.active&&eligible(n,i)))throw Error('Invalid active issue.');
 for(const row of n.history)if(!row||typeof row.title!=='string'||typeof row.choice!=='string'||typeof row.result!=='string'||!Number.isInteger(row.turn)||!row.delta||Object.entries(row.delta).some(([k,v])=>!Object.hasOwn(stats,k)||!Number.isFinite(v)))throw Error('Invalid decision history.');
 return n;
}
