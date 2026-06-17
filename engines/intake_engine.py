from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import re

from engines.observation_extractor import ObservationExtractor


SECTOR_ROOT = Path("research/sectors")

SECTOR_FILES = [
    "README.md",
    "applicability.md",
    "glean_rules.md",
    "confirmation_rules.md",
    "questions.md",
    "mappings.md",
    "examples.md",
    "derived_examples.md",
    "intake_example.md",
    "sources.md",
]


@dataclass
class SectorKnowledge:
    sector: str
    root: str
    files_loaded: list[str]
    files_missing: list[str]
    content: dict[str, str]


class MissionIntakeEngine:
    def __init__(self) -> None:
        self.observation_extractor = ObservationExtractor()

    """
    Mission Intake Engine

    Raw Request
        ↓
    Sector knowledge inspection
        ↓
    Canonical Mission JSON candidate

    This engine represents the Subject.
    It does not perform governance evaluation.
    """

    def load_sector(self, sector: str) -> SectorKnowledge:
        root = SECTOR_ROOT / sector

        if not root.exists():
            raise FileNotFoundError(f"Sector package not found: {root}")

        loaded: list[str] = []
        missing: list[str] = []
        content: dict[str, str] = {}

        for filename in SECTOR_FILES:
            path = root / filename
            key = filename.replace(".md", "")
            if path.exists():
                loaded.append(filename)
                content[key] = path.read_text(encoding="utf-8")
            else:
                missing.append(filename)
                content[key] = ""

        return SectorKnowledge(
            sector=sector,
            root=str(root),
            files_loaded=loaded,
            files_missing=missing,
            content=content,
        )


    def detect_sectors(self, raw_request: str) -> list[str]:
        text = raw_request.lower()
        sectors: list[str] = []

        keyword_map = {
            "healthcare": [
                "medical", "doctor", "appointment", "medication", "refill",
                "pharmacy", "clinic", "provider", "specialist"
            ],
            "calendar": [
                "schedule", "appointment", "meeting", "calendar", "reschedule"
            ],
            "travel": [
                "travel", "flight", "hotel", "trip", "airport"
            ],
            "commerce": [
                "buy", "purchase", "order", "budget", "spend", "expense"
            ],
        }

        for sector, keywords in keyword_map.items():
            if any(keyword in text for keyword in keywords):
                sectors.append(sector)

        return sectors



    def parse_questions(self, questions_md: str) -> list[dict[str, str]]:
        questions: list[dict[str, str]] = []
        current: dict[str, str] | None = None
        current_lines: list[str] = []
        current_category = ""

        def close_current() -> None:
            nonlocal current, current_lines
            if current is not None:
                current["body"] = "\n".join(current_lines).strip()
                questions.append(current)
                current = None
                current_lines = []

        for line in questions_md.splitlines():
            coded = re.match(r"^##\s+([A-Z]\d{3})\s+(.+)$", line)
            category = re.match(r"^#\s+(.+)$", line)

            if coded:
                close_current()
                current = {
                    "id": coded.group(1),
                    "title": coded.group(2).strip(),
                    "category": current_category,
                    "question": "",
                    "cmr_mapping": "",
                    "body": "",
                }
                current_lines = []
                continue

            if category and not line.startswith("##"):
                current_category = category.group(1).strip()
                continue

            stripped = line.strip()

            # Calendar-style packages use category headings plus bullet questions.
            if stripped.startswith("- "):
                question_text = stripped[2:].strip()
                if not question_text.endswith("?"):
                    if current is not None:
                        current_lines.append(line)
                    continue

                close_current()
                generated_id = f"{current_category[:3].upper()}-{len(questions) + 1:03d}"
                questions.append(
                    {
                        "id": generated_id,
                        "title": current_category,
                        "category": current_category,
                        "question": question_text,
                        "cmr_mapping": current_category,
                        "body": question_text,
                    }
                )
                continue

            if current is None:
                continue

            if stripped.startswith("Question:"):
                current["question"] = stripped.replace("Question:", "").strip()
            elif stripped.startswith("CMR mapping:"):
                current["cmr_mapping"] = stripped.replace("CMR mapping:", "").strip()

            current_lines.append(line)

        close_current()

        return questions


    def evaluate_question(
        self,
        question: dict[str, str],
        raw_request: str,
        gleaned: dict[str, Any],
    ) -> dict[str, Any]:
        request = raw_request.lower()
        q_text = question.get("question", "").lower()
        mapping = question.get("cmr_mapping", "")

        status = "ASK"
        reason = "Question may be needed for mission intake."

        medication_terms = ["medication", "molecule", "dose", "pharmacy", "dispense", "substitution"]
        if (
            any(term in q_text for term in medication_terms)
            and "appointment" in request
            and "medication" not in request
            and "refill" not in request
            and "pharmacy" not in request
        ):
            status = "NOT_APPLICABLE"
            reason = "Medication-specific question does not apply to an appointment-management request."

        elif "objective" in mapping and gleaned.get("objective"):
            status = "ANSWERED"
            reason = "Objective was gleaned from original request."

        elif "representative" in q_text or "who may" in q_text or "authority" in q_text:
            if gleaned.get("delegate"):
                status = "CONFIRM"
                reason = "Delegate was mentioned, but identity and authority boundary require confirmation."

        elif "travel" in q_text or "reachable" in q_text:
            if "travel" in request or "traveling" in request:
                status = "CONFIRM"
                reason = "Travel context was mentioned, but reachability details require confirmation."

        elif (
            ("what are you trying to schedule" in q_text)
            or ("what outcome are you trying to achieve" in q_text)
            or ("healthcare objective" in q_text)
        ):
            if "appointment" in request or "appointments" in request:
                status = "ANSWERED"
                reason = "Appointment management was stated in the original request."

        return {
            "id": question.get("id", ""),
            "title": question.get("title", ""),
            "question": question.get("question", ""),
            "cmr_mapping": question.get("cmr_mapping", ""),
            "status": status,
            "reason": reason,
        }

    def evaluate_questions(
        self,
        raw_request: str,
        parsed_questions: dict[str, list[dict[str, str]]],
        gleaned: dict[str, Any],
    ) -> dict[str, list[dict[str, Any]]]:
        return {
            sector: [
                self.evaluate_question(question, raw_request, gleaned)
                for question in questions
            ]
            for sector, questions in parsed_questions.items()
        }


    def collect_evidence(
        self,
        raw_request: str,
        evaluated_questions: dict[str, list[dict[str, Any]]],
        gleaned: dict[str, Any],
    ) -> list[dict[str, Any]]:
        evidence: list[dict[str, Any]] = []

        if gleaned.get("delegate"):
            for sector, questions in evaluated_questions.items():
                matching_question_ids: list[str] = []

                for question in questions:
                    q_text = question.get("question", "").lower()
                    if "who may" in q_text or "authority" in q_text or "representative" in q_text:
                        matching_question_ids.append(str(question.get("id")))

                if matching_question_ids:
                    evidence.append(
                        {
                            "evidence_kind": "delegation_candidate",
                            "sector": sector,
                            "candidate_value": gleaned["delegate"]["value"],
                            "question_ids": matching_question_ids,
                            "source": "original_request",
                            "source_text": raw_request,
                            "confidence": 0.72,
                            "status": "PROPOSED",
                            "reason": "Delegate was mentioned but identity and authority boundary require confirmation.",
                        }
                    )

        if gleaned.get("objective"):
            evidence.append(
                {
                    "evidence_kind": "objective_candidate",
                    "sector": "cross-sector",
                    "candidate_value": gleaned["objective"]["value"],
                    "question_ids": ["objective"],
                    "source": "original_request",
                    "source_text": raw_request,
                    "confidence": 0.95,
                    "status": "PROPOSED",
                    "reason": "Objective was directly stated in the request.",
                }
            )

        return evidence

    def glean(self, raw_request: str) -> dict[str, Any]:
        observations = self.observation_extractor.extract(raw_request)

        gleaned: dict[str, Any] = {}
        unresolved: list[str] = []

        for observation in observations:
            semantic_type = observation.get("semantic_type")
            if semantic_type == "delegate":
                gleaned["delegate"] = observation
                unresolved.append("Confirm delegate identity and authority boundary.")
            elif semantic_type == "objective":
                gleaned["objective"] = observation
            elif semantic_type == "context":
                gleaned["context"] = observation
                unresolved.append("Confirm execution context and reachability.")

        return {
            "candidate_observations": observations,
            "gleaned": gleaned,
            "unresolved": unresolved,
        }

    def inspect(self, raw_request: str, sector: str | None = None) -> dict[str, Any]:
        detected_sectors = self.detect_sectors(raw_request)

        selected_sectors = [sector] if sector else detected_sectors

        sector_packages = [
            asdict(self.load_sector(selected_sector))
            for selected_sector in selected_sectors
        ]

        parsed_questions = {
            package["sector"]: self.parse_questions(package["content"].get("questions", ""))
            for package in sector_packages
        }

        glean_result = self.glean(raw_request)

        evaluated_questions = self.evaluate_questions(
            raw_request,
            parsed_questions,
            glean_result["gleaned"],
        )

        evidence = self.collect_evidence(
            raw_request,
            evaluated_questions,
            glean_result["gleaned"],
        )

        return {
            "status": "INSPECTED",
            "original_request": raw_request,
            "detected_sectors": detected_sectors,
            "selected_sectors": selected_sectors,
            "sector_packages": sector_packages,
            "parsed_questions": parsed_questions,
            "evaluated_questions": evaluated_questions,
            "candidate_observations": glean_result["candidate_observations"],
            "gleaned": glean_result["gleaned"],
            "evidence": evidence,
            "unresolved": glean_result["unresolved"],
            "notes": [
                "Original request preserved.",
                "Applicable sectors detected using minimal keyword rules.",
                "Sector packages loaded from research/sectors.",
                "Initial deterministic gleaning completed.",
                "CMR generation not yet implemented.",
            ],
        }
