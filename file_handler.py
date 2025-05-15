"""
Módulo para manejo de archivos binarios del juego.

Implementa la codificación/decodificación del estado del juego
para guardar y cargar partidas según el formato especificado.

Clases:
    FileHandler: Maneja operaciones de lectura/escritura de partidas.

Autor: [Tu nombre]
Fecha: [Fecha]
"""

import os

class FileHandler:
    """
    Clase para manejar el guardado y carga de partidas en archivos binarios.
    
    Métodos:
        save_game: Guarda el estado actual del juego en un archivo.
        load_game: Carga un juego desde un archivo guardado.
        list_saved_games: Lista todas las partidas guardadas.
    """
    
    def __init__(self):
        """Inicializa el manejador de archivos."""
        pass
    
    def save_game(self, game_logic, filename):
        """
        Guarda el estado del juego en un archivo binario.
        
        Args:
            game_logic (GameLogic): Instancia del juego a guardar
            filename (str): Ruta del archivo de destino
            
        Returns:
            bool: True si se guardó correctamente, False si hubo error
        """
        try:
            with open(filename, 'wb') as file:
                # Escribir tamaño del tablero (2 bytes)
                size = game_logic.size
                file.write(size.to_bytes(2, byteorder='big'))
                
                # Escribir nivel actual (1 byte)
                level = game_logic.level
                file.write(level.to_bytes(1, byteorder='big'))
                
                # Escribir estado del tablero
                for row in game_logic.board:
                    base3_str = ''.join(str(cell) for cell in row)
                    base3_num = int(base3_str, 3)
                    
                    hex_str = format(base3_num, 'x')
                    if len(hex_str) % 2 != 0:
                        hex_str = '0' + hex_str
                    file.write(bytes.fromhex(hex_str))
            
            return True
        except Exception as e:
            print(f"Error al guardar el juego: {e}")
            return False
    
    def load_game(self, filename):
        """
        Carga un juego desde un archivo binario.
        
        Args:
            filename (str): Ruta del archivo a cargar
            
        Returns:
            tuple: (board, level, virus_positions) o (None, None, None) si hay error
        """
        try:
            with open(filename, 'rb') as file:
                # Leer tamaño del tablero (2 bytes)
                size = int.from_bytes(file.read(2), byteorder='big')
                
                # Leer nivel actual (1 byte)
                level = int.from_bytes(file.read(1), byteorder='big')
                
                # Leer y decodificar el tablero
                board = [[0 for _ in range(size)] for _ in range(size)]
                virus_positions = []
                
                for i in range(size):
                    max_base3 = 3**size - 1
                    max_hex_len = len(format(max_base3, 'x'))
                    bytes_to_read = (max_hex_len + 1) // 2
                    
                    hex_data = file.read(bytes_to_read).hex()
                    base3_num = int(hex_data, 16)
                    base3_str = self._base3(base3_num, size)
                    
                    for j in range(size):
                        cell = int(base3_str[j])
                        board[i][j] = cell
                        if cell == 1:
                            virus_positions.append((i, j))
                
                return board, level, virus_positions
        except Exception as e:
            print(f"Error al cargar el juego: {e}")
            return None, None, None
    
    def _base3(self, n, length):
        """
        Convierte un número a base3 con padding de ceros.
        
        Args:
            n (int): Número a convertir
            length (int): Longitud deseada del string resultante
            
        Returns:
            str: Representación en base3 con ceros a la izquierda
        """
        digits = []
        if n == 0:
            return '0' * length
        while n > 0:
            digits.append(str(n % 3))
            n = n // 3
        num_str = ''.join(reversed(digits))
        return num_str.zfill(length)
    
    def list_saved_games(self):
        """
        Lista todos los juegos guardados en el directorio actual.
        
        Returns:
            list: Lista de nombres de archivos .vsc
        """
        games = []
        for file in os.listdir('.'):
            if file.endswith('.vsc'):
                games.append(file)
        return games