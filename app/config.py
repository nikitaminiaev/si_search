from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import os

BASE_MOUNT = os.getenv("BASE_MOUNT", "/mnt/hdd")
BOOKS_DIR = Path(os.getenv("BOOKS_DIR", f"{BASE_MOUNT}/libgen/libgen"))

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "libgen"),
    "password": os.getenv("DB_PASSWORD", "libgen"),
    "db": os.getenv("DB_NAME", "libgen"),
    "unix_socket": os.getenv("DB_SOCKET", "/run/mysqld/mysqld.sock"),
}
