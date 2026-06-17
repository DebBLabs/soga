from __future__ import annotations

import os
from typing import Any, Callable, Dict, Tuple

import yaml

from policy_gate import PolicyGate
from context_logger import log_event

from persona.aiim_context_builder import build_aiim_context
from persona.interface import build_persona_context
from execution.interface import build_execution_context


def _autodetect_settings_path(explicit: str | None) -> str:
    """
    Choose a settings path that works for both local dev and containers.

    Precedence:
      1) explicit arg
      2) SETTINGS_PATH env var
      3) ./settings.yaml (repo root)
      4) /app/settings.yaml (container convention)
    """
    if explicit:
        return explicit

    env_path = os.environ.get("SETTINGS_PATH")
    if env_path:
        return env_path

    if os.path.exists("settings.yaml"):
        return "settings.yaml"

    return "/app/settings.yaml"


def load_settings(settings_path: str | None = None) -> Dict[str, Any]:
    """
    Load verify-related settings from the YAML config file.
    """
    path = _autodetect_settings_path(settings_path)
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return raw.get("verify", {})


def build_gate_and_logger(
    settings_path: str | None = None,
) -> Tuple[PolicyGate, Callable[[Dict[str, Any]], None]]:
    """
    Construct a PolicyGate instance and a logger function that writes
    to the shared event log, enriched with an AIIM-style context envelope.
    """
    cfg = load_settings(settings_path)

    # tolerate either key name
    environment = str(cfg.get("environment", cfg.get("env", "dev"))).strip() or "dev"

    policy_id = cfg.get("policy_id", "P03-delex-stub")
    policy_version = cfg.get("policy_version", "0.1.0")
    log_path = cfg.get("log_path", "logs/events.jsonl")

    gate = PolicyGate(
        policy_id=policy_id,
        policy_version=policy_version,
        delex_config=None,
        policy_file=None,
    )

    def logger(event: Dict[str, Any]) -> None:
        component = event.get("component", "verify")
        action = event.get("action")
        request = event.get("request") or {}
        decision = event.get("decision") or {}

        # P12: persona interface (stub; no inference)
        persona_ctx = build_persona_context(action=action, request=request)

        # Build AIIM context using ONLY the parameters the builder supports,
        # then inject env/persona fields in a backward-compatible way.
        aiim_ctx = build_aiim_context(
            component=component,
            action=action,
            request=request,
            decision=decision,
            policy_id=policy_id,
            policy_version=policy_version,
        )

        # Inject/override (safe even if the builder already adds these)
        aiim_ctx["environment"] = environment
        aiim_ctx["persona"] = persona_ctx

        # P13: execution interface (stub; no inference)
        exec_ctx = build_execution_context(raw={"context_keys": ["action", "component"]})

        enriched_event: Dict[str, Any] = {
            **event,
            "environment": environment,
            "aiim_context": aiim_ctx,
            "execution": {
                "provider": exec_ctx.get("provider", "stub"),
                "output_text": exec_ctx.get("output_text", ""),
                "raw": exec_ctx.get("raw"),
                "timestamp": exec_ctx.get("timestamp"),
                "version": exec_ctx.get("version"),
            },
        }

        log_event(enriched_event, log_path=log_path)

    return gate, logger