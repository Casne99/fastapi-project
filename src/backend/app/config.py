from pathlib import Path
from configparser import ConfigParser

_BASE_DIR = Path(__file__).resolve().parent.parent          # src/backend

ACTIVE_PROFILE = (_BASE_DIR / "profile").read_text().strip()

_parser = ConfigParser()
_parser.read(_BASE_DIR / "profiles.ini")

# ── Database ─────────────────────────────────────────────────────────
DATABASE_URL: str = _parser.get(ACTIVE_PROFILE, "DATABASE_URL")

# ── JWT ──────────────────────────────────────────────────────────────
SECRET_KEY = "supersegreto"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
