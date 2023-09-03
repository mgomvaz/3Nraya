import sqlite3

# Configura la conexión a la base de datos
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Crea la tabla de jugadores
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jugadores (
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE NOT NULL
    )
''')

# Crea la tabla de partidas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS partidas (
        id INTEGER PRIMARY KEY,
        jugador1 TEXT UNIQUE NOT NULL,
        jugador2 TEXT UNIQUE NOT NULL,
        ganador TEXT UNIQUE NOT NULL
    )
''')


# Guarda los cambios en la base de datos
conn.commit()

# Cierra la conexión a la base de datos
conn.close()
