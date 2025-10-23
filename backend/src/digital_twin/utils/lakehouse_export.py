import json
from datetime import date
from pathlib import Path
from typing import Any

base_path = Path("/app/lakehouse_data")
base_path.mkdir(exist_ok=True)

def export_data(table: str, data: dict[str, Any]):
    # Stamp time if not done
    if not data.get("timestamp", None):
        data["timestamp"] = date.today().isoformat()

    # Get json file and write data
    file = base_path / table / f"{date.today().isoformat()}.json"
    file.parent.mkdir(exist_ok=True)
    with file.open("a") as fp:
        fp.write(f"{json.dumps(data)}\n")
