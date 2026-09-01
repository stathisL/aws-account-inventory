from typing import Any, TypedDict


class InventoryResult(TypedDict):
    service: str
    resources: list[dict[str, Any]]
