import {mkdir,cp,rm,readFile,writeFile,readdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
async function walk(dir){const out=[];for(const entry of await readdir(dir,{withFileTypes:true})){const path=dir+'/'+entry.name;if(entry.isDirectory())out.push(...await walk(path));else out.push(path);}return out.sort();}
const sources=['index.html','style.css',...await walk('src')];const digest=createHash('sha256');for(const file of sources){digest.update(file);digest.update(await readFile(file));}const version=digest.digest('hex').slice(0,12);
await rm('dist',{recursive:true,force:true});await mkdir('dist');for(const file of ['index.html','style.css','src'])await cp(file,`dist/${file}`,{recursive:true});await cp('.nojekyll','dist/.nojekyll');
for(const file of await walk('dist/src'))if(file.endsWith('.js')){const source=await readFile(file,'utf8');await writeFile(file,source.replace(/((?:from|import)\s*['"])(\.[^'"]+\.js)(['"])/g,`$1$2?v=${version}$3`));}
const html=await readFile('dist/index.html','utf8');await writeFile('dist/index.html',html.replaceAll('./style.css',`./style.css?v=${version}`).replaceAll('./src/app.js',`./src/app.js?v=${version}`));console.log(`Built static site in dist/; asset version ${version}`);
