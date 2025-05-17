import struct
from game_logic import GameLogic

class FileManager:
    @staticmethod
    def save_game(game, filename):
        try:
            with open(f"{filename}.bin", "wb") as f:
                f.write(struct.pack(">H", game.size))
                f.write(struct.pack("B", game.level))
                f.write(struct.pack("B", game.barriers_remaining))
                
                max_num = 3**game.size - 1
                bytes_per_row = (max_num.bit_length() + 7) // 8
                
                for row in game.board:
                    num = 0
                    for i, val in enumerate(row):
                        num += val * (3 ** (game.size - 1 - i))
                    
                    hex_num = format(num, 'X')
                    hex_padded = hex_num.zfill(bytes_per_row * 2)
                    
                    if len(hex_padded) % 2 != 0:
                        hex_padded = '0' + hex_padded
                    
                    f.write(bytes.fromhex(hex_padded))
            return True
        except Exception as e:
            print(f"Error saving: {str(e)}")
            return False
    
    @staticmethod
    def load_game(filename):
        try:
            with open(f"{filename}.bin", "rb") as f:
                size = struct.unpack(">H", f.read(2))[0]
                level = struct.unpack("B", f.read(1))[0]
                barriers = struct.unpack("B", f.read(1))[0]
                
                max_num = 3**size - 1
                bytes_per_row = (max_num.bit_length() + 7) // 8
                
                game = GameLogic(size)
                game.level = level
                game.barriers_remaining = barriers
                game.board = [[0]*size for _ in range(size)]
                
                for i in range(size):
                    hex_bytes = f.read(bytes_per_row)
                    hex_str = hex_bytes.hex().upper()
                    num = int(hex_str, 16)
                    
                    for j in range(size-1, -1, -1):
                        game.board[i][j] = num % 3
                        num = num // 3
                
                return game
        except Exception as e:
            print(f"Error loading: {str(e)}")
            return None