"""Fail-closed Phase 3B controller source. Execution requires Phase 3B-2."""
from __future__ import annotations
import hashlib, os, signal, subprocess, threading, time
from pathlib import Path

SOGA=Path(__file__).resolve().parent.parent
WAS=Path('/private/tmp/m02-stage3lib-20260910/was-teaching-server')
HEAD='2090a606f2723e4d57ef0090db55fd1bdab9427e'; TREE='540d85cea6cc7ab50ee6f00b0dead2084c1d65de'
NODE='/opt/homebrew/Cellar/node/26.7.0/bin/node'; PYTHON='/usr/bin/python3'
MANIFEST_SHA='7f5355e94db8c9d5ec87fa249150d15eb99640fd150c9ebeed75a3bed86cf586'

def _run(args,cwd=None,timeout=10,allow_empty_failure=False,extra_env=None):
    environment={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','LANG':'C','LC_ALL':'C','GIT_OPTIONAL_LOCKS':'0'}
    environment.update(extra_env or {})
    result=subprocess.run(args,cwd=cwd,shell=False,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout,check=False,env=environment)
    if allow_empty_failure and result.returncode==1 and not result.stdout: return ''
    if result.returncode: raise RuntimeError(f'preflight:{Path(args[0]).name}')
    return result.stdout.decode('utf-8','strict').strip()

def _manifest()->str:
    rows=[]
    for file in sorted((WAS/'dist').rglob('*')):
        if file.is_file(): rows.append(f'{hashlib.sha256(file.read_bytes()).hexdigest()}  {file.relative_to(WAS)}\n')
    if len(rows)!=298: raise RuntimeError('preflight:manifest_count')
    return hashlib.sha256(''.join(rows).encode()).hexdigest()

def snapshot()->dict:
    return {'soga':_run(['/usr/bin/git','status','--porcelain'],SOGA),'was':_run(['/usr/bin/git','status','--porcelain','--untracked-files=no'],WAS),'manifest':_manifest()}

def preflight(*,expected_soga_head:str):
    if len(expected_soga_head)!=40 or _run(['/usr/bin/git','rev-parse','HEAD'],SOGA)!=expected_soga_head: raise RuntimeError('preflight:soga_head')
    if _run(['/usr/bin/git','rev-parse','HEAD'],WAS)!=HEAD or _run(['/usr/bin/git','rev-parse','HEAD^{tree}'],WAS)!=TREE: raise RuntimeError('preflight:was_identity')
    if _run([PYTHON,'--version'])!='Python 3.9.6' or _run([NODE,'--version'])!='v26.7.0': raise RuntimeError('preflight:runtime')
    if _manifest()!=MANIFEST_SHA: raise RuntimeError('preflight:manifest')
    if not (WAS/'dist/index.js').is_file() or snapshot()['was']: raise RuntimeError('preflight:candidate')

def listener_snapshot()->str:
    # Unprivileged user-visible TCP inventory; not a whole-host proof.
    if not _run(['/usr/sbin/lsof','-nP','-p',str(os.getpid())]): raise RuntimeError('observation:lsof_control')
    return _run(['/usr/sbin/lsof','-nP','-a','-u',str(os.getuid()),'-iTCP','-sTCP:LISTEN'],timeout=10,allow_empty_failure=True)

def observe_process(process:subprocess.Popen,baseline:str|None=None):
    if baseline is not None:
        if process.poll() is None: raise RuntimeError('observation:worker_survived')
        if listener_snapshot()!=baseline: raise RuntimeError('observation:listener_changed')
        return None
    if process.poll() is not None: raise RuntimeError('observation:worker_not_live')
    control=_run(['/usr/sbin/lsof','-nP','-p',str(os.getpid())])
    if not control: raise RuntimeError('observation:lsof_control')
    sockets=_run(['/usr/sbin/lsof','-nP','-a','-p',str(process.pid),'-i'],allow_empty_failure=True)
    if sockets: raise RuntimeError('observation:worker_socket')
    if process.poll() is not None: raise RuntimeError('observation:worker_died')
    return listener_snapshot()

def _focused_execution()->tuple[int,bytes,bytes]:
    process=subprocess.Popen([PYTHON,'-m','unittest','tests.test_m02_was_composition','-v'],cwd=SOGA,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False,start_new_session=True,env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','LANG':'C','LC_ALL':'C','M02_STAGE3B_EXECUTE':'1'})
    out=bytearray();err=bytearray();overflow=[False]
    def drain(stream,target):
        while True:
            chunk=stream.read(4096)
            if not chunk:return
            if len(target)+len(chunk)>65536:overflow[0]=True;os.killpg(process.pid,signal.SIGTERM);return
            target.extend(chunk)
    threads=[threading.Thread(target=drain,args=(process.stdout,out),daemon=True),threading.Thread(target=drain,args=(process.stderr,err),daemon=True)]
    for thread in threads:thread.start()
    try: process.wait(timeout=180)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid,signal.SIGTERM)
        try:process.wait(timeout=1)
        except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait(timeout=1)
        for thread in threads:thread.join(1)
        return 124,bytes(out),bytes(err)
    try:os.killpg(process.pid,signal.SIGTERM)
    except ProcessLookupError:pass
    for thread in threads:thread.join(1)
    if any(thread.is_alive() for thread in threads):return 125,bytes(out),bytes(err)
    if overflow[0]:return 125,bytes(out),bytes(err)
    return process.returncode,bytes(out),bytes(err)

def run_once(*,expected_soga_head:str)->dict:
    preflight(expected_soga_head=expected_soga_head);before=snapshot();listeners=listener_snapshot();started=time.monotonic();status=126;out=b'';err=b'';post_error=None
    try:status,out,err=_focused_execution()
    finally:
        try:
            after=snapshot();after_listeners=listener_snapshot()
            leftovers=list(Path('/private/tmp').glob('m02-stage3b-run-*'))+list(Path('/private/tmp').glob('m02-stage3b-fake-*'))+list(Path('/private/tmp').glob('m02-was-composition-modules-*'))
            if before!=after or listeners!=after_listeners:raise RuntimeError('postflight:state_changed')
            if leftovers:raise RuntimeError('postflight:temporary_paths')
        except BaseException as exc:post_error=exc
    if post_error is not None:raise post_error
    if status==124:raise RuntimeError('execution:overall_timeout')
    if status==125:raise RuntimeError('execution:output_limit')
    if status:raise RuntimeError('execution:focused_tests')
    return {'ok':True,'focused_stdout_s256':hashlib.sha256(out).hexdigest(),'focused_stderr_s256':hashlib.sha256(err).hexdigest(),'elapsed_ms':int((time.monotonic()-started)*1000),'manifest':after['manifest']}
