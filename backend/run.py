import os
import sys
from pathlib import Path


def load_local_env() -> None:
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')

        if key:
            os.environ.setdefault(key, value)


if __name__ == "__main__":
    load_local_env()

    try:
        import uvicorn
    except ImportError:
        print("Uvicorn is not installed.")
        print("Run: python -m pip install -r requirements.txt")
        sys.exit(1)

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    reload_enabled = os.getenv("RELOAD", "true").lower() == "true"

    print(f"Starting backend on http://{host}:{port}")
    print(f"Docs available at http://{host}:{port}/docs")

    uvicorn.run("app.main:app", host=host, port=port, reload=reload_enabled)
