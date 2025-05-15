"""
Módulo de interfaz gráfica del juego.

Implementa la visualización del juego usando Tkinter con emojis
para representar los elementos del tablero.

Clases:
    GameGUI: Maneja la interfaz gráfica del juego.

"""

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from file_handler import FileHandler  

class GameGUI(tk.Tk):
    """
    Clase principal de la interfaz gráfica del juego.
    
    Atributos:
        game_logic (GameLogic): Instancia de la lógica del juego
        file_handler (FileHandler): Instancia para manejar archivos
        emoji (dict): Mapeo de estados del tablero a emojis
        cells (list): Matriz de widgets Canvas para el tablero
    """
    
    def __init__(self, game_logic):
        """
        Inicializa la interfaz gráfica.
        
        Args:
            game_logic (GameLogic): Instancia de la lógica del juego
        """
        super().__init__()
        self.game_logic = game_logic
        self.file_handler = FileHandler()
        self.title("Virus Spread Challenge")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")
        
        # Configuración de emojis para cada estado del tablero
        self.emoji = {
            0: "⬜",  # Celda libre
            1: "🦠",  # Virus
            2: "🧱"   # Barrera
        }
        
        self.create_widgets()
        self.draw_board()
    
    def create_widgets(self):
        """Crea y organiza todos los widgets de la interfaz."""
        # Frame principal
        self.main_frame = tk.Frame(self, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de información (nivel y turno)
        self.info_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.level_label = tk.Label(self.info_frame, 
                                 text=f"Nivel: {self.game_logic.level}", 
                                 font=("Arial", 12), bg="#f0f0f0")
        self.level_label.pack(side=tk.LEFT)
        
        self.turn_label = tk.Label(self.info_frame, 
                                text=f"Turno: {self.game_logic.turn}", 
                                font=("Arial", 12), bg="#f0f0f0")
        self.turn_label.pack(side=tk.LEFT, padx=20)
        
        # Frame del tablero
        self.board_frame = tk.Frame(self.main_frame, bg="#333")
        self.board_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de controles
        self.control_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.control_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botones de control
        self.spread_button = tk.Button(self.control_frame, 
                                    text="Propagar Virus", 
                                    command=self.spread_virus)
        self.spread_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = tk.Button(self.control_frame, 
                                  text="Guardar Partida", 
                                  command=self.save_game)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.load_button = tk.Button(self.control_frame, 
                                  text="Cargar Partida", 
                                  command=self.load_game)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        self.next_level_button = tk.Button(self.control_frame, 
                                        text="Siguiente Nivel", 
                                        command=self.next_level,
                                        state=tk.DISABLED)
        self.next_level_button.pack(side=tk.RIGHT, padx=5)
        
        # Inicializar celdas del tablero
        self.cells = []
        self.create_board_cells()
    
    def create_board_cells(self):
        """Crea las celdas del tablero como widgets Canvas."""
        size = self.game_logic.size
        cell_size = min(500 // size, 50)  # Ajustar tamaño según dimensiones
        
        for i in range(size):
            row = []
            for j in range(size):
                cell = tk.Canvas(self.board_frame, 
                               width=cell_size, 
                               height=cell_size,
                               bg="white",
                               highlightthickness=1,
                               highlightbackground="black")
                cell.grid(row=i, column=j, padx=1, pady=1)
                cell.bind("<Button-1>", lambda e, x=i, y=j: self.handle_click(x, y))
                row.append(cell)
            self.cells.append(row)
    
    def draw_board(self):
        """Actualiza la visualización del tablero."""
        board = self.game_logic.get_board_state()
        
        for i in range(self.game_logic.size):
            for j in range(self.game_logic.size):
                cell_value = board[i][j]
                emoji = self.emoji[cell_value]
                self.cells[i][j].delete("all")
                self.cells[i][j].create_text(
                    15, 15,  # Posición centrada
                    text=emoji,
                    font=("Arial", 20),
                    fill="black" if cell_value == 2 else "red" if cell_value == 1 else "gray"
                )
        
        # Actualizar información de nivel y turno
        self.level_label.config(text=f"Nivel: {self.game_logic.level}")
        self.turn_label.config(text=f"Turno: {self.game_logic.turn}")
        
        # Manejar estado del juego
        if self.game_logic.game_over:
            self.spread_button.config(state=tk.DISABLED)
            if self.game_logic.winner == "player":
                self.next_level_button.config(state=tk.NORMAL)
                messagebox.showinfo("¡Ganaste!", f"¡Has contenido el virus en el nivel {self.game_logic.level}!")
            else:
                self.next_level_button.config(state=tk.DISABLED)
                messagebox.showinfo("Perdiste", "El virus ha tomado todo el territorio. ¡Mejor suerte la próxima vez!")
        else:
            self.spread_button.config(state=tk.NORMAL)
            self.next_level_button.config(state=tk.DISABLED)
    
    def handle_click(self, x, y):
        """Maneja el clic del usuario en una celda del tablero."""
        if self.game_logic.game_over:
            return
        
        if self.game_logic.place_barrier(x, y):
            self.draw_board()
        else:
            messagebox.showwarning("Movimiento inválido", "No puedes colocar una barrera allí.")
    
    def spread_virus(self):
        """Propaga el virus y actualiza la interfaz."""
        self.game_logic.spread_virus()
        self.draw_board()
    
    def next_level(self):
        """Avanza al siguiente nivel si es posible."""
        if self.game_logic.next_level():
            self.draw_board()
    
    def save_game(self):
        """Guarda la partida actual en un archivo."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".vsc",
            filetypes=[("Virus Spread Challenge", "*.vsc")]
        )
        
        if filename:
            game_name = simpledialog.askstring(
                "Nombre de la partida",
                "Ingrese un nombre para esta partida:"
            )
            
            if game_name is None:  # Usuario canceló
                return
            
            if self.file_handler.save_game(self.game_logic, filename):
                messagebox.showinfo("Partida guardada", "La partida se ha guardado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo guardar la partida.")
    
    def load_game(self):
        """Carga una partida desde un archivo."""
        filename = filedialog.askopenfilename(
            filetypes=[("Virus Spread Challenge", "*.vsc")]
        )
        
        if filename:
            board, level, virus_positions = self.file_handler.load_game(filename)
            if board is not None:
                self.game_logic.set_board_state(board, level, virus_positions)
                if self.game_logic.size != len(self.cells):
                    self.create_board_cells()
                self.draw_board()
                messagebox.showinfo("Partida cargada", "La partida se ha cargado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo cargar la partida.")