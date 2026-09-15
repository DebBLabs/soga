"""Bounded create-only Person Server/WAS composition source (D-065)."""

from .adapter import CompositionAdapter, CompositionError, build_evidence_envelope

__all__ = ["CompositionAdapter", "CompositionError", "build_evidence_envelope"]
