import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from . import config


def now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


class AppDatabase:
    """SQLite-first database adapter with optional Supabase REST backend."""

    def __init__(self) -> None:
        self.backend = config.DB_BACKEND
        if self.backend == "supabase" and config.SUPABASE_URL and config.SUPABASE_SERVICE_ROLE_KEY:
            self.mode = "supabase"
        else:
            self.mode = "sqlite"
            self.path = Path(config.SQLITE_PATH)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._ensure_sqlite()

    # ---------- SQLite ----------
    def _conn(self):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        return con

    def _ensure_sqlite(self) -> None:
        with self._conn() as con:
            con.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    display_name TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS profiles (
                    user_id TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );
                CREATE TABLE IF NOT EXISTS medications (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    dose TEXT NOT NULL,
                    times TEXT NOT NULL,
                    days TEXT NOT NULL,
                    instructions TEXT,
                    inventory REAL DEFAULT 0,
                    units_per_dose REAL DEFAULT 1,
                    refill_threshold REAL DEFAULT 5,
                    active INTEGER DEFAULT 1,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS dose_logs (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    medication_id TEXT,
                    scheduled_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    note TEXT,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS health_logs (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    data TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS reminder_sent (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    medication_id TEXT NOT NULL,
                    reminder_key TEXT NOT NULL,
                    channel TEXT NOT NULL,
                    sent_at TEXT NOT NULL,
                    UNIQUE(user_id, medication_id, reminder_key, channel)
                );
                """
            )

    # ---------- Supabase REST ----------
    def _headers(self) -> Dict[str, str]:
        key = config.SUPABASE_SERVICE_ROLE_KEY or config.SUPABASE_ANON_KEY
        return {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

    def _url(self, table: str) -> str:
        return f"{config.SUPABASE_URL}/rest/v1/{table}"

    def _sb_select(self, table: str, params: Dict[str, str]) -> List[Dict[str, Any]]:
        r = requests.get(self._url(table), headers=self._headers(), params=params, timeout=25)
        r.raise_for_status()
        return r.json()

    def _sb_insert(self, table: str, row: Dict[str, Any]) -> Dict[str, Any]:
        r = requests.post(self._url(table), headers=self._headers(), data=json.dumps(row), timeout=25)
        r.raise_for_status()
        data = r.json()
        return data[0] if isinstance(data, list) and data else row

    def _sb_update(self, table: str, row_id: str, patch: Dict[str, Any]) -> None:
        r = requests.patch(self._url(table), headers=self._headers(), params={"id": f"eq.{row_id}"}, data=json.dumps(patch), timeout=25)
        r.raise_for_status()

    def _sb_delete(self, table: str, row_id: str) -> None:
        r = requests.delete(self._url(table), headers=self._headers(), params={"id": f"eq.{row_id}"}, timeout=25)
        r.raise_for_status()

    # ---------- Users/Auth ----------
    def create_user(self, email: str, display_name: str, password_hash: str) -> Dict[str, Any]:
        row = {"id": str(uuid.uuid4()), "email": email.lower().strip(), "display_name": display_name.strip() or email, "password_hash": password_hash, "created_at": now_iso()}
        if self.mode == "supabase":
            return self._sb_insert("users", row)
        with self._conn() as con:
            con.execute("INSERT INTO users VALUES (:id,:email,:display_name,:password_hash,:created_at)", row)
        return row

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        email = email.lower().strip()
        if self.mode == "supabase":
            rows = self._sb_select("users", {"email": f"eq.{email}", "select": "*"})
            return rows[0] if rows else None
        with self._conn() as con:
            row = con.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
            return dict(row) if row else None

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        if self.mode == "supabase":
            rows = self._sb_select("users", {"id": f"eq.{user_id}", "select": "*"})
            return rows[0] if rows else None
        with self._conn() as con:
            row = con.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
            return dict(row) if row else None

    # ---------- Profile JSON ----------
    def load_profile(self, user_id: str) -> Dict[str, Any]:
        if self.mode == "supabase":
            rows = self._sb_select("profiles", {"user_id": f"eq.{user_id}", "select": "*"})
            if rows:
                data = rows[0].get("data")
                return data if isinstance(data, dict) else json.loads(data or "{}")
            return {}
        with self._conn() as con:
            row = con.execute("SELECT data FROM profiles WHERE user_id=?", (user_id,)).fetchone()
            return json.loads(row["data"]) if row else {}

    def save_profile(self, user_id: str, data: Dict[str, Any]) -> None:
        updated = now_iso()
        if self.mode == "supabase":
            rows = self._sb_select("profiles", {"user_id": f"eq.{user_id}", "select": "user_id"})
            if rows:
                r = requests.patch(self._url("profiles"), headers=self._headers(), params={"user_id": f"eq.{user_id}"}, data=json.dumps({"data": data, "updated_at": updated}), timeout=25)
                r.raise_for_status()
            else:
                self._sb_insert("profiles", {"user_id": user_id, "data": data, "updated_at": updated})
            return
        with self._conn() as con:
            con.execute(
                "INSERT INTO profiles(user_id,data,updated_at) VALUES(?,?,?) ON CONFLICT(user_id) DO UPDATE SET data=excluded.data, updated_at=excluded.updated_at",
                (user_id, json.dumps(data, ensure_ascii=False), updated),
            )

    # ---------- Medications ----------
    def list_medications(self, user_id: str, active_only: bool = True) -> List[Dict[str, Any]]:
        if self.mode == "supabase":
            params = {"user_id": f"eq.{user_id}", "select": "*", "order": "created_at.desc"}
            if active_only:
                params["active"] = "eq.true"
            rows = self._sb_select("medications", params)
        else:
            q = "SELECT * FROM medications WHERE user_id=?" + (" AND active=1" if active_only else "") + " ORDER BY created_at DESC"
            with self._conn() as con:
                rows = [dict(r) for r in con.execute(q, (user_id,)).fetchall()]
        for r in rows:
            for key in ("times", "days"):
                if isinstance(r.get(key), str):
                    try:
                        r[key] = json.loads(r[key])
                    except Exception:
                        r[key] = [x.strip() for x in r.get(key, "").split(",") if x.strip()]
        return rows

    def list_all_active_medications(self) -> List[Dict[str, Any]]:
        if self.mode == "supabase":
            rows = self._sb_select("medications", {"active": "eq.true", "select": "*"})
        else:
            with self._conn() as con:
                rows = [dict(r) for r in con.execute("SELECT * FROM medications WHERE active=1").fetchall()]
        for r in rows:
            for key in ("times", "days"):
                if isinstance(r.get(key), str):
                    try:
                        r[key] = json.loads(r[key])
                    except Exception:
                        r[key] = []
        return rows

    def add_medication(self, user_id: str, med: Dict[str, Any]) -> Dict[str, Any]:
        row = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "name": med["name"],
            "dose": med["dose"],
            "times": med.get("times", []),
            "days": med.get("days", ["Tất cả"]),
            "instructions": med.get("instructions", ""),
            "inventory": float(med.get("inventory", 0) or 0),
            "units_per_dose": float(med.get("units_per_dose", 1) or 1),
            "refill_threshold": float(med.get("refill_threshold", 5) or 5),
            "active": True,
            "created_at": now_iso(),
        }
        if self.mode == "supabase":
            return self._sb_insert("medications", row)
        dbrow = row.copy(); dbrow["times"] = json.dumps(row["times"], ensure_ascii=False); dbrow["days"] = json.dumps(row["days"], ensure_ascii=False); dbrow["active"] = 1
        with self._conn() as con:
            con.execute("""
                INSERT INTO medications(id,user_id,name,dose,times,days,instructions,inventory,units_per_dose,refill_threshold,active,created_at)
                VALUES(:id,:user_id,:name,:dose,:times,:days,:instructions,:inventory,:units_per_dose,:refill_threshold,:active,:created_at)
            """, dbrow)
        return row

    def update_medication(self, med_id: str, patch: Dict[str, Any]) -> None:
        if self.mode == "supabase":
            self._sb_update("medications", med_id, patch)
            return
        patch = patch.copy()
        if "times" in patch: patch["times"] = json.dumps(patch["times"], ensure_ascii=False)
        if "days" in patch: patch["days"] = json.dumps(patch["days"], ensure_ascii=False)
        if "active" in patch: patch["active"] = int(bool(patch["active"]))
        keys = list(patch.keys())
        if not keys: return
        sql = "UPDATE medications SET " + ",".join([f"{k}=?" for k in keys]) + " WHERE id=?"
        with self._conn() as con:
            con.execute(sql, [patch[k] for k in keys] + [med_id])

    def log_dose(self, user_id: str, medication_id: str, scheduled_at: str, status: str, note: str = "") -> None:
        row = {"id": str(uuid.uuid4()), "user_id": user_id, "medication_id": medication_id, "scheduled_at": scheduled_at, "status": status, "note": note, "created_at": now_iso()}
        if self.mode == "supabase":
            self._sb_insert("dose_logs", row); return
        with self._conn() as con:
            con.execute("INSERT INTO dose_logs VALUES(:id,:user_id,:medication_id,:scheduled_at,:status,:note,:created_at)", row)

    def list_dose_logs(self, user_id: str, limit: int = 200) -> List[Dict[str, Any]]:
        if self.mode == "supabase":
            return self._sb_select("dose_logs", {"user_id": f"eq.{user_id}", "select": "*", "order": "created_at.desc", "limit": str(limit)})
        with self._conn() as con:
            return [dict(r) for r in con.execute("SELECT * FROM dose_logs WHERE user_id=? ORDER BY created_at DESC LIMIT ?", (user_id, limit)).fetchall()]

    def add_health_log(self, user_id: str, data: Dict[str, Any]) -> None:
        row = {"id": str(uuid.uuid4()), "user_id": user_id, "data": data, "created_at": now_iso()}
        if self.mode == "supabase":
            self._sb_insert("health_logs", row); return
        dbrow = row.copy(); dbrow["data"] = json.dumps(data, ensure_ascii=False)
        with self._conn() as con:
            con.execute("INSERT INTO health_logs VALUES(:id,:user_id,:data,:created_at)", dbrow)

    def list_health_logs(self, user_id: str, limit: int = 200) -> List[Dict[str, Any]]:
        if self.mode == "supabase":
            rows = self._sb_select("health_logs", {"user_id": f"eq.{user_id}", "select": "*", "order": "created_at.desc", "limit": str(limit)})
        else:
            with self._conn() as con:
                rows = [dict(r) for r in con.execute("SELECT * FROM health_logs WHERE user_id=? ORDER BY created_at DESC LIMIT ?", (user_id, limit)).fetchall()]
        for r in rows:
            if isinstance(r.get("data"), str):
                r["data"] = json.loads(r["data"])
        return rows

    def reminder_was_sent(self, user_id: str, medication_id: str, reminder_key: str, channel: str) -> bool:
        if self.mode == "supabase":
            rows = self._sb_select("reminder_sent", {"user_id": f"eq.{user_id}", "medication_id": f"eq.{medication_id}", "reminder_key": f"eq.{reminder_key}", "channel": f"eq.{channel}", "select": "id"})
            return bool(rows)
        with self._conn() as con:
            row = con.execute("SELECT id FROM reminder_sent WHERE user_id=? AND medication_id=? AND reminder_key=? AND channel=?", (user_id, medication_id, reminder_key, channel)).fetchone()
            return bool(row)

    def mark_reminder_sent(self, user_id: str, medication_id: str, reminder_key: str, channel: str) -> None:
        if self.reminder_was_sent(user_id, medication_id, reminder_key, channel):
            return
        row = {"id": str(uuid.uuid4()), "user_id": user_id, "medication_id": medication_id, "reminder_key": reminder_key, "channel": channel, "sent_at": now_iso()}
        if self.mode == "supabase":
            self._sb_insert("reminder_sent", row); return
        with self._conn() as con:
            con.execute("INSERT OR IGNORE INTO reminder_sent VALUES(:id,:user_id,:medication_id,:reminder_key,:channel,:sent_at)", row)

    def export_user_data(self, user_id: str) -> Dict[str, Any]:
        return {
            "profile": self.load_profile(user_id),
            "medications": self.list_medications(user_id, active_only=False),
            "dose_logs": self.list_dose_logs(user_id, 1000),
            "health_logs": self.list_health_logs(user_id, 1000),
            "exported_at": now_iso(),
            "backend": self.mode,
        }


_db: Optional[AppDatabase] = None


def get_db() -> AppDatabase:
    global _db
    if _db is None:
        _db = AppDatabase()
    return _db
