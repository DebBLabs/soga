"""Synthetic instrumentation tests. Running them requires separate authority."""
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from m02_was_composition import controller
from m02_was_composition.diagnostic_tests import DiagnosticResult, STAGES
from m02_was_composition.adapter import CompositionError

IDENTIFIER='tests.test_m02_was_composition.AdapterContractTests.test_worker_failure_stage_is_preserved'

class SyntheticCase(unittest.TestCase):
    def id(self):return IDENTIFIER
    def runTest(self):raise AssertionError('SECRET bearer token must not escape')

class DiagnosticInstrumentationTests(unittest.TestCase):
    def document(self):
        result=DiagnosticResult({IDENTIFIER});SyntheticCase().run(result)
        return result.document()
    def test_redacts_exception_and_preserves_failure_name(self):
        raw=self.document();self.assertNotIn(b'SECRET',raw);self.assertNotIn(b'bearer',raw)
        value=controller._diagnostic_document(raw,1)
        self.assertEqual(value['records'][0]['test'],IDENTIFIER)
        self.assertEqual(value['records'][0]['stage'],'unknown')
    def test_record_limit_emits_fixed_truncation(self):
        result=DiagnosticResult({IDENTIFIER})
        for _ in range(129):result.addSuccess(SyntheticCase())
        value=json.loads(result.document());self.assertTrue(value['truncated']);self.assertEqual(value['records'],[])
    def test_malformed_and_excess_output_fail_closed(self):
        for raw in (b'not-json',b'x'*16385,b'{}'):
            with self.assertRaises((ValueError,RuntimeError)):controller._diagnostic_document(raw,0)
    def test_retains_execution_and_postflight_failure_atomically(self):
        with tempfile.TemporaryDirectory(prefix='m02-stage3b-diagnostics-',dir='/private/tmp') as directory:
            root=Path(directory)
            with mock.patch.object(controller,'preflight'),mock.patch.object(controller,'snapshot',side_effect=[{'x':1},{'x':2}]),mock.patch.object(controller,'listener_snapshot',side_effect=['same','same']),mock.patch.object(controller,'_focused_execution',return_value=(1,self.document(),b'')):
                result=controller.run_diagnostic_once(expected_soga_head='a'*40,evidence_root=root)
            value=json.loads((root/'record.json').read_bytes())
            self.assertEqual(value['execution'],'focused_tests');self.assertEqual(value['postflight'],'state_changed')
            self.assertFalse(result['ok']);self.assertFalse((root/'record.tmp').exists())
    def test_atomic_write_refuses_preexisting_temporary_file(self):
        with tempfile.TemporaryDirectory(prefix='m02-stage3b-diagnostics-',dir='/private/tmp') as directory:
            root=Path(directory);(root/'record.tmp').write_text('occupied')
            with self.assertRaises(FileExistsError):controller._atomic_record(root,{'schema':1})
            self.assertFalse((root/'record.json').exists())
    def test_controller_failure_stage_is_retained_without_raw_message(self):
        for stage in ('preflight:runtime','observation:lsof_control','execution:child_spawn','SECRET bearer arbitrary'):
            with self.subTest(stage=stage),tempfile.TemporaryDirectory(prefix='m02-stage3b-diagnostics-',dir='/private/tmp') as directory:
                root=Path(directory)
                with mock.patch.object(controller,'preflight',side_effect=RuntimeError(stage)):
                    controller.run_diagnostic_once(expected_soga_head='a'*40,evidence_root=root)
                raw=(root/'record.json').read_bytes();value=json.loads(raw)
                self.assertEqual(value['controller_stage'],'unknown' if stage.startswith('SECRET') else stage)
                self.assertNotIn(b'SECRET',raw)
    def test_unallowlisted_test_identifier_is_rejected(self):
        value=json.loads(self.document());value['records'][0]['test']='tests.test_m02_was_composition.AdapterContractTests.test_injected'
        with self.assertRaisesRegex(RuntimeError,'diagnostic:test'):controller._diagnostic_document(json.dumps(value).encode(),1)
    def test_fixed_worker_stages_are_retained_without_raw_messages(self):
        for stage in ('input','package_resolution','was_import','storage','SECRET arbitrary'):
            with self.subTest(stage=stage):
                result=DiagnosticResult({IDENTIFIER})
                error=CompositionError(stage,'SECRET bearer private data')
                result.addError(SyntheticCase(),(CompositionError,error,None))
                raw=result.document();value=controller._diagnostic_document(raw,1)
                self.assertEqual(value['records'][0]['stage'],'unknown' if stage.startswith('SECRET') else stage)
                self.assertNotIn(b'SECRET',raw);self.assertNotIn(b'bearer',raw)
    def test_every_fixed_worker_stage_is_diagnostic_allowlisted(self):
        source=(Path(__file__).resolve().parents[1]/'m02_was_composition/worker.mjs').read_text()
        declaration=re.search(r'const ERROR_STAGES = new Set\(\[([^\]]+)\]\)',source)
        self.assertIsNotNone(declaration)
        categories=set(re.findall(r"'([a-z_]+)'",declaration.group(1)))
        self.assertTrue(categories);self.assertTrue(categories.issubset(STAGES))
