#!/usr/bin/env python3
"""Build and install Atlas studios from verified upstream sources. Python 3.10+."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
STUDIOS = {
    'growth': ('atlas-growth-social', 'Atlas Growth & Social', 79),
    'creative': ('atlas-creative-production', 'Atlas Creative Production', 79),
    'engineering': ('atlas-engineering-tools', 'Atlas Engineering Tools', 69),
}
VERSION = '1.3.0'


def contained(root, relative):
    """Reject catalog/archive paths that could escape a managed directory."""
    if not isinstance(relative,str) or not relative or '\\' in relative or ':' in relative or re.search(r'[\x00-\x1f]',relative):
        raise ValueError(f'Invalid relative path: {relative!r}')
    parts = PurePosixPath(relative).parts
    if relative.startswith('/') or any(p in {'.','..'} or p.lower()=='.git' for p in parts):
        raise ValueError(f'Unsafe relative path: {relative!r}')
    target = root.joinpath(*parts)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes managed directory: {relative!r}')
    return target


def digest(data):
    return hashlib.sha256(data).hexdigest()


def patched(data, edits):
    lines = data.decode('utf-8').splitlines(keepends=True)
    previous = len(lines)+1
    for edit in reversed(edits):
        start,end = edit['start'],edit['end']
        if not (isinstance(start,int) and isinstance(end,int) and 0 <= start <= end < previous <= len(lines)+1):
            raise ValueError('Invalid or overlapping patch range')
        if not isinstance(edit['lines'],list) or not all(isinstance(s,str) for s in edit['lines']):
            raise ValueError('Patch replacement must contain text lines')
        lines[start:end] = edit['lines']
        previous = start+1
    return ''.join(lines).encode('utf-8')


def run(arguments, **kwargs):
    subprocess.run([str(a) for a in arguments], check=True, **kwargs)


def source_tree(key, record, paths, cache):
    repo,commit = record['repository'],record['commit']
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo) or not re.fullmatch(r'[0-9a-f]{40}',commit):
        raise ValueError(f'Invalid pinned source: {key}')
    directory = cache/(repo.replace('/','--')+'-'+commit)
    git = shutil.which('git')
    if not git:raise RuntimeError('Git is required to fetch upstream sources. Install Git and rerun.')
    url = 'https://github.com/'+repo+'.git'
    if directory.exists():
        if not (directory/'.git').is_dir():raise RuntimeError(f'Unmanaged source cache: {directory}')
        actual = subprocess.check_output([git,'-C',str(directory),'remote','get-url','origin'],text=True).strip()
        if actual != url:raise RuntimeError(f'Source cache identity mismatch: {directory}')
    else:
        directory.mkdir(parents=True)
        run([git,'init','--quiet',directory])
        run([git,'-C',directory,'remote','add','origin',url])
    run([git,'-C',directory,'config','core.longpaths','true'])
    run([git,'-C',directory,'config','core.autocrlf','false'])
    run([git,'-C',directory,'config','remote.origin.promisor','true'])
    run([git,'-C',directory,'config','remote.origin.partialclonefilter','blob:none'])
    have = subprocess.run([git,'-C',str(directory),'cat-file','-e',commit+'^{commit}'],capture_output=True).returncode == 0
    if not have:run([git,'-C',directory,'fetch','--quiet','--depth=1','--filter=blob:none','origin',commit])
    run([git,'-C',directory,'config','core.sparseCheckout','true'])
    patterns=[]
    for path in sorted(paths):
        contained(directory,path)
        patterns.append('/'+re.sub(r'([\\*?\[\]!])',r'\\\1',path))
    (directory/'.git/info/sparse-checkout').write_text('\n'.join(patterns)+'\n',encoding='utf-8')
    run([git,'-C',directory,'-c','advice.detachedHead=false','checkout','--quiet','--detach',commit])
    run([git,'-C',directory,'read-tree','-mu','HEAD'])
    return directory


def write_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp = path.with_name(path.name+'.tmp')
    temp.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    temp.replace(path)


def link_or_copy(src,dst):
    try:os.link(src,dst)
    except OSError:shutil.copy2(src,dst)
    return dst


def antigravity_entrypoints(plugin):
    """Keep full guides readable despite Antigravity's 24,000-byte skill-body limit."""
    adapted=[]
    for entry in plugin.glob('skills/*/SKILL.md'):
        content=entry.read_text(encoding='utf-8')
        end=content.find('\n---\n',4)
        if end < 0:raise ValueError('Missing skill frontmatter delimiter: '+str(entry))
        body=content[end+5:]
        if len(body.encode('utf-8')) <= 24000:continue
        guide=entry.with_name('ATLAS-FULL-GUIDE.md')
        if guide.exists():raise FileExistsError('Companion guide already exists: '+str(guide))
        guide.write_text(content,encoding='utf-8')
        wrapper=content[:end+5]+'\n# '+entry.parent.name+'\n\nBefore applying this skill, read the [complete skill guide](ATLAS-FULL-GUIDE.md) in this directory. Its workflow, references, constraints and verification steps are part of this skill. Read the whole companion guide in chunks if needed, then follow it using the tools actually available in this host. Resolve relative paths from this skill directory.\n\nThe companion preserves the full source instructions because Antigravity truncates skill bodies above 24,000 bytes. This entrypoint retains the original trigger metadata.\n'
        temp=entry.with_name('SKILL.md.tmp')
        temp.write_text(wrapper,encoding='utf-8');temp.replace(entry)
        adapted.append(entry.parent.name)
    return adapted


def build(selection, cache):
    catalog = json.loads((ROOT/'catalog/atlas.lock.json').read_text(encoding='utf-8'))
    groups = [value for name,value in STUDIOS.items() if selection == 'all' or name == selection]
    names = {g[0] for g in groups}
    files = [f for f in catalog['files'] if f['studio'] in names]
    needed={}
    for item in files:
        if 'source' in item:needed.setdefault(item['source'],set()).add(item['source_path'])
    cache.mkdir(parents=True,exist_ok=True)
    sources={};opened=[]
    try:
        for key,paths in sorted(needed.items()):
            record=catalog['sources'][key]
            archive=cache/(record['repository'].replace('/','--')+'-'+record['commit']+'.zip')
            print('Preparing '+record['repository'],flush=True)
            if archive.exists():
                if digest(archive.read_bytes()) != record['sha256']:raise ValueError(f'Archive checksum mismatch: {archive}')
                z=zipfile.ZipFile(archive);opened.append(z)
                members={m.split('/',1)[-1]:m for m in z.namelist() if '/' in m}
                sources[key]=(z,members)
            else:sources[key]=source_tree(key,record,paths,cache)
        output=ROOT/'dist'
        output.mkdir(exist_ok=True)
        # Build in a fresh directory; never clear or overwrite an existing package tree.
        stage=Path(tempfile.mkdtemp(prefix='atlas-build-',dir=output))
        portable=stage/'codex/plugins'
        for item in files:
            target=contained(portable/item['studio'],item['path'])
            target.parent.mkdir(parents=True,exist_ok=True)
            if 'local' in item:data=contained(ROOT,item['local']).read_bytes()
            else:
                src=sources[item['source']]
                if isinstance(src,tuple):data=src[0].read(src[1][item['source_path']])
                else:
                    data=contained(src,item['source_path']).read_bytes()
                    if digest(data) != item['upstream_sha256']:
                        # Git attributes may transform checkout line endings; verify the committed bytes.
                        commit=catalog['sources'][item['source']]['commit']
                        data=subprocess.check_output([shutil.which('git'),'-C',str(src),'show',commit+':'+item['source_path']])
                if digest(data) != item['upstream_sha256']:raise ValueError('Upstream checksum mismatch: '+item['path'])
                if 'patch' in item:data=patched(data,json.loads(contained(ROOT,item['patch']).read_text(encoding='utf-8')))
            if digest(data) != item['sha256']:raise ValueError('Output checksum mismatch: '+item['path'])
            target.write_bytes(data)
        for name,title,count in groups:
            plugin=portable/name
            metadata=json.loads((ROOT/'templates'/name/'plugin.json').read_text(encoding='utf-8'))
            write_json(plugin/'plugin.json',metadata)
            write_json(plugin/'.codex-plugin/plugin.json',dict(name=name,version=VERSION,description=metadata['description'],skills='./skills',interface=metadata['extensions']['com.openai']['interface']))
            shutil.copy2(ROOT/'templates'/name/'README.md',plugin/'README.md')
            shutil.copy2(ROOT/'docs/RUNTIME.md',plugin/'ATLAS-RUNTIME.md')
            actual={p.parent.name for p in plugin.glob('skills/*/SKILL.md')}
            expected={s['name'] for s in catalog['skills'] if s['studio']==name}
            if actual != expected or len(actual)!=count:raise ValueError('Skill registration mismatch: '+name)
            for p in plugin.rglob('*'):
                if p.is_file():p.chmod(p.stat().st_mode | 0o100) if p.suffix in {'.sh','.py'} or p.name=='impeccable' else None
            for host in ['claude','antigravity']:
                dest=stage/host/'plugins'/name
                shutil.copytree(plugin,dest,copy_function=link_or_copy)
                if host=='claude':
                    write_json(dest/'.claude-plugin/plugin.json',dict(name=name,version=VERSION,description=metadata['description'],author=dict(name='bangaji313'),homepage='https://github.com/bangaji313/atlas-skill-studio',repository='https://github.com/bangaji313/atlas-skill-studio',keywords=['agent-skills','atlas-studio'],skills='./skills'))
                else:
                    write_json(dest/'plugin.json',dict(name=name,displayName=title,version=VERSION,description=metadata['description'],logo='assets/logo.png'))
                    adapted=antigravity_entrypoints(dest)
                    write_json(dest/'ATLAS-HOST-ADAPTATIONS.json',dict(host='Antigravity',body_limit_bytes=24000,companion_guides=adapted))
                archive=stage/(name+'-'+host+'-'+VERSION+'.zip')
                with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,strict_timestamps=False) as z:
                    for p in sorted(dest.rglob('*')):
                        if p.is_file():z.write(p,p.relative_to(dest).as_posix())
        write_json(stage/'claude/.claude-plugin/marketplace.json',dict(name='atlas-studio',owner=dict(name='bangaji313'),plugins=[dict(name=n,source='./plugins/'+n,description=t) for n,t,_ in groups]))
        write_json(stage/'codex/.agents/plugins/marketplace.json',dict(name='atlas-studio',interface=dict(displayName='Atlas Skill Studio'),plugins=[dict(name=n,source=dict(source='local',path='./plugins/'+n),policy=dict(installation='AVAILABLE',authentication='ON_USE')) for n,_,_ in groups]))
        receipt=dict(version=VERSION,directory=str(stage.resolve()),studios={n:c for n,_,c in groups},files_verified=len(files))
        write_json(output/'latest-build.json',receipt)
        print(json.dumps(receipt,indent=2),flush=True)
        return stage,groups
    finally:
        for z in opened:z.close()


def install(host,stage,groups):
    if host=='antigravity':
        # This is the documented Antigravity App/Desktop global location, not the IDE's workspace.
        parent=Path.home()/'.gemini/config/plugins'
        parent.mkdir(parents=True,exist_ok=True)
        for name,_,_ in groups:
            target=parent/name
            if target.exists():raise FileExistsError(f'{target} already exists. Uninstall it in Antigravity before installing this distribution.')
        for name,_,_ in groups:shutil.copytree(stage/'antigravity/plugins'/name,parent/name)
        print('Antigravity App: restart, then open Customizations > Installed to inspect and enable Atlas.')
    else:
        binary=shutil.which(host)
        if not binary:raise RuntimeError(f'{host} CLI not found. Packages were built successfully at {stage}.')
        run([binary,'plugin','marketplace','add',stage/host])
        action='install' if host=='claude' else 'add'
        for name,_,_ in groups:run([binary,'plugin',action,name+'@atlas-studio'])
        run([binary,'plugin','list'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    for command in ['build','install']:
        p=sub.add_parser(command)
        if command=='install':p.add_argument('host',choices=['antigravity','claude','codex'])
        p.add_argument('--studio',choices=['all',*STUDIOS],default='all')
        p.add_argument('--cache-dir',type=Path,default=ROOT/'.atlas-cache')
    sub.add_parser('list')
    args=parser.parse_args()
    if args.command=='list':
        for _,(name,title,count) in STUDIOS.items():print(f'{title}: {count} skills ({name})')
        return
    stage,groups=build(args.studio,args.cache_dir.resolve())
    if args.command=='install':install(args.host,stage,groups)


if __name__=='__main__':
    try:main()
    except (OSError,ValueError,KeyError,RuntimeError,subprocess.CalledProcessError) as exc:
        print('Atlas stopped: '+str(exc),file=sys.stderr)
        sys.exit(1)
