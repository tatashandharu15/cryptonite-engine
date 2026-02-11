from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ModelVersion:
    model_name: str
    version: str
    artifact_path: str
    metrics: dict[str, float]
    created_at: str


class ModelRegistry:
    def __init__(self, registry_file: str = "models/registry/registry.json") -> None:
        self._path = Path(registry_file)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._path.write_text("[]", encoding="utf-8")

    def _read(self) -> list[dict[str, Any]]:
        return json.loads(self._path.read_text(encoding="utf-8"))

    def _write(self, records: list[dict[str, Any]]) -> None:
        self._path.write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")

    def register(
        self,
        model_name: str,
        version: str,
        artifact_path: str,
        metrics: dict[str, float] | None = None,
    ) -> ModelVersion:
        entry = ModelVersion(
            model_name=model_name,
            version=version,
            artifact_path=artifact_path,
            metrics=metrics or {},
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        records = self._read()
        records.append(asdict(entry))
        self._write(records)
        return entry

    def latest(self, model_name: str) -> ModelVersion | None:
        records = [item for item in self._read() if item.get("model_name") == model_name]
        if not records:
            return None
        latest_record = records[-1]
        return ModelVersion(**latest_record)
