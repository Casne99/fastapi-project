import sys

import bcrypt
from sqlalchemy import create_engine, text

from env_test import DATABASE_URL


def insert_user(username: str, password: str):
    engine = create_engine(DATABASE_URL)
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with engine.connect() as conn:
        conn.execute(
            text(
                'INSERT INTO credentials ("user", password) VALUES (:user, :password) ON CONFLICT ("user") DO NOTHING'),
            {"user": username, "password": hashed.decode()}
        )
        conn.commit()
    print(f"Utente '{username}' inserito.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python insert_test_user.py <username> <password>")
        sys.exit(1)
    insert_user(sys.argv[1], sys.argv[2])
