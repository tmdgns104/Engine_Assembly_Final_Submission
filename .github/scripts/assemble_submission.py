#!/usr/bin/env python3
"""One-shot, pinned snapshot import. Does not execute imported project code."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from urllib.parse import unquote, urlsplit
import zipfile

TARGET = 'tmdgns104/Engine_Assembly_Final_Submission'
SOURCES = [
    dict(folder='project', repository='tmdgns104/Engine_Assembly_Defect_Inspector', branch='master',
         commit='bdadacc51c6c9b03d67a57ed7bbe10366a06cc4c', tree='37b3f515b58b0d87fc4217cdd0287a90784eed2e'),
    dict(folder='docs', repository='tmdgns104/Engine_Assembly_Runtime_Review', branch='main',
         commit='fa9774e1e08f83b6f287c27f018cee78f7febe5f', tree='fb599ee2524914c042e3885041e4eacdf377f6ea'),
]
LINK = re.compile(r'(!?\[[^\]\n]*\]\()([^\s)]+)(\))')
LFS = re.compile(rb'^version https://git-lfs.github.com/spec/v1\noid sha256:([0-9a-f]{64})\nsize ([0-9]+)\n?$')

def run(*args, cwd=None, text=True):
    p = subprocess.run(list(args), cwd=cwd, check=True, stdout=subprocess.PIPE,
                       text=text, encoding='utf-8' if text else None)
    return p.stdout.strip() if text else p.stdout

def git(*args, cwd=None, text=True):
    return run('git', *args, cwd=cwd, text=text)

def dump(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def payload(path):
    return os.fsencode(os.readlink(path)) if path.is_symlink() else path.read_bytes()

def digest(path):
    return hashlib.sha256(payload(path)).hexdigest()

def blob_digest(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def tree_entries(ref):
    result=[]
    for item in git('ls-tree','-r','-l','-z',ref,text=False).split(b'\0'):
        if not item: continue
        head,name=item.split(b'\t',1)
        mode,kind,oid,size=head.decode().split()
        name=name.decode('utf-8')
        assert kind=='blob' and mode in ('100644','100755','120000'), ('unsupported_entry',name,mode)
        assert not PurePosixPath(name).is_absolute() and '..' not in PurePosixPath(name).parts
        result.append(dict(path=name,mode=mode,oid=oid,git_size=int(size)))
    return result

def relocate_url(url, prefix, refs):
    """Relocate current navigation only; historical commit links remain intact."""
    for source in refs:
        base='https://github.com/'+source['repository']
        destination=source['folder']
        if url.rstrip('/')==base:
            return os.path.relpath(destination,prefix).replace(os.sep,'/')+'/'
        for branch in (source['branch'],source['commit']):
            for kind in ('blob','tree'):
                start=f'{base}/{kind}/{branch}/'
                if url.startswith(start):
                    return os.path.relpath(destination,prefix).replace(os.sep,'/')+'/'+url[len(start):]
            for start in (f'{base}/raw/{branch}/',f'{base}/raw/refs/heads/{branch}/'):
                if url.startswith(start):
                    return f'https://github.com/{TARGET}/raw/refs/heads/main/{destination}/'+url[len(start):]
    return url

def rewrite_readme(text,folder):
    # Also handles reference-style Markdown definitions without touching other prose.
    url_pattern=re.compile(r'https://github\.com/tmdgns104/(?:Engine_Assembly_Defect_Inspector|Engine_Assembly_Runtime_Review)(?:/[^\s)<>\]\"\']*)?')
    changed=url_pattern.sub(lambda m: relocate_url(m.group(0),folder,SOURCES),text)
    return '> **통합 제출본:** [전체 안내](../README.md) · [실행·학습 코드](../project/) · [보고서·증빙](../docs/)\n> 아래 본문은 원본 설명을 보존하고 현재 자료로 이동하는 링크만 새 위치에 맞췄습니다. 과거 커밋 링크는 출처로 유지합니다.\n\n'+changed

def check_links(path,root):
    text=path.read_text(encoding='utf-8')
    destinations=[m.group(2) for m in LINK.finditer(text)]
    destinations += re.findall(r'^\[[^\]\n]+\]:\s*(\S+)',text,re.M)
    checked=[]; missing=[]
    for url in destinations:
        parts=urlsplit(url)
        if parts.scheme or parts.netloc or not parts.path: continue
        target=(path.parent/unquote(parts.path)).resolve()
        if not target.is_relative_to(root.resolve()) or not target.exists(): missing.append(url)
        else: checked.append(url)
    return dict(file=str(path.relative_to(root)),checked=len(checked),missing=missing)

def public_clone(url,path):
    # No token is supplied: public evaluation access is checked independently.
    git('-c','credential.helper=','clone','--depth','1',url,str(path))
    git('lfs','pull','origin','main',cwd=path)
    git('lfs','fsck',cwd=path)

def verify_manifest(root,rows):
    for row in rows:
        path=root/row['destination_path']; assert path.exists() or path.is_symlink(), str(path)
        assert digest(path)==row['final_sha256'], ('content_mismatch',str(path))
        assert len(payload(path))==row['size_bytes'], ('size_mismatch',str(path))
        actual='120000' if path.is_symlink() else '100755' if path.stat().st_mode & 0o111 else '100644'
        assert actual==row['mode'], ('mode_mismatch',str(path),actual,row['mode'])
    for folder in ('project','docs'):
        expected={row['destination_path'] for row in rows if row['destination_path'].startswith(folder+'/')}
        actual={str(p.relative_to(root)) for p in (root/folder).rglob('*') if p.is_file() or p.is_symlink()}
        assert actual==expected, (folder,'file_set_mismatch',sorted(actual^expected))

def make_readme(root,docs_original,sources):
    rows=[]
    for line in docs_original.splitlines():
        if re.match(r'^\|\s*\d{2}\s*\|',line):
            rows.append(LINK.sub(lambda m:m.group(1)+'docs/'+m.group(2)+m.group(3),line))
    assert len(rows)==11, ('unexpected_document_index',len(rows))
    content='''# On-Device AI 엔진 모형 조립 검사 시스템 — 최종 제출\n\n카메라·센서 입력, Jetson AI 검사, 원본·판정 저장, PLC와 LED·컨베이어 연계를 구현한 프로젝트의 **실행 코드와 평가 문서를 한 저장소에 모았습니다.**\n\n**검토 시작:** [최종 결과보고서 v1.2](docs/10_final_report_v1_2.pdf) · [프로젝트 상세](project/README.md) · [전체 문서·증빙](docs/README.md)\n\n## 폴더 안내\n\n| 폴더 | 포함 내용 |\n|---|---|\n| [project/](project/) | 기존 코드 저장소의 전체 추적 파일: 실행·학습 코드, 모델·설정, 설치 안내, 내부 개발 문서 |\n| [docs/](docs/) | 기존 문서 저장소의 전체 추적 파일: 제출 보고서, 편집본, 원본 증빙 ZIP, DB 검토 자료 |\n\n두 폴더는 서브모듈이나 외부 저장소 바로가기가 아닌 **실제 파일 폴더**입니다. `project/docs/`는 프로젝트 내부 문서이며 루트의 `docs/`와 구분합니다.\n\n## 평가 문서 바로가기\n\n원본 문서 저장소의 최신 목록을 그대로 연결했습니다. PDF·DOCX·원본 ZIP의 내용을 수정하지 않았습니다.\n\n| ID | 최신 문서 | 버전 | 크기 | 편집·표시본 |\n|---|---|---|---|---|\n'''+ '\n'.join(rows)+'''\n\n## 원본 증빙과 DB\n\n| 자료 | 링크 |\n|---|---|\n| 전체 학습·검증 사진과 라벨 | [M1_M2_dataset_evidence_v002.zip](docs/M1_M2_dataset_evidence_v002.zip) |\n| 모델 학습·평가 원본 | [M1_M2_model_evaluation_evidence_v001.zip](docs/M1_M2_model_evaluation_evidence_v001.zip) |\n| 최적화 비교 원본 | [M1_M2_benchmark_evidence_v001.zip](docs/M1_M2_benchmark_evidence_v001.zip) |\n| 실제 통합시험 원본 | [Engine_Integrated_Test_Evidence_v001.zip](docs/Engine_Integrated_Test_Evidence_v001.zip) |\n| DB·SQL·조회 검토 | [DB 검토 자료](docs/review_kit/README_KO.md) |\n| 평가 근거 위치 | [EVIDENCE_INDEX.md](docs/EVIDENCE_INDEX.md) |\n| 문서 버전 대응 | [DOCUMENT_VERSION_MAP.md](docs/DOCUMENT_VERSION_MAP.md) |\n\n## 내려받기와 실행 위치\n\n전체 데이터셋 ZIP은 Git LFS 파일입니다. 실제 파일까지 내려받으려면 Git LFS가 설치된 환경에서 다음을 사용합니다.\n\n```bash\ngit lfs install\ngit clone https://github.com/tmdgns104/Engine_Assembly_Final_Submission.git\ncd Engine_Assembly_Final_Submission\ngit lfs pull\ncd project\n```\n\n기존 실행 안내의 프로젝트 루트는 이제 **`project/`**입니다. 위 `cd project` 이후 해당 환경에 맞는 설치·실행 안내를 따르세요.\n\n- [Jetson 운영본 설치 안내](project/jetson/INSTALL_OPERATING_KO.md)\n- [학습 코드와 자료 안내](project/notebook/training/README_KO.md)\n- [데이터셋 ZIP 실파일 다운로드](https://github.com/tmdgns104/Engine_Assembly_Final_Submission/raw/refs/heads/main/docs/M1_M2_dataset_evidence_v002.zip)\n\nGitHub의 `Code → Download ZIP`에 LFS 실파일까지 포함되는지는 이 작업에서 검증하지 않았습니다. 전체 파일 확보에는 위 Git LFS 방식 또는 개별 실파일 다운로드를 사용하세요.\n\n## 출처와 검증\n\n이 저장소는 아래 두 커밋의 스냅샷입니다. 원본 저장소와 운영 장치는 변경하지 않았으며, 원본의 후속 변경이 자동 동기화되지는 않습니다.\n\n| 폴더 | 원본 저장소 | 고정 커밋 |\n|---|---|---|\n'''
    for source in sources:
        content+=f"| {source['folder']}/ | [{source['repository']}](https://github.com/{source['repository']}) | `{source['commit']}` |\n"
    content+='''\n[출처·수량](SOURCE_REVISIONS.json) · [파일별 보존·해시 목록](.submission/FILE_MANIFEST.json) · [이전 검증](.submission/MIGRATION_VERIFICATION.json)\n\n원본 README 두 개는 [.submission/original_readmes/](.submission/original_readmes/)에도 보존했습니다. 통합 폴더의 README는 안내 링크만 새 위치로 연결하며, 과거 근거 커밋·보고서 내부 링크는 원문 출처로 보존합니다.\n\n이번 작업은 파일 통합과 다운로드 검증입니다. 새로운 모델 학습·현장시험·Jetson 또는 PLC 배포를 수행한 것은 아닙니다. PPT·시연영상은 실제 파일 포함 여부를 별도로 확인해야 하며, 이 통합만으로 모든 제출 요건의 완료를 의미하지는 않습니다.\n'''
    (root/'README.md').write_text(content,encoding='utf-8')

def main():
    root=Path.cwd().resolve()
    assert os.environ.get('GITHUB_REPOSITORY')==TARGET,'unexpected destination'
    assert git('remote','get-url','origin').rstrip('/') in (f'https://github.com/{TARGET}',f'https://github.com/{TARGET}.git')
    assert not git('status','--porcelain'), 'working tree is not clean'
    for name in ('project','docs','SOURCE_REVISIONS.json'):
        assert not (root/name).exists(), f'Already populated: {name}; refusing overwrite'
    starting_commit=git('rev-parse','HEAD')
    git('config','user.name','github-actions[bot]')
    git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    git('config','core.autocrlf','false')
    git('lfs','install','--local')
    rows=[]; sources=[]; source_entries={}; lfs_pointers={}
    for spec in SOURCES:
        source=dict(spec); name='source-'+source['folder']; url=f"https://github.com/{source['repository']}.git"
        git('remote','add',name,url)
        git('remote','set-url','--push',name,'disabled-source-write')
        git('fetch','--no-tags','--depth','1',name,source['commit'])
        assert git('rev-parse',source['commit']+'^{tree}')==source['tree']
        entries=tree_entries(source['commit']); source_entries[source['folder']]=entries
        for entry in entries:
            if entry['git_size']<1024:
                data=git('cat-file','blob',entry['oid'],text=False); match=LFS.fullmatch(data)
                if match:lfs_pointers[source['folder']+'/'+entry['path']]=dict(oid=match[1].decode(),size=int(match[2]))
            if entry['git_size']>=100*1024*1024:raise RuntimeError('oversized ordinary Git blob')
        git('read-tree','--prefix='+source['folder']+'/','-u',source['commit'])
        source.update(url=url,tracked_files=len(entries))
        sources.append(source)
        print('Imported tree',source['folder'],len(entries),flush=True)
    git('commit','-m','import: preserve pinned project and docs snapshots in real folders')
    for source in sources:
        if any(p.startswith(source['folder']+'/') for p in lfs_pointers):
            git('lfs','fetch','--include=','--exclude=','source-'+source['folder'],source['commit'])
    git('lfs','checkout')
    for source in sources:
        for entry in source_entries[source['folder']]:
            destination=source['folder']+'/'+entry['path']; path=root/destination; data=payload(path)
            pointer=lfs_pointers.get(destination)
            if pointer:
                assert len(data)==pointer['size'] and hashlib.sha256(data).hexdigest()==pointer['oid'],('LFS materialization',destination)
            else:assert blob_digest(data)==entry['oid'],('source bytes',destination)
            rows.append(dict(destination_path=destination,source_path=entry['path'],source_repository=source['repository'],
                             source_commit=source['commit'],source_git_blob=entry['oid'],mode=entry['mode'],
                             source_sha256=hashlib.sha256(data).hexdigest(),final_sha256=hashlib.sha256(data).hexdigest(),
                             size_bytes=len(data),lfs=pointer))
        source['materialized_bytes']=sum(r['size_bytes'] for r in rows if r['destination_path'].startswith(source['folder']+'/'))
        source['lfs_files']=sum(p.startswith(source['folder']+'/') for p in lfs_pointers)
    original_dir=root/'.submission/original_readmes'; original_dir.mkdir(parents=True)
    readmes={folder:(root/folder/'README.md').read_text(encoding='utf-8') for folder in ('project','docs')}
    for folder in readmes:
        path=root/folder/'README.md'; (original_dir/(folder+'_README.md')).write_bytes(path.read_bytes())
        path.write_text(rewrite_readme(readmes[folder],folder),encoding='utf-8')
        row=next(r for r in rows if r['destination_path']==folder+'/README.md')
        row.update(final_sha256=digest(path),size_bytes=path.stat().st_size,
                   change='Navigation-only README integration; original bytes saved separately')
    (root/'.gitattributes').write_text('* -text\n',encoding='utf-8')
    dump(root/'SOURCE_REVISIONS.json',dict(schema_version=1,created_at=datetime.now(timezone.utc).isoformat(),
        mode='PINNED_SNAPSHOTS_NOT_AUTOMATIC_SYNC',target=TARGET,sources=sources))
    dump(root/'.submission/FILE_MANIFEST.json',dict(schema_version=1,files=rows))
    report_path=root/'.submission/MIGRATION_VERIFICATION.json'
    report=dict(status='LOCAL_VERIFIED_REMOTE_PENDING',scope='Packaging and file integrity, not runtime or field acceptance',
        source_files=len(rows),lfs_files=lfs_pointers,source_repositories_written=False,source_readmes_modified_only=True,
        starting_target_commit=starting_commit,workflow_run=os.environ.get('GITHUB_RUN_ID'))
    dump(report_path,report)
    make_readme(root,readmes['docs'],sources)
    verify_manifest(root,rows)
    checks=[check_links(root/p,root) for p in ('README.md','project/README.md','docs/README.md')]
    assert not checks[0]['missing'],checks[0]
    report['navigation_checks']=checks
    zip_results=[]
    for path in sorted((root/'docs').glob('*.zip')):
        with zipfile.ZipFile(path) as z:
            bad=z.testzip(); assert bad is None,(str(path),bad)
            zip_results.append(dict(path=str(path.relative_to(root)),bytes=path.stat().st_size,sha256=digest(path),members=len(z.infolist()),crc='PASS'))
    report['evidence_zip_checks']=zip_results
    dump(report_path,report)
    git('add','.gitattributes','README.md','SOURCE_REVISIONS.json','.submission','project/README.md','docs/README.md')
    git('commit','-m','docs: add evaluator navigation and snapshot integrity records')
    for source in sources:
        expected={e['path']:(e['mode'],e['oid']) for e in source_entries[source['folder']]}
        actual={e['path']:(e['mode'],e['oid']) for e in tree_entries('HEAD:'+source['folder'])}
        assert set(actual)==set(expected),(source['folder'],'staged path mismatch')
        assert all(actual[p]==value for p,value in expected.items() if p!='README.md'),(source['folder'],'staged blob changed')
    remote_head=git('ls-remote','origin','refs/heads/main').split()[0]
    assert remote_head==starting_commit,'Target advanced concurrently; no force push'
    git('lfs','push','origin','HEAD')
    git('push','origin','HEAD:refs/heads/main')
    published=git('rev-parse','HEAD')
    with tempfile.TemporaryDirectory(prefix='submission-public-verify-') as temporary:
        fresh=Path(temporary)/'fresh'
        public_clone(f'https://github.com/{TARGET}.git',fresh)
        assert git('rev-parse','HEAD',cwd=fresh)==published
        verify_manifest(fresh,rows)
        public_zip_checks=[]
        for row in rows:
            if row['lfs'] and row['destination_path'].endswith('.zip'):
                with zipfile.ZipFile(fresh/row['destination_path']) as z:
                    assert z.testzip() is None
                    public_zip_checks.append(dict(path=row['destination_path'],members=len(z.infolist()),crc='PASS'))
        root_links=check_links(fresh/'README.md',fresh);assert not root_links['missing']
    report.update(status='PASS',public_clone_verified=True,public_clone_content_commit=published,
                  all_materialized_file_hashes_and_modes='PASS',exact_source_file_sets='PASS',
                  source_git_blobs_except_navigation_readmes='PASS',lfs_fresh_download='PASS',
                  lfs_public_zip_checks=public_zip_checks,verified_at=datetime.now(timezone.utc).isoformat(),
                  limitations=['Source histories are linked by pinned commit, not merged.',
                               'Existing binary document hyperlinks and historical commit links are preserved.',
                               'GitHub Download ZIP inclusion of LFS payloads was not tested.',
                               'No application, model inference, camera or PLC was executed.'])
    dump(report_path,report)
    git('add','.submission/MIGRATION_VERIFICATION.json')
    git('commit','-m','verify: confirm anonymous clone and complete LFS payload integrity')
    git('push','origin','HEAD:refs/heads/main')
    print(json.dumps(dict(status='PASS',target='https://github.com/'+TARGET,head=git('rev-parse','HEAD'),
                          source_files=len(rows),sources=sources,lfs_files=lfs_pointers),ensure_ascii=False,indent=2),flush=True)
    summary=os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        Path(summary).write_text('# Submission import verified\n\n'+json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
    main()
