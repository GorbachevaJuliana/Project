import sqlite3
conn = sqlite3.connect('project.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "tournament" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" VARCHAR(50) NOT NULL,
    "date" DATETIME NOT NULL,
    "place" TEXT NOT NULL,
    "players" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "games" TEXT,
    FOREIGN KEY("players") REFERENCES "player"("name"),
    FOREIGN KEY("games") REFERENCES "game"("id")
);
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS "player" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" VARCHAR(100) UNIQUE NOT NULL,
    "rating" integer NOT NULL,
    "age" integer,
    "country" TEXT NOT NULL
);
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS "game" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "date" TEXT NOT NULL,
    "player1" VARCHAR(100) NOT NULL,
    "player2" VARCHAR(100) NOT NULL,
    "favorite" VARCHAR(100) NOT NULL,
    "winner" TEXT NOT NULL,
    "result" TEXT NOT NULL,
    FOREIGN KEY("player1") REFERENCES "player"("name"),
    FOREIGN KEY("player2") REFERENCES "player"("name"),
    FOREIGN KEY("favorite") REFERENCES "player"("name")
);
''')