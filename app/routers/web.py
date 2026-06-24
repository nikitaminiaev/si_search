from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["web"])

_HERE = Path(__file__).parent
_TEMPLATES = _HERE.parent / "templates"
_INDEX_HTML = (_TEMPLATES / "index.html").read_text(encoding="utf-8")


@router.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(_INDEX_HTML)
