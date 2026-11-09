"""SQLite-backed job/post store.

Responsibilities:
- Track segments, clips, and posts so the pipeline survives restarts.
- Prevent duplicate uploads via a UNIQUE(platform, content_hash) constraint.
- Provide safe retry accounting with backoff.
- Enforce per-platform daily limits and a consecutive-failure circuit breaker.

The store is the source of truth; files on disk are derived state.
"""
from __future__ import annotations

import hashlib
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

SCHEMA = """
CREATE TABLE IF NOT EXISTS segments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL UNIQUE,
    content_hash TEXT,
    created_at REAL NOT NULL,
    processed INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS clips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_hash TEXT NOT NULL UNIQUE,
    source TEXT NOT NULL,
    start REAL NOT NULL,
    end REAL NOT NULL,
    score REAL NOT NULL,
    render_path TEXT,
    created_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    status TEXT NOT NULL,          -- pending | success | failed | skipped
    external_id TEXT,
    error TEXT,
    attempts INTEGER NOT NULL DEFAULT 0,
    next_attempt_at REAL NOT NULL DEFAULT 0,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    UNIQUE(platform, content_hash)
);
"""


def hash_file(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def hash_spec(*parts: object) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(repr(part).encode("utf-8"))
    return h.hexdigest()


@dataclass
class PostRecord:
    id: int
    platform: str
    content_hash: str
    status: str
    external_id: Optional[str]
    error: Optional[str]
    attempts: int
    next_attempt_at: float


class JobStore:
    def __init__(self, db_path: str):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    # ---- segments -------------------------------------------------------
    def record_segment(self, path: str, content_hash: Optional[str] = None) -> int:
        now = time.time()
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO segments(path, content_hash, created_at) VALUES(?,?,?)",
            (path, content_hash, now),
        )
        self.conn.commit()
        if cur.lastrowid:
            return cur.lastrowid
        row = self.conn.execute("SELECT id FROM segments WHERE path=?", (path,)).fetchone()
        return int(row["id"])

    def mark_segment_processed(self, path: str) -> None:
        self.conn.execute("UPDATE segments SET processed=1 WHERE path=?", (path,))
        self.conn.commit()

    def is_segment_processed(self, path: str) -> bool:
        row = self.conn.execute(
            "SELECT processed FROM segments WHERE path=?", (path,)
        ).fetchone()
        return bool(row and row["processed"])

    # ---- clips ----------------------------------------------------------
    def record_clip(self, content_hash: str, source: str, start: float, end: float,
                    score: float, render_path: Optional[str] = None) -> bool:
        """Return True if newly inserted, False if the clip already existed (dedup)."""
        now = time.time()
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO clips(content_hash, source, start, end, score, render_path, created_at)"
            " VALUES(?,?,?,?,?,?,?)",
            (content_hash, source, start, end, score, render_path, now),
        )
        self.conn.commit()
        return cur.rowcount > 0

    def set_clip_render(self, content_hash: str, render_path: str) -> None:
        self.conn.execute(
            "UPDATE clips SET render_path=? WHERE content_hash=?", (render_path, content_hash)
        )
        self.conn.commit()

    def clip_exists(self, content_hash: str) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM clips WHERE content_hash=?", (content_hash,)
        ).fetchone()
        return row is not None

    # ---- posts (idempotent) --------------------------------------------
    def already_posted(self, platform: str, content_hash: str) -> bool:
        row = self.conn.execute(
            "SELECT status FROM posts WHERE platform=? AND content_hash=?",
            (platform, content_hash),
        ).fetchone()
        return bool(row and row["status"] == "success")

    def get_post(self, platform: str, content_hash: str) -> Optional[PostRecord]:
        row = self.conn.execute(
            "SELECT * FROM posts WHERE platform=? AND content_hash=?",
            (platform, content_hash),
        ).fetchone()
        if not row:
            return None
        return PostRecord(
            id=row["id"], platform=row["platform"], content_hash=row["content_hash"],
            status=row["status"], external_id=row["external_id"], error=row["error"],
            attempts=row["attempts"], next_attempt_at=row["next_attempt_at"],
        )

    def begin_post(self, platform: str, content_hash: str) -> PostRecord:
        """Create or fetch a pending post row. Idempotent: a successful post is returned
        as-is so the caller can short-circuit."""
        now = time.time()
        self.conn.execute(
            "INSERT OR IGNORE INTO posts(platform, content_hash, status, created_at, updated_at)"
            " VALUES(?,?,?,?,?)",
            (platform, content_hash, "pending", now, now),
        )
        self.conn.commit()
        rec = self.get_post(platform, content_hash)
        assert rec is not None
        return rec

    def mark_post_success(self, platform: str, content_hash: str, external_id: str) -> None:
        now = time.time()
        self.conn.execute(
            "UPDATE posts SET status='success', external_id=?, error=NULL, updated_at=?"
            " WHERE platform=? AND content_hash=?",
            (external_id, now, platform, content_hash),
        )
        self.conn.commit()

    def mark_post_skipped(self, platform: str, content_hash: str, reason: str) -> None:
        now = time.time()
        self.conn.execute(
            "UPDATE posts SET status='skipped', error=?, updated_at=? "
            "WHERE platform=? AND content_hash=?",
            (reason, now, platform, content_hash),
        )
        self.conn.commit()

    def mark_post_failed(self, platform: str, content_hash: str, error: str,
                         backoff_base: float = 2.0) -> float:
        """Record a failure, increment attempts, schedule exponential backoff.
        Returns the next_attempt_at timestamp."""
        now = time.time()
        rec = self.get_post(platform, content_hash)
        attempts = (rec.attempts if rec else 0) + 1
        delay = min(backoff_base ** attempts, 3600.0)  # cap at 1h
        next_at = now + delay
        self.conn.execute(
            "UPDATE posts SET status='failed', error=?, attempts=?, next_attempt_at=?, updated_at=?"
            " WHERE platform=? AND content_hash=?",
            (error, attempts, next_at, now, platform, content_hash),
        )
        self.conn.commit()
        return next_at

    def is_retry_due(self, platform: str, content_hash: str) -> bool:
        rec = self.get_post(platform, content_hash)
        if rec is None:
            return True
        if rec.status == "success":
            return False
        return time.time() >= rec.next_attempt_at

    # ---- limits & circuit breaker --------------------------------------
    def posts_today(self, platform: str, now: Optional[float] = None) -> int:
        now = now if now is not None else time.time()
        day_start = now - (now % 86400)
        row = self.conn.execute(
            "SELECT COUNT(*) AS c FROM posts WHERE platform=? AND status='success' AND updated_at>=?",
            (platform, day_start),
        ).fetchone()
        return int(row["c"])

    def consecutive_failures(self, platform: str) -> int:
        """Count trailing failures since the last success for a platform."""
        rows = self.conn.execute(
            "SELECT status FROM posts WHERE platform=? AND status IN ('success','failed')"
            " ORDER BY updated_at DESC",
            (platform,),
        ).fetchall()
        count = 0
        for row in rows:
            if row["status"] == "failed":
                count += 1
            else:
                break
        return count
