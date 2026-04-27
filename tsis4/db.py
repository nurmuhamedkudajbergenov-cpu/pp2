import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG

CREATE_PLAYERS = """
CREATE TABLE IF NOT EXISTS players (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);
"""

CREATE_SESSIONS = """
CREATE TABLE IF NOT EXISTS game_sessions (
    id            SERIAL PRIMARY KEY,
    player_id     INTEGER REFERENCES players(id),
    score         INTEGER   NOT NULL,
    level_reached INTEGER   NOT NULL,
    played_at     TIMESTAMP DEFAULT NOW()
);
"""


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    """Create tables if they don't exist."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_PLAYERS)
                cur.execute(CREATE_SESSIONS)
            conn.commit()
        return True
    except Exception as e:
        print(f"[DB] init error: {e}")
        return False


def upsert_player(username: str) -> int | None:
    """Return player id, inserting if new."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO players (username) VALUES (%s) "
                    "ON CONFLICT (username) DO UPDATE SET username=EXCLUDED.username "
                    "RETURNING id",
                    (username,)
                )
                row = cur.fetchone()
            conn.commit()
        return row[0] if row else None
    except Exception as e:
        print(f"[DB] upsert_player error: {e}")
        return None


def save_session(username: str, score: int, level: int):
    """Save a game result."""
    try:
        player_id = upsert_player(username)
        if player_id is None:
            return
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO game_sessions (player_id, score, level_reached) "
                    "VALUES (%s, %s, %s)",
                    (player_id, score, level)
                )
            conn.commit()
    except Exception as e:
        print(f"[DB] save_session error: {e}")


def get_top10() -> list[dict]:
    """Fetch top 10 all-time scores."""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT p.username, gs.score, gs.level_reached,
                           TO_CHAR(gs.played_at, 'DD Mon') AS date
                    FROM game_sessions gs
                    JOIN players p ON p.id = gs.player_id
                    ORDER BY gs.score DESC
                    LIMIT 10
                """)
                return [dict(r) for r in cur.fetchall()]
    except Exception as e:
        print(f"[DB] get_top10 error: {e}")
        return []


def get_personal_best(username: str) -> int:
    """Return the player's highest score ever, or 0."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COALESCE(MAX(gs.score), 0)
                    FROM game_sessions gs
                    JOIN players p ON p.id = gs.player_id
                    WHERE p.username = %s
                """, (username,))
                row = cur.fetchone()
        return row[0] if row else 0
    except Exception as e:
        print(f"[DB] get_personal_best error: {e}")
        return 0
