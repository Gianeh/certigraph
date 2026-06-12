"""Canonical hashes and lightweight certificate envelopes.

These helpers are intentionally small: they make a JSON certificate portable,
cacheable, and auditable without introducing a cryptographic signing dependency.
Signing can be layered on top by downstream users with Sigstore, minisign, GPG,
or an organization-specific transparency log.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, Mapping

SCHEMA_VERSION = "certigraph-envelope-v1"


def canonical_json(data: Any) -> str:
    """Return a deterministic UTF-8 JSON representation for JSON-like data.

    The function expects data that is already JSON serializable. It deliberately
    avoids custom encoders so that surprising objects fail loudly at the caller
    boundary.
    """

    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha256_json(data: Any) -> str:
    """SHA-256 digest of ``canonical_json(data)`` as lowercase hex."""

    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


def make_envelope(kind: str, payload: Mapping[str, Any], *, producer: str = "unknown") -> Dict[str, Any]:
    """Wrap a certificate payload with stable metadata and a payload hash."""

    payload_dict = dict(payload)
    return {
        "schema": SCHEMA_VERSION,
        "kind": kind,
        "producer": producer,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "payload_sha256": sha256_json(payload_dict),
        "payload": payload_dict,
    }


def check_envelope(envelope: Mapping[str, Any]) -> bool:
    """Return True iff the envelope payload hash matches the payload."""

    if envelope.get("schema") != SCHEMA_VERSION:
        return False
    payload = envelope.get("payload")
    digest = envelope.get("payload_sha256")
    if not isinstance(digest, str):
        return False
    return sha256_json(payload) == digest
