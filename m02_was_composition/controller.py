"""Fail-closed Phase 3B controller source. Execution requires Phase 3B-2."""
from __future__ import annotations
import hashlib, json, os, signal, subprocess, threading, time
from pathlib import Path

SOGA=Path(__file__).resolve().parent.parent
WAS=Path('/private/tmp/m02-stage3lib-20260910/was-teaching-server')
HEAD='2090a606f2723e4d57ef0090db55fd1bdab9427e'; TREE='540d85cea6cc7ab50ee6f00b0dead2084c1d65de'
NODE='/opt/homebrew/Cellar/node/26.7.0/bin/node'; PYTHON='/usr/bin/python3'
MANIFEST_SHA='7f5355e94db8c9d5ec87fa249150d15eb99640fd150c9ebeed75a3bed86cf586'
CONTROLLER_STAGES={'preflight:soga_head','preflight:was_identity','preflight:runtime','preflight:manifest','preflight:manifest_count','preflight:candidate','preflight:git','preflight:lsof','preflight:python3','preflight:node','observation:lsof_control','observation:worker_socket','observation:worker_not_live','observation:worker_died','observation:worker_survived','observation:listener_changed','execution:child_spawn'}

def _safe_controller_stage(error):
    # Compare the full message only to fixed literals; never emit arbitrary text.
    message=str(error)
    return message if message in CONTROLLER_STAGES else 'unknown'

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

def _focused_execution(diagnostic=False)->tuple[int,bytes,bytes]:
    command=[PYTHON,'-m','m02_was_composition.diagnostic_tests'] if diagnostic else [PYTHON,'-m','unittest','tests.test_m02_was_composition','-v']
    try:
        process=subprocess.Popen(command,cwd=SOGA,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False,start_new_session=True,env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','LANG':'C','LC_ALL':'C','M02_STAGE3B_EXECUTE':'1'})
    except OSError as error:
        raise RuntimeError('execution:child_spawn') from error
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

def _diagnostic_document(raw, status):
    from .diagnostic_tests import ERROR_CLASSES, OUTCOMES, STAGES, allowed_test_identifiers
    if len(raw)>16384: raise RuntimeError('diagnostic:output_limit')
    value=json.loads(raw)
    if not isinstance(value,dict) or set(value)!={'schema','tests_run','counts','records','truncated','exit_status'}: raise RuntimeError('diagnostic:schema')
    if value['schema']!=1 or type(value['truncated']) is not bool or type(value['tests_run']) is not int or not 0<=value['tests_run']<=128: raise RuntimeError('diagnostic:schema')
    if type(value['exit_status']) is not int or value['exit_status'] not in (0,1) or value['exit_status']!=status: raise RuntimeError('diagnostic:status')
    counts=value['counts']
    if not isinstance(counts,dict) or set(counts)!={'failure','error','skip'} or any(type(x) is not int or not 0<=x<=128 for x in counts.values()): raise RuntimeError('diagnostic:counts')
    records=value['records']
    if not isinstance(records,list) or len(records)>128: raise RuntimeError('diagnostic:records')
    allowed=allowed_test_identifiers()
    for item in records:
        if not isinstance(item,dict) or set(item)!={'test','outcome','error_class','stage'}: raise RuntimeError('diagnostic:records')
        if not isinstance(item['test'],str) or item['test'] not in allowed: raise RuntimeError('diagnostic:test')
        if item['outcome'] not in OUTCOMES or item['error_class'] not in ERROR_CLASSES|{'none','unknown'} or item['stage'] not in STAGES|{'unknown'}: raise RuntimeError('diagnostic:records')
    if (value['truncated'] or counts['failure'] or counts['error']) and status==0: raise RuntimeError('diagnostic:status')
    return value

def _atomic_record(root, value):
    raw=json.dumps(value,sort_keys=True,separators=(',',':')).encode('ascii')
    if len(raw)>24576: raise RuntimeError('diagnostic:record_limit')
    temporary=root/'record.tmp';target=root/'record.json'
    descriptor=os.open(str(temporary),os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try:
        with os.fdopen(descriptor,'wb') as output:
            output.write(raw);output.flush();os.fsync(output.fileno())
        os.replace(temporary,target)
    finally:
        if temporary.exists():temporary.unlink()
    return hashlib.sha256(raw).hexdigest()

def run_diagnostic_once(*,expected_soga_head:str,evidence_root:Path)->dict:
    """No runtime authority is conveyed by this entry point."""
    root=evidence_root.resolve(strict=True)
    if evidence_root.is_symlink() or root.parent!=Path('/private/tmp') or not root.name.startswith('m02-stage3b-diagnostics-') or list(root.iterdir()): raise RuntimeError('diagnostic:evidence_root')
    started=time.monotonic();status=126;out=b'';err=b'';report=None;execution='not_started';postflight='not_started';controller_stage='none';before=None;listeners=None
    try:
        preflight(expected_soga_head=expected_soga_head);before=snapshot();listeners=listener_snapshot()
        status,out,err=_focused_execution(diagnostic=True)
        execution='timeout' if status==124 else 'output_limit' if status==125 else 'focused_tests' if status else 'success'
        try:report=_diagnostic_document(out,status)
        except (ValueError,TypeError,KeyError,RuntimeError):execution='invalid_diagnostic'
    except Exception as error:
        execution='controller_error';controller_stage=_safe_controller_stage(error)
    finally:
        if before is not None and listeners is not None:
            try:
                after=snapshot();current=listener_snapshot()
                leftovers=list(Path('/private/tmp').glob('m02-stage3b-run-*'))+list(Path('/private/tmp').glob('m02-stage3b-fake-*'))+list(Path('/private/tmp').glob('m02-was-composition-modules-*'))
                postflight='state_changed' if before!=after or listeners!=current else 'temporary_paths' if leftovers else 'success'
            except Exception:postflight='inspection_error'
    value={'schema':1,'expected_target':expected_soga_head,'execution':execution,'controller_stage':controller_stage,'subprocess_status':status,'diagnostic':report,'postflight':postflight,'stdout_s256':hashlib.sha256(out).hexdigest(),'stderr_s256':hashlib.sha256(err).hexdigest(),'elapsed_ms':int((time.monotonic()-started)*1000)}
    digest=_atomic_record(root,value)
    return {'ok':execution=='success' and postflight=='success','execution':execution,'postflight':postflight,'record_s256':digest}
