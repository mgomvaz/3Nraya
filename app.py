from flask import Flask, jsonify
from tic_tac_toe import TicTacToe
import sqlite3
import subprocess



app = Flask(__name__)
game = TicTacToe()
app.config['DATABASE'] = 'data.db'
subprocess.run(['python', 'data.py'])

p1=None
p2=None
#p1 van a ser las X y p2 van a ser  las O



#endpoint que nos devuelve todos los jugadores que han jugado
@app.route('/jugadores', methods=['GET'])
def jugadores():   
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jugadores')
    registros = cursor.fetchall()
    conn.close()
    return registros


#endpoint que nos devuelve todas las partidas que se han jugado
@app.route('/partidas', methods=['GET'])
def partidas():   
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM partidas')
    registros = cursor.fetchall()
    conn.close()
    return registros


#endpoint que nos devuelve el numero de partidas ganadas por un jugador en concreto
@app.route('/partidas_ganadas/<string:player>', methods=['GET'])
def partidas_ganadas(player):   
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    consulta_sql = f"SELECT COUNT(*) FROM partidas WHERE ganador = ?;"
    cursor.execute(consulta_sql, (player,))
    partidas_ganadas = cursor.fetchone()[0]
    res=(f"{player} ha ganado {partidas_ganadas} partidas.")
    conn.close()
    return res

#endpoint que dado dos nombres de dos jugadores te da su historial de partidas
@app.route('/record_partidas/<string:player1>/<string:player2>', methods=['GET'])
def record_partidas(player1,player2):   
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    jugador1 = player1
    jugador2 = player2
    # Consulta SQL
    consulta_sql = """
    SELECT
    COUNT(*) AS total_partidas,
    (SELECT COUNT(*) FROM partidas WHERE (jugador1 = ? AND jugador2 = ? AND ganador = ?) OR (jugador1 = ? AND jugador2 = ? AND ganador = ?)) AS enfrentamientos,
    (SELECT COUNT(*) FROM partidas WHERE (jugador1 = ? AND jugador2 = ? AND ganador = ?)) AS victorias_jugador1,
    (SELECT COUNT(*) FROM partidas WHERE (jugador1 = ? AND jugador2 = ? AND ganador = ?)) AS victorias_jugador2
    FROM partidas
    WHERE (jugador1 = ? AND jugador2 = ?) OR (jugador1 = ? AND jugador2 = ?);
    """
    # Ejecutar la consulta SQL
    cursor.execute(consulta_sql, (jugador1, jugador2, jugador1, jugador2, jugador1, jugador2, jugador1, jugador2, jugador1, jugador2, jugador2, jugador1, jugador1, jugador2, jugador2, jugador1))
    # Obtener el resultado
    resultado = cursor.fetchone()
    # Cerrar la conexión con la base de datos
    conn.close()
    # Mostrar los resultados
    total_partidas, enfrentamientos, victorias_jugador1, victorias_jugador2 = resultado
    r1=(f"Total de partidas entre {jugador1} y {jugador2}: {total_partidas}")
    r2=(f"Enfrentamientos directos: {enfrentamientos}")
    r3=(f"Victorias de {jugador1}: {victorias_jugador1}")
    r4=(f"Victorias de {jugador2}: {victorias_jugador2}")
    return r1+'\n'+'\n'+r2+'\n'+r3+'\n'+r4


#endpoint que sirve para iniciar una nueva partida
@app.route('/start/<string:player1>/<string:player2>', methods=['GET'])
def start_game(player1,player2):
    global game,p1,p2
    p1=player1
    p2=player2
    nombres=[player1,player2]
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    for i in nombres:
        try:
            # Intentar insertar el nombre en la tabla
            cursor.execute("INSERT INTO jugadores (nombre) VALUES (?)", (i,))
            conn.commit()
            print("El jugador se ha añadido correctamente.")
        except sqlite3.IntegrityError:
            # Si ocurre un error de integridad, significa que el nombre ya existe
            print("Ese nombre ya está ocupado.")
    game = TicTacToe()
    current_player = game.current_player
    response = 'Juego reiniciado \nTurno del jugador '+current_player + '\n'+p1+' será las X'+ '\n'+p2+' será las O'
    conn.close()
    return response, 200


#endpoint que usaremos para jugar la partida
@app.route('/play/<movimiento>', methods=['GET'])
def play_game(movimiento):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    global game
    try:
        move = int(movimiento)
    except (ValueError, TypeError):
        return jsonify({'error': 'Movimiento inválido'}), 400
    if 0 <= move < 9:
        current_player = game.current_player
        if game.make_move(move):
            winner = game.check_winner()
            if winner:
                ganador=p1
                if winner=='O':
                    ganador=p2
                cursor.execute("INSERT INTO partidas (jugador1,jugador2, ganador) VALUES (?, ?, ?)", (p1,p2,ganador))
                conn.commit()
                conn.close()
                return jsonify({'message': f'Jugador {ganador} gana el juego'}), 200
            formatted_board = format_board(game.board)
            response = f"Turno del jugador {current_player}\n{formatted_board}"
            #return jsonify({'message': response}), 200
            return response, 200
        else:
            return jsonify({'error': 'Movimiento inválido'}), 400
    else:
        return jsonify({'error': 'Movimiento fuera de rango'}), 400

def format_board(board):
    formatted = ""
    for i in range(0, 9, 3):
        formatted += board[i] + ' | ' + board[i + 1] + ' | ' + board[i + 2] + '\n'
        if i < 6:
            formatted += '---------' + "\n"
    return formatted


if __name__ == '__main__':
    app.run(debug=True)


#mañana tengo que explicar para que sirve cada cosa, hacer los test unitarios, poner el rqeuriments.txt, el readme.me
#quitar los endpoints que no hacen falta, subirlo a github