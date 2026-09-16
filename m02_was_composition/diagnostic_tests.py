"""Bounded child-process diagnostic runner; execution requires PI authority."""
import ast
import contextlib
import json
import os
import unittest
from pathlib import Path

MAX_RECORDS = 128
MAX_JSON = 16384
CLASSES = {'CanonicalEnvelopeTests', 'AdapterContractTests', 'ControllerNegativeTests', 'AuthorizedCompositionTests'}
OUTCOMES = {'success', 'failure', 'error', 'skip'}
ERROR_CLASSES = {'AssertionError', 'CompositionError', 'RuntimeError', 'TypeError', 'ValueError', 'OSError', 'FileNotFoundError', 'TimeoutExpired'}
STAGES = {'canonicalization', 'envelope_validation', 'secret_screen', 'binding', 'mode', 'observation', 'invocation_budget', 'worker_input', 'worker_readiness', 'worker_exit', 'worker_output', 'worker_timeout', 'cross_language_verification', 'readback', 'collision', 'prohibited_api', 'cleanup', 'partial_write', 'boundary', 'identifier', 'holdpoint'}

def allowed_test_identifiers():
    source=Path(__file__).resolve().parent.parent/'tests/test_m02_was_composition.py'
    tree=ast.parse(source.read_text())
    return {f'tests.test_m02_was_composition.{node.name}.{method.name}'
            for node in tree.body if isinstance(node,ast.ClassDef) and node.name in CLASSES
            for method in node.body if isinstance(method,ast.FunctionDef) and method.name.startswith('test_')}

class DiagnosticResult(unittest.TestResult):
    def __init__(self, allowed):
        super().__init__()
        self.allowed = frozenset(allowed)
        self.records = []
        self.counts = {'failure': 0, 'error': 0, 'skip': 0}
        self.truncated = False

    def record(self, test, outcome, error=None):
        identifier = test.id()
        if identifier not in self.allowed:
            self.truncated = True
            self.stop()
            return
        if outcome in self.counts:
            self.counts[outcome] += 1
        if len(self.records) >= MAX_RECORDS:
            self.truncated = True
            self.stop()
            return
        error_class = 'none' if error is None else error[0].__name__
        if error_class not in ERROR_CLASSES | {'none'}:
            error_class = 'unknown'
        stage = getattr(error[1], 'stage', None) if error else None
        self.records.append({'test': identifier, 'outcome': outcome,
                             'error_class': error_class,
                             'stage': stage if stage in STAGES else 'unknown'})

    def addSuccess(self, test): self.record(test, 'success')
    def addFailure(self, test, err): self.record(test, 'failure', err)
    def addError(self, test, err): self.record(test, 'error', err)
    def addSkip(self, test, reason): self.record(test, 'skip')
    def addSubTest(self, test, subtest, err):
        if err is not None:
            self.record(test, 'failure' if issubclass(err[0], test.failureException) else 'error', err)
    def addExpectedFailure(self, test, err): self.record(test, 'error', err)
    def addUnexpectedSuccess(self, test): self.record(test, 'failure')

    def document(self):
        status = 1 if self.truncated or self.counts['failure'] or self.counts['error'] else 0
        value = {'schema': 1, 'tests_run': self.testsRun, 'counts': self.counts,
                 'records': self.records, 'truncated': self.truncated, 'exit_status': status}
        raw = json.dumps(value, sort_keys=True, separators=(',', ':')).encode('ascii')
        if self.truncated or len(raw) > MAX_JSON:
            value = {'schema': 1, 'tests_run': self.testsRun, 'counts': self.counts,
                     'records': [], 'truncated': True, 'exit_status': 1}
            raw = json.dumps(value, sort_keys=True, separators=(',', ':')).encode('ascii')
        return raw

def main():
    # Import and test execution occur only in this explicitly invoked child.
    with open(os.devnull, 'w') as sink, contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        from tests import test_m02_was_composition as focused
        result = DiagnosticResult(allowed_test_identifiers())
        unittest.defaultTestLoader.loadTestsFromModule(focused).run(result)
    raw = result.document()
    print(raw.decode('ascii'), end='')
    return json.loads(raw)['exit_status']

if __name__ == '__main__':
    raise SystemExit(main())
