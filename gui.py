import tkinter as tk
"""
Interfaz gráfica para el juego de Virus usando Tkinter.
Permite al usuario interactuar con el juego, colocar barreras, avanzar turnos,
guardar y cargar partidas, y visualizar el estado del tablero.
"""
"""
    Inicializa la interfaz gráfica, crea el menú y comienza un nuevo juego.
    Args:
        master (tk.Tk): Ventana principal de Tkinter.
    """
"""
    Inicializa la barra de menú con las opciones de Nuevo Juego, Guardar y Cargar.
    """
"""
    Inicia un nuevo juego solicitando al usuario el tamaño del tablero.
    Reinicia el estado del juego y actualiza la interfaz.
    """
"""
    Crea los botones del tablero en la interfaz gráfica según el tamaño actual del juego.
    También agrega el botón para avanzar al siguiente turno.
    """
"""
    Actualiza la visualización del tablero y la información en la ventana principal,
    mostrando el estado de cada celda y los datos del juego.
    """
"""
    Maneja el evento de clic en una celda del tablero.
    Permite colocar una barrera si es posible y muestra mensajes de error o derrota según corresponda.
    Args:
        i (int): Fila de la celda.
        j (int): Columna de la celda.
    """
"""
    Avanza al siguiente turno del juego.
    Propaga el virus, verifica condiciones de victoria o derrota y actualiza la interfaz.
    """
"""
    Maneja la lógica cuando el jugador gana un nivel o el juego completo.
    Muestra mensajes de victoria y avanza de nivel o reinicia el juego.
    """
"""
    Solicita al usuario un nombre de archivo y guarda el estado actual del juego.
    Muestra un mensaje de éxito si la operación es exitosa.
    """
"""
    Solicita al usuario un nombre de archivo y carga una partida guardada.
    Actualiza la interfaz con el estado cargado y muestra un mensaje de éxito.
    """
from tkinter import messagebox, simpledialog
from game_logic import GameLogic
from file_manager import FileManager

class VirusGameGUI:
    def __init__(self, master):
        self.master = master
        self.game = None
        self.buttons = []
        self.init_menu()
        self.start_new_game()
        self.master.resizable(False, False)
    
    def init_menu(self):
        menu_bar = tk.Menu(self.master)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Nuevo Juego", command=self.start_new_game)
        file_menu.add_command(label="Guardar", command=self.save_game)
        file_menu.add_command(label="Cargar", command=self.load_game)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        self.master.config(menu=menu_bar)

    def start_new_game(self):
        size = simpledialog.askinteger("Nuevo Juego", "Tamaño del tablero (3-10):", 
                                     minvalue=3, maxvalue=10)
        if size:
            self.game = GameLogic(size)
            self.create_board()
            self.update_board()

    def create_board(self):
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        
        self.buttons = []
        for i in range(self.game.size):
            row = []
            for j in range(self.game.size):
                btn = tk.Button(self.master, width=4, height=2,
                               command=lambda i=i, j=j: self.on_cell_click(i, j))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)
        
        tk.Button(self.master, text="Siguiente Turno", 
                 command=self.next_turn).grid(row=self.game.size, columnspan=self.game.size)

    def update_board(self):
        for i in range(self.game.size):
            for j in range(self.game.size):
                cell = self.game.board[i][j]
                color = "#90EE90" if cell == 0 else "#FF6961" if cell == 1 else "#A9A9A9"
                text = "🌿" if cell == 0 else "🦠" if cell == 1 else "🧱"
                self.buttons[i][j].config(text=text, bg=color, relief="sunken" if cell == 2 else "raised")
        
        title_info = [
            f"Nivel: {self.game.level}",
            f"Tamaño: {self.game.size}x{self.game.size}",
            f"Barreras: {self.game.barriers_remaining}/{self.game.max_barriers()}",
            f"Zonas libres: {self.game.free_cells()}"
        ]
        self.master.title(" | ".join(title_info))

    def on_cell_click(self, i, j):
        if not self.game.barrier_placed:
            if self.game.place_barrier(i, j):
                self.update_board()
                if self.game.check_loss():
                    messagebox.showinfo("Derrota", "¡Te quedaste sin barreras!")
                    self.start_new_game()
            else:
                msg = "Sin barreras disponibles" if self.game.barriers_remaining <= 0 else "Ubicación inválida"
                messagebox.showerror("Error", f"¡{msg}!")
        else:
            messagebox.showerror("Error", "Solo 1 barrera por turno")

    def next_turn(self):
        self.game.barrier_placed = False
        
        if self.game.check_win():
            self.handle_victory()
            return
            
        if self.game.spread_virus():
            self.update_board()
            
        if self.game.check_loss() or self.game.check_win():
            self.update_board()

    def handle_victory(self):
        if self.game.advance_level():
            messagebox.showinfo("¡Victoria!", 
                f"¡Nivel {self.game.level-1} completado!\n"
                f"Barreras restantes: {self.game.barriers_remaining}\n"
                f"Zonas libres: {self.game.free_cells()}")
            self.create_board()
            self.update_board()
        else:
            messagebox.showinfo("¡Juego Ganado!", 
                "¡Has completado todos los niveles!\n"
                f"Barreras finales restantes: {self.game.barriers_remaining}")
            self.start_new_game()

    def save_game(self):
        filename = simpledialog.askstring("Guardar", "Nombre:")
        if filename and FileManager.save_game(self.game, filename):
            messagebox.showinfo("Éxito", "Partida guardada")
    
    def load_game(self):
        filename = simpledialog.askstring("Cargar", "Nombre:")
        if filename and (loaded_game := FileManager.load_game(filename)):
            self.game = loaded_game
            self.create_board()
            self.update_board()
            messagebox.showinfo("Éxito", "Partida cargada")

if __name__ == "__main__":
    root = tk.Tk()
    app = VirusGameGUI(root)
    root.mainloop()
