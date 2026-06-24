import aiomysql
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import FileResponse

from ..config import BOOKS_DIR
from .. import db

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/search")
async def search(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    words = " ".join(f"+{w}*" for w in q.split() if w)
    if not words:
        return {"total": 0, "limit": limit, "offset": offset, "results": []}

    async with db.POOL.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                """SELECT SQL_CALC_FOUND_ROWS
                          MD5, Title, Author, Publisher, Year,
                          Pages, Language, Extension, Filesize
                   FROM libgenrs_updated
                   WHERE MATCH(Title, Author) AGAINST (%s IN BOOLEAN MODE)
                   ORDER BY ID
                   LIMIT %s OFFSET %s""",
                (words, limit, offset),
            )
            rows = await cur.fetchall()

            await cur.execute("SELECT FOUND_ROWS() AS total")
            total = (await cur.fetchone())["total"]

    return {"total": total, "limit": limit, "offset": offset, "results": rows}


@router.get("/file/{md5}")
async def get_file(md5: str):
    if len(md5) != 32:
        raise HTTPException(400, "Invalid MD5")

    md5_lower = md5.lower()

    async with db.POOL.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT ID, Extension, Visible FROM libgenrs_updated WHERE MD5 = %s",
                (md5_lower,),
            )
            row = await cur.fetchone()

    if not row or row["Visible"] == "no":
        raise HTTPException(404, "File not found")

    folder = str((row["ID"] - 1) // 1000 * 1000)
    file_path = BOOKS_DIR / folder / md5_lower

    if not file_path.exists():
        raise HTTPException(404, "File not found on disk")

    media_type = _guess_media_type(row["Extension"] or "")
    return FileResponse(file_path, media_type=media_type)


_MEDIA_TYPES = {
    "pdf": "application/pdf",
    "djvu": "image/vnd.djvu",
    "epub": "application/epub+zip",
    "mobi": "application/x-mobipocket-ebook",
    "fb2": "text/x-fictionbook+xml",
    "cbr": "application/x-cbr",
    "cbz": "application/x-cbz",
    "zip": "application/zip",
    "rar": "application/vnd.rar",
    "chm": "application/vnd.ms-htmlhelp",
    "txt": "text/plain",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def _guess_media_type(ext: str) -> str:
    return _MEDIA_TYPES.get(ext.lower(), "application/octet-stream")
