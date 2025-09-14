import psycopg2
import os

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "postgres"),
    port=os.getenv("POSTGRES_PORT", 5432),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "mysecretpassword"),
    dbname=os.getenv("POSTGRES_DB", "postgres")
)

cur = conn.cursor()

class Player:
    def __init__(self, name, nationality, current_club, year_of_birth, player_id=None):
        self.id = player_id
        self.name = name
        self.nationality = nationality
        self.current_club = current_club
        self.year_of_birth = year_of_birth

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "nationality": self.nationality,
            "current_club": self.current_club,
            "year_of_birth": self.year_of_birth
        }

    @classmethod
    def save(cls, player):
        cur.execute("""
            INSERT INTO players (name, nationality, current_club, year_of_birth)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (player.name, player.nationality, player.current_club, player.year_of_birth))
        player_id = cur.fetchone()[0]
        conn.commit()
        return player_id

    @classmethod
    def get_all(cls):
        cur.execute("SELECT id, name, nationality, current_club, year_of_birth FROM players;")
        rows = cur.fetchall()
        return [cls(row[1], row[2], row[3], row[4], row[0]) for row in rows]

    @classmethod
    def get_by_parameters(cls, country=None, club=None, year_gt=None, year_lt=None):
        query = "SELECT id, name, nationality, current_club, year_of_birth FROM players WHERE 1=1"
        params = []

        if country:
            query += " AND LOWER(nationality) = LOWER(%s)"
            params.append(country)

        if club:
            query += " AND LOWER(current_club) = LOWER(%s)"
            params.append(club)

        if year_gt is not None:
            query += " AND year_of_birth > %s"
            params.append(year_gt)

        if year_lt is not None:
            query += " AND year_of_birth < %s"
            params.append(year_lt)

        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        return [cls(row[1], row[2], row[3], row[4], row[0]) for row in rows]
