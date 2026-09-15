"""D-065 create-only tests. Execution requires Phase 3B-2 authorization."""
import os, shutil, tempfile, unittest
from pathlib import Path
from unittest import mock
from m02_was_composition.adapter import CompositionAdapter, CompositionError, build_evidence_envelope, canonical_bytes
from m02_was_composition.controller import observe_process
from m02_was_composition import controller

ROOT=Path(__file__).parents[1]; WORKER=ROOT/'m02_was_composition/worker.mjs'; WAS=Path('/private/tmp/m02-stage3lib-20260910/was-teaching-server')

def result(**changes):
    value={'request_id':'request-1','subject':'person-test','action':'store-evidence','projection':'granted','status':'terminal','mission_s256':'abc123','authority_reference':'pt-test'}
    value.update(changes);return value

def envelope(**changes):
    value=build_evidence_envelope(issuer='urn:soga:test-ps',correlation_id='c-1',result=result(),expected_subject='person-test',expected_mission='abc123',expected_request='request-1')
    value.update(changes);return value

def live_observer(process,baseline=None):
    if baseline is None:
        if process.poll() is not None: raise RuntimeError('worker not live')
        return 'observed'
    if process.poll() is None: raise RuntimeError('worker survived')

class CanonicalEnvelopeTests(unittest.TestCase):
    def test_bool_integer_and_key_order(self): self.assertEqual(canonical_bytes({'z':True,'a':1}),b'{"a":1,"z":true}')
    def test_control_characters(self): self.assertEqual(canonical_bytes({'v':'\b\f\n\r\t\x00\x1f\x7f'}),b'{"v":"\\b\\f\\n\\r\\t\\u0000\\u001f\x7f"}')
    def test_rejects_float_non_ascii_unsafe_integer_and_non_plain_type(self):
        for value in (1.5,'caf\N{LATIN SMALL LETTER E WITH ACUTE}',9_007_199_254_740_992,{1,2}):
            with self.subTest(value=value),self.assertRaises(CompositionError):canonical_bytes({'value':value})
    def test_projection_is_non_secret_and_bounded(self):
        value=envelope();self.assertEqual(value['interpretation'],'person_server_evidence_only');self.assertNotIn('authority_reference',value)
    def test_unknown_secret_and_bad_authority_fail_closed(self):
        for change in ({'unknown':'x'},{'person_token':'x'},{'authority_reference':'\N{SNOWMAN}'}):
            with self.subTest(change=change),self.assertRaises(CompositionError):build_evidence_envelope(issuer='urn:test',correlation_id='c',result=result(**change))
    def test_wrong_bindings_fail_at_binding(self):
        for name,expected in (('expected_subject','other'),('expected_mission','other'),('expected_request','other')):
            with self.subTest(name=name),self.assertRaises(CompositionError) as caught:build_evidence_envelope(issuer='urn:test',correlation_id='c',result=result(),**{name:expected})
            self.assertEqual(caught.exception.stage,'binding')
    def test_invalid_issuer_and_correlation_fail(self):
        for issuer,correlation in (('', 'c'),('urn:test',''),('\N{SNOWMAN}','c')):
            with self.assertRaises(CompositionError):build_evidence_envelope(issuer=issuer,correlation_id=correlation,result=result())

class AdapterContractTests(unittest.TestCase):
    def test_rejects_mode_and_second_binding_before_worker(self):
        adapter=CompositionAdapter(worker=WORKER)
        with self.assertRaises(CompositionError):adapter.store(envelope=envelope(),package_root=WAS,mode='other')
        with self.assertRaises(CompositionError) as caught:adapter.store(envelope=envelope(),package_root=WAS,mode='duplicate',second_envelope=envelope(request_id='other'),observer=live_observer)
        self.assertEqual(caught.exception.stage,'binding')
    def test_observer_is_mandatory_before_worker(self):
        with self.assertRaises(CompositionError) as caught:CompositionAdapter(worker=WORKER).store(envelope=envelope(),package_root=WAS)
        self.assertEqual(caught.exception.stage,'observation')
    def test_worker_source_has_guards_holdpoint_and_no_listener(self):
        source=WORKER.read_text()
        for text in ('syncBuiltinESMExports()','dnsPromises.lookup','readyPath','releasePath',"ifNoneMatch: true","kind: 'binary'"):
            self.assertIn(text,source)
        self.assertNotIn('createApp(',source);self.assertNotIn('.listen(',source)
        self.assertIn("request.mode === 'guard_child'",source)
    def test_adapter_pins_runtime_and_bounds_streaming_output(self):
        source=(ROOT/'m02_was_composition/adapter.py').read_text()
        self.assertIn("EXPECTED_NODE=Path('/opt/homebrew/Cellar/node/26.7.0/bin/node')",source)
        self.assertIn('process.terminate()',source);self.assertNotIn('subprocess.run(',source)
    def test_worker_failure_stage_is_preserved(self):
        fake=mock.Mock(returncode=1);fake.poll.return_value=1
        # Structural assertion: stderr is parsed and its stage is used.
        source=(ROOT/'m02_was_composition/adapter.py').read_text()
        self.assertIn("failure.get('stage')",source)
    def test_controller_regenerates_manifest_and_checks_identity(self):
        source=(ROOT/'m02_was_composition/controller.py').read_text()
        for text in ("rglob('*')","rev-parse','HEAD^{tree}","Python 3.9.6","v26.7.0","GIT_OPTIONAL_LOCKS"):
            self.assertIn(text,source)
    def test_controller_has_observation_and_cleanup_gates(self):
        source=(ROOT/'m02_was_composition/controller.py').read_text()
        for text in ('lsof_control','worker_socket','listener_snapshot','temporary_paths','state_changed'):
            self.assertIn(text,source)
        self.assertIn("m02-stage3b-fake-*",source)
    def test_storage_projection_cannot_carry_governance_semantics(self):
        forbidden={'permission','identity','authority','consent','admission','payment','execution'}
        self.assertTrue(forbidden.isdisjoint(envelope()))

class ControllerNegativeTests(unittest.TestCase):
    def test_wrong_soga_head_fails_preflight(self):
        with mock.patch.object(controller,'_run',return_value='different'):
            with self.assertRaisesRegex(RuntimeError,'preflight:soga_head'):controller.preflight(expected_soga_head='0'*40)
    def test_manifest_count_and_hash_fail_closed(self):
        with mock.patch.object(controller,'_manifest',return_value='wrong'),mock.patch.object(controller,'_run',side_effect=['1'*40,controller.HEAD,controller.TREE,'Python 3.9.6','v26.7.0']):
            with self.assertRaisesRegex(RuntimeError,'preflight:manifest'):controller.preflight(expected_soga_head='1'*40)
    def test_was_identity_runtime_and_candidate_fail_closed(self):
        cases=(
            (['1'*40,'wrong'], 'preflight:was_identity'),
            (['1'*40,controller.HEAD,controller.TREE,'wrong'], 'preflight:runtime'),
            (['1'*40,controller.HEAD,controller.TREE,'Python 3.9.6','v26.7.0'], 'preflight:candidate'),
        )
        for outputs,stage in cases:
            with self.subTest(stage=stage),mock.patch.object(controller,'_run',side_effect=outputs),mock.patch.object(controller,'_manifest',return_value=controller.MANIFEST_SHA),mock.patch.object(Path,'is_file',return_value=False):
                with self.assertRaisesRegex(RuntimeError,stage):controller.preflight(expected_soga_head='1'*40)
    def test_controller_detects_leftover_temporary_path(self):
        fake=Path('/private/tmp/m02-stage3b-fake-test')
        with mock.patch.object(controller,'preflight'),mock.patch.object(controller,'snapshot',side_effect=[{'x':1},{'x':1}]),mock.patch.object(controller,'listener_snapshot',side_effect=['same','same']),mock.patch.object(controller,'_focused_execution',return_value=(0,b'',b'')),mock.patch.object(Path,'glob',side_effect=[[],[fake],[]]):
            with self.assertRaisesRegex(RuntimeError,'postflight:temporary_paths'):controller.run_once(expected_soga_head='1'*40)

@unittest.skipUnless(os.environ.get('M02_STAGE3B_EXECUTE')=='1','Phase 3B-2 not authorized')
class AuthorizedCompositionTests(unittest.TestCase):
    def setUp(self): self.adapter=CompositionAdapter(worker=WORKER)
    def test_successful_write_read_and_hash(self):
        response=self.adapter.store(envelope=envelope(),package_root=WAS,observer=observe_process)
        self.assertFalse(response['first']['idempotent']);self.assertEqual(response['networkAttempts'],0)
        self.assertEqual(len(response['canonicalFixtures']),3)
    def test_duplicate_is_idempotent_in_one_worker(self):
        value=envelope();response=self.adapter.store(envelope=value,package_root=WAS,mode='duplicate',second_envelope=value,observer=observe_process)
        self.assertTrue(response['second']['idempotent'])
    def test_changed_content_collision_has_named_stage(self):
        changed=envelope();changed['status']='changed';changed['result_s256']='changed-result-hash'
        with self.assertRaises(CompositionError) as caught:self.adapter.store(envelope=envelope(),package_root=WAS,mode='collision',second_envelope=changed,observer=observe_process)
        self.assertEqual(caught.exception.stage,'collision')
    def test_unsupported_interpretation_fails_at_binding(self):
        with self.assertRaises(CompositionError) as caught:self.adapter.store(envelope=envelope(interpretation='permission'),package_root=WAS,observer=observe_process)
        self.assertEqual(caught.exception.stage,'binding')
    def test_was_named_child_process_binding_is_guarded(self):
        with self.assertRaises(CompositionError) as caught:self.adapter.store(envelope=envelope(),package_root=WAS,mode='guard_child',observer=observe_process)
        self.assertEqual(caught.exception.stage,'prohibited_api')
        self.assertIn('child_process.execFile',str(caught.exception))
    def test_dns_and_network_guards_intercept_before_system_call(self):
        for mode,guard in (('guard_dns','dns.promises.lookup'),('guard_network','net.connect')):
            with self.subTest(mode=mode),self.assertRaises(CompositionError) as caught:self.adapter.store(envelope=envelope(),package_root=WAS,mode=mode,observer=observe_process)
            self.assertEqual(caught.exception.stage,'prohibited_api')
            self.assertIn(guard,str(caught.exception))
    def test_worker_thread_spawn_and_exec_guards(self):
        for mode,guard in (('guard_worker','worker_threads.Worker'),('guard_spawn','child_process.spawn'),('guard_exec','child_process.exec')):
            with self.subTest(mode=mode),self.assertRaises(CompositionError) as caught:self.adapter.store(envelope=envelope(),package_root=WAS,mode=mode,observer=observe_process)
            self.assertEqual(caught.exception.stage,'prohibited_api')
            self.assertIn(guard,str(caught.exception))
    def _fake_worker(self,body):
        directory=tempfile.TemporaryDirectory(prefix='m02-stage3b-fake-',dir='/private/tmp');path=Path(directory.name)/'worker.mjs'
        path.write_text("import fs from 'node:fs';let b='';for await(const c of process.stdin)b+=c;const r=JSON.parse(b);fs.writeFileSync(r.readyPath,'ready\\n',{flag:'wx'});while(!fs.existsSync(r.releasePath))await new Promise(x=>setTimeout(x,5));"+body)
        self.addCleanup(directory.cleanup);return path
    def test_mismatched_hash_fails_cross_language_verification(self):
        worker=self._fake_worker("process.stdout.write(JSON.stringify({ok:true,networkAttempts:0,first:{s256:'wrong',version:1}}));")
        with self.assertRaises(CompositionError) as caught:CompositionAdapter(worker=worker).store(envelope=envelope(),package_root=WAS,observer=live_observer)
        self.assertEqual(caught.exception.stage,'cross_language_verification')
    def test_malformed_nonzero_and_excess_output_have_named_stages(self):
        cases=(("process.stdout.write('not-json');",'worker_output'),("process.stderr.write(JSON.stringify({ok:false,stage:'partial_write'}));process.exitCode=1;",'partial_write'),("process.stdout.write('x'.repeat(70000));",'worker_output'))
        for body,stage in cases:
            with self.subTest(stage=stage),self.assertRaises(CompositionError) as caught:CompositionAdapter(worker=self._fake_worker(body)).store(envelope=envelope(),package_root=WAS,observer=live_observer)
            self.assertEqual(caught.exception.stage,stage)
    def test_timeout_is_named_and_temp_root_is_removed(self):
        before=set(Path('/private/tmp').glob('m02-stage3b-run-*'))
        with self.assertRaises(CompositionError) as caught:CompositionAdapter(worker=self._fake_worker("await new Promise(()=>{});"),timeout_seconds=1).store(envelope=envelope(),package_root=WAS,observer=live_observer)
        self.assertEqual(caught.exception.stage,'worker_timeout');self.assertEqual(set(Path('/private/tmp').glob('m02-stage3b-run-*')),before)
    def test_cleanup_failure_is_named_and_chains_primary(self):
        before=set(Path('/private/tmp').glob('m02-stage3b-run-*'));real_rmtree=shutil.rmtree
        try:
            with mock.patch('m02_was_composition.adapter.shutil.rmtree',return_value=None):
                with self.assertRaises(CompositionError) as caught:CompositionAdapter(worker=self._fake_worker("process.stderr.write(JSON.stringify({ok:false,stage:'primary'}));process.exitCode=1;")).store(envelope=envelope(),package_root=WAS,observer=live_observer)
            self.assertEqual(caught.exception.stage,'cleanup');self.assertIsNotNone(caught.exception.__cause__)
        finally:
            for path in set(Path('/private/tmp').glob('m02-stage3b-run-*'))-before:real_rmtree(path,ignore_errors=True)
    def test_oversized_worker_input_fails_before_spawn(self):
        huge=envelope();huge['projection']='x'*65000
        with self.assertRaises(CompositionError) as caught:self.adapter.store(envelope=huge,package_root=WAS,observer=live_observer)
        self.assertEqual(caught.exception.stage,'worker_input')

if __name__=='__main__':unittest.main()
