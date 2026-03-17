import tkinter as tk
from tkinter import ttk

class NonOverlappingConnector:
    def __init__(self, root):
        self.root = root
        self.root.title("Умные соединения (без пересечений)")
        self.root.geometry("900x600")

        self.nodes = [] # Список: {'name', 'x', 'y'}
        self.links = [] # Список: {'from', 'to'}

        # --- Панель управления ---
        sidebar = tk.Frame(root, width=200, bg="#f8f9fa", padx=10, pady=10)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(sidebar, text="Имя узла:").pack()
        self.name_ent = tk.Entry(sidebar)
        self.name_ent.insert(0, "Узел 1")
        self.name_ent.pack(pady=5)

        tk.Label(sidebar, text="Присоединить к:").pack()
        self.target_combo = ttk.Combobox(sidebar, values=["(Нет)"], state="readonly")
        self.target_combo.current(0)
        self.target_combo.pack(pady=5)

        tk.Button(sidebar, text="Создать узел", command=self.add_node, bg="#e1f5fe").pack(pady=20)
        tk.Button(sidebar, text="Очистить", command=self.reset).pack()

        # --- Холст ---
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

    def add_node(self):
        name = self.name_ent.get().strip()
        target = self.target_combo.get()

        # Авто-расчет позиции (сетка 3x3)
        idx = len(self.nodes)
        x = 150 + (idx % 3) * 200
        y = 100 + (idx // 3) * 150

        new_node = {'name': name, 'x': x, 'y': y}
        self.nodes.append(new_node)
        
        if target != "(Нет)":
            self.links.append({'from': name, 'to': target})

        self.update_ui()
        self.draw()

    def update_ui(self):
        names = ["(Нет)"] + [n['name'] for n in self.nodes]
        self.target_combo['values'] = names
        self.name_ent.delete(0, tk.END)
        self.name_ent.insert(0, f"Узел {len(self.nodes)+1}")

    def draw(self):
        self.canvas.delete("all")
        
        # 1. Отрисовка умных линий
        for link in self.links:
            n1 = next(n for n in self.nodes if n['name'] == link['from'])
            n2 = next(n for n in self.nodes if n['name'] == link['to'])
            
            self.draw_smart_line(n1['x'], n1['y'], n2['x'], n2['y'])

        # 2. Отрисовка узлов
        for n in self.nodes:
            self.canvas.create_rectangle(n['x']-40, n['y']-25, n['x']+40, n['y']+25, 
                                         fill="#fff9c4", outline="#fbc02d", width=2)
            self.canvas.create_text(n['x'], n['y'], text=n['name'])

    def draw_smart_line(self, x1, y1, x2, y2):
        """Рисует ступенчатую линию, чтобы минимизировать наложения"""
        # Смещение, чтобы линии одного направления не сливались (эффект шины)
        offset = 10 if x1 > x2 else -10
        mid_x = (x1 + x2) / 2 + offset
        
        # Строим путь из 3-х отрезков (Z-образный)
        points = [
            x1, y1,       # Старт
            mid_x, y1,    # Горизонтально до середины
            mid_x, y2,    # Вертикально до уровня цели
            x2, y2        # Горизонтально до цели
        ]
        
        self.canvas.create_line(points, width=2, fill="#546e7a", arrow=tk.LAST, smooth=False)

    def reset(self):
        self.nodes, self.links = [], []
        self.update_ui()
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = NonOverlappingConnector(root)
    root.mainloop()
