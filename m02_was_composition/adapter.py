"""Bounded socket-free Python adapter for Person Server/WAS composition."""
from __future__ import annotations
import hashlib, json, shutil, subprocess, tempfile, threading, time
from pathlib import Path
from typing import Any, Callable, Mapping

MAX_SAFE_INTEGER=9_007_199_254_740_991; MAX_ENVELOPE_BYTES=32_768; MAX_OUTPUT=65_536
MAX_INPUT=65_536
_INVOCATIONS=0; _INVOCATION_LOCK=threading.Lock()
EXPECTED_NODE=Path('/opt/homebrew/Cellar/node/26.7.0/bin/node')
RESULT_FIELDS={'request_id','subject','action','projection','status','mission_s256','authority_reference'}
ENVELOPE_FIELDS={'schema','version','correlation_id','issuer','subject','mission_s256','request_id','action','projection','status','result_s256','authority_reference_s256','interpretation'}
SECRET_KEYS=('token','secret','password','private_key','authorization','payment')
CANONICAL_FIXTURES=({'z':True,'a':1},{'v':'\b\f\n\r\t\x00\x1f\x7f'},{'min':-MAX_SAFE_INTEGER,'max':MAX_SAFE_INTEGER})

class CompositionError(RuntimeError):
    def __init__(self,stage:str,detail:str): super().__init__(f'{stage}:{detail}'); self.stage=stage

def _validate(value:Any,path='$'):
    if value is None or isinstance(value,bool): return
    if isinstance(value,int):
        if abs(value)>MAX_SAFE_INTEGER: raise CompositionError('canonicalization',f'unsafe integer {path}')
        return
    if isinstance(value,float): raise CompositionError('canonicalization',f'float {path}')
    if isinstance(value,str):
        if not value.isascii(): raise CompositionError('canonicalization',f'non-ASCII {path}')
        return
    if isinstance(value,list):
        for i,item in enumerate(value): _validate(item,f'{path}[{i}]')
        return
    if isinstance(value,dict):
        for key,item in value.items():
            if not isinstance(key,str) or not key.isascii(): raise CompositionError('canonicalization',f'key {path}')
            _validate(item,f'{path}.{key}')
        return
    raise CompositionError('canonicalization',f'type {path}')

def canonical_bytes(value:Mapping[str,Any])->bytes:
    _validate(value); return json.dumps(value,ensure_ascii=True,separators=(',',':'),sort_keys=True).encode()

def _text(value:Any,name:str)->str:
    if not isinstance(value,str) or not value or not value.isascii(): raise CompositionError('envelope_validation',name)
    return value

def _screen(value:Any,path='$'):
    if isinstance(value,dict):
        for key,item in value.items():
            if any(mark in key.lower() for mark in SECRET_KEYS): raise CompositionError('secret_screen',path)
            _screen(item,f'{path}.{key}')
    elif isinstance(value,list):
        for i,item in enumerate(value): _screen(item,f'{path}[{i}]')
    elif isinstance(value,str) and any(mark in value.lower() for mark in ('bearer ','begin private key','privatekeymultibase')):
        raise CompositionError('secret_screen',path)

def build_evidence_envelope(*,issuer:str,correlation_id:str,result:Mapping[str,Any],expected_subject:str|None=None,expected_mission:str|None=None,expected_request:str|None=None)->dict[str,Any]:
    issuer=_text(issuer,'issuer'); correlation_id=_text(correlation_id,'correlation_id')
    if set(result)-RESULT_FIELDS: raise CompositionError('envelope_validation','unsupported fields')
    _screen(result)
    subject=_text(result.get('subject'),'subject'); mission=_text(result.get('mission_s256'),'mission_s256'); request=_text(result.get('request_id'),'request_id')
    for actual,expected,name in ((subject,expected_subject,'subject'),(mission,expected_mission,'mission'),(request,expected_request,'request')):
        if expected is not None and actual!=expected: raise CompositionError('binding',name)
    authority=result.get('authority_reference')
    if authority is not None: authority=_text(authority,'authority_reference')
    envelope={'schema':'urn:soga:ps-was-evidence:v1','version':1,'correlation_id':correlation_id,'issuer':issuer,'subject':subject,'mission_s256':mission,'request_id':request,'action':_text(result.get('action'),'action'),'projection':_text(result.get('projection'),'projection'),'status':_text(result.get('status'),'status'),'result_s256':hashlib.sha256(canonical_bytes(result)).hexdigest(),'authority_reference_s256':hashlib.sha256(authority.encode()).hexdigest() if authority else None,'interpretation':'person_server_evidence_only'}
    if set(envelope)!=ENVELOPE_FIELDS or len(canonical_bytes(envelope))>MAX_ENVELOPE_BYTES: raise CompositionError('envelope_validation','schema or size')
    return envelope

def _drain(stream,target:bytearray,process:subprocess.Popen,overflow:list[bool]):
    while True:
        chunk=stream.read(4096)
        if not chunk:return
        if len(target)+len(chunk)>MAX_OUTPUT: overflow[0]=True; process.terminate(); return
        target.extend(chunk)

class CompositionAdapter:
    def __init__(self,*,worker:Path,timeout_seconds:int=10): self.node=EXPECTED_NODE; self.worker=worker.resolve(); self.timeout_seconds=timeout_seconds
    def store(self,*,envelope:Mapping[str,Any],package_root:Path,mode='store',second_envelope:Mapping[str,Any]|None=None,observer:Callable[...,Any]|None=None)->dict[str,Any]:
        global _INVOCATIONS
        with _INVOCATION_LOCK:
            _INVOCATIONS+=1
            if _INVOCATIONS>24: raise CompositionError('invocation_budget','limit')
        single={'store','guard_child','guard_dns','guard_network','guard_worker','guard_spawn','guard_exec'}
        if mode not in single|{'duplicate','collision'}: raise CompositionError('mode','unsupported')
        if observer is None: raise CompositionError('observation','required')
        if (mode in single) != (second_envelope is None): raise CompositionError('mode','second envelope')
        if second_envelope is not None and second_envelope.get('request_id')!=envelope.get('request_id'): raise CompositionError('binding','second request')
        package=package_root.resolve(strict=True)
        expected=hashlib.sha256(canonical_bytes(envelope)).hexdigest(); root=Path(tempfile.mkdtemp(prefix='m02-stage3b-run-',dir='/private/tmp')); data=root/'data'; ready=root/'ready'; release=root/'release'; data.mkdir()
        if package in root.parents or root in package.parents: shutil.rmtree(root); raise CompositionError('boundary','overlap')
        payload={'mode':mode,'dataRoot':str(data),'moduleRoot':str(root/'modules'),'packageRoot':str(package),'readyPath':str(ready),'releasePath':str(release),'envelope':dict(envelope),'secondEnvelope':dict(second_envelope) if second_envelope else None}
        raw=canonical_bytes(payload)
        if len(raw)>MAX_INPUT: shutil.rmtree(root,ignore_errors=True); raise CompositionError('worker_input','limit')
        out=bytearray(); err=bytearray(); overflow=[False]; process=None; primary=None
        try:
            deadline=time.monotonic()+self.timeout_seconds
            process=subprocess.Popen([str(self.node),str(self.worker)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False,env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','LANG':'C','LC_ALL':'C'})
            threads=[threading.Thread(target=_drain,args=(process.stdout,out,process,overflow),daemon=True),threading.Thread(target=_drain,args=(process.stderr,err,process,overflow),daemon=True)]
            for thread in threads:thread.start()
            write_error=[]
            def write_input():
                try: process.stdin.write(raw); process.stdin.close()
                except (BrokenPipeError,OSError) as exc: write_error.append(exc)
            writer=threading.Thread(target=write_input,daemon=True);writer.start()
            while writer.is_alive() and time.monotonic()<deadline: writer.join(.02)
            if writer.is_alive(): process.terminate(); raise CompositionError('worker_input','write timeout')
            while not ready.exists() and process.poll() is None and time.monotonic()<deadline:time.sleep(.02)
            if not ready.exists():
                if process.poll() is not None:
                    for thread in threads:thread.join(1)
                    try:failure=json.loads(bytes(err))
                    except (UnicodeDecodeError,json.JSONDecodeError):failure={}
                    stage=failure.get('stage') if isinstance(failure,dict) else None;guard=failure.get('guard') if isinstance(failure,dict) else None
                    raise CompositionError(stage if isinstance(stage,str) else 'worker_exit',guard if isinstance(guard,str) else 'before readiness')
                raise CompositionError('worker_readiness','marker absent')
            observation=observer(process,None);release.write_text('release\n');process.wait(timeout=max(.01,deadline-time.monotonic()));observer(process,observation)
            for thread in threads:thread.join(1)
            if overflow[0]:raise CompositionError('worker_output','limit')
            if process.returncode:
                try:failure=json.loads(bytes(err))
                except (UnicodeDecodeError,json.JSONDecodeError):failure={}
                stage=failure.get('stage') if isinstance(failure,dict) else None;guard=failure.get('guard') if isinstance(failure,dict) else None
                raise CompositionError(stage if isinstance(stage,str) else 'worker_exit',guard if isinstance(guard,str) else 'failed')
            try:response=json.loads(bytes(out))
            except (UnicodeDecodeError,json.JSONDecodeError) as exc:raise CompositionError('worker_output','invalid JSON') from exc
            if not isinstance(response,dict) or response.get('ok') is not True:raise CompositionError('worker_output','invalid')
            fixture_hashes=[hashlib.sha256(canonical_bytes(item)).hexdigest() for item in CANONICAL_FIXTURES]
            if response.get('canonicalFixtures')!=fixture_hashes:raise CompositionError('canonicalization','fixture mismatch')
            if response.get('networkAttempts')!=0 or response.get('first',{}).get('s256')!=expected:raise CompositionError('cross_language_verification','first')
            if not isinstance(response.get('first',{}).get('version'),int):raise CompositionError('readback','version')
            if second_envelope is not None and response.get('second',{}).get('s256')!=hashlib.sha256(canonical_bytes(second_envelope)).hexdigest():raise CompositionError('cross_language_verification','second')
            return response
        except subprocess.TimeoutExpired as exc:raise CompositionError('worker_timeout','deadline') from exc
        except BaseException as exc:
            primary=exc; raise
        finally:
            if process is not None and process.poll() is None:
                process.terminate()
                try:process.wait(1)
                except subprocess.TimeoutExpired:process.kill();process.wait(1)
            shutil.rmtree(root,ignore_errors=True)
            if root.exists():
                cleanup=CompositionError('cleanup','root remains')
                if primary is not None: raise cleanup from primary
                raise cleanup
