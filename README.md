# 3Nraya
Desarrollo del backend de una pequeña aplicación que permite jugar al tres en ralla a través de una APIRest
# Miguel Gómez Vázquez 

## Instalación
1. Abriendo una Consola y estando en la carpeta raiz del proyecto escribimos lo siguiente: pip install -r requeriments.txt .

## Ejecución

1. Lo primero que haremos será encender el servidor, para ello estando en la carpeta raiz del proyecto escribimos lo siguiente por consola: python app.py
2. Lo segundo que haremos será abrir una consola (CMD) ya que será desde ahi desde donde controlaremos la aplicación.

### Empezar una partida
1. deberemos escribir por la consola <br>
 curl http://localhost:5000/start/player1/player2 <br>
 siendo player1 y player2 los nombres de las personas que van a jugar. <br>
 Una vez hecho esto la partida ya ha empezado y no se acabará hasta que termine o se vuelva a ejecutar el mismo código.<br>
 2. Para empezar con los movimientos deberemos escribir el siguiente código:<br>
 curl http://localhost:5000/play/movimiento <br>
 siendo movimiento un numero entre el 0-8, que representan las distintas casillas del tablero, sería tal que así:<br>

     0 | 1 | 2 <br>
     --------- <br>
     3 | 4 | 5 <br>
     --------- <br>
     6 | 7 | 8 <br>
<br>
Por lo tanto el numero que pongas será la casilla que marque el jugador.<br>
Automaticamente después será turno del otro jugador y se realizará la misma mecanica hasta que se acabe la partida.
 
### Saber los jugadores
Para saber todos los jugadores que alguna vez han jugado realizaremos esta peticion:<br>
curl http://localhost:5000/jugadores
### Saber las partidas
Para saber todos las partidas que se han jugado realizaremos esta peticion:<br>
curl http://localhost:5000/partidas
### Saber el numero de partidas ganadas
Para saber el número de partidas ganadas por un jugador en específico haremos esta petición:<br>
curl http://localhost:5000/partidas_ganadas/PLAYER <br>
siendo PLAYER el jugador del que queremos saber
### Saber record en enfrentamientos
Para saber el historico de enfrentamientos y sus resultados de dos jugadores haremos esta petición:<br>
curl http://localhost:5000/record_partidas/PLAYER1/PLAYER2 <br>
