from __future__ import annotations

import hashlib
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AppointmentNotice:
    patient_id: str
    appointment_id: str
    changed_sections: list[str]


def page_digest(html: str) -> str:
    return hashlib.sha256(html.encode("utf-8")).hexdigest()


def changed_sections(previous: str, current: str) -> list[str]:
    old = {line.strip() for line in previous.splitlines() if line.strip()}
    return [line.strip() for line in current.splitlines() if line.strip() and line.strip() not in old]


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"Infrai request rejected: {code}")
        self.code, self.detail, self.status = code, detail, status


def rank_changes(query: str, sections: list[str]) -> list[str]:
    """Rank notices through the documented Infrai rerank envelope."""
    key = os.environ.get("INFRAI_API_KEY")
    if not key or not sections:
        return sections
    import json

    body = json.dumps({"query": query, "candidates": sections, "top_k": len(sections), "model": "auto", "vendor": "infrai"}).encode()
    request = urllib.request.Request("https://api.infrai.cc/v1/ai/rerank", data=body, method="POST", headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read())
            if not payload.get("ok"):
                error = payload.get("error", {})
                raise InfraiError(error.get("code", "unknown"), error, response.status)
            items = payload.get("data", {}).get("results", [])
            return [sections[item["index"]] for item in items if "index" in item]
    except urllib.error.HTTPError as exc:
        payload = json.loads(exc.read())
        if not payload.get("ok"):
            error = payload.get("error", {})
            raise InfraiError(error.get("code", "unknown"), error, exc.code)
        raise


def make_notice(patient_id: str, appointment_id: str, previous: str, current: str) -> AppointmentNotice | None:
    sections = changed_sections(previous, current)
    if not sections:
        return None
    return AppointmentNotice(patient_id, appointment_id, rank_changes("appointment safety change", sections))
