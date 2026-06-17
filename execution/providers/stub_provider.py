from __future__ import annotations

from execution.provider_base import ExecutionRequest, ExecutionResult


class StubProvider:
    name = "stub"

    def execute(self, req: ExecutionRequest) -> ExecutionResult:
        return ExecutionResult(
            output_text="STUB: execution provider not yet wired (P13).",
            provider=self.name,
            model=req.model_hint,
            usage=None,
            raw={"context_keys": sorted(list(req.context.keys()))},
        )