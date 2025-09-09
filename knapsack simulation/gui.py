import tkinter as tk
from tkinter import ttk, messagebox
import time, tracemalloc, random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import algoritma
from dp import knapsack_dp
from bt import knapsack_backtrack
from ga import knapsack_ga

class KnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kelompok 1")

        # Input kapasitas
        frm_input = tk.Frame(root)
        frm_input.pack(pady=10)
        tk.Label(frm_input, text="Kapasitas Knapsack:").grid(row=0, column=0)
        self.capacity_entry = tk.Entry(frm_input, width=10)
        self.capacity_entry.grid(row=0, column=1)

        # Input item
        self.tree = ttk.Treeview(root, columns=("Berat", "Nilai"), show="headings", height=5)
        self.tree.heading("Berat", text="Berat")
        self.tree.heading("Nilai", text="Nilai")
        self.tree.pack(pady=5)

        frm_btn = tk.Frame(root)
        frm_btn.pack()
        tk.Button(frm_btn, text="Tambah Item", command=self.add_item).grid(row=0, column=0, padx=5)
        tk.Button(frm_btn, text="Hapus Item", command=self.del_item).grid(row=0, column=1, padx=5)

        # Input parameter GA
        frm_ga = tk.LabelFrame(root, text="Parameter Genetic Algorithm")
        frm_ga.pack(pady=10)

        tk.Label(frm_ga, text="Populasi:").grid(row=0, column=0)
        self.pop_entry = tk.Entry(frm_ga, width=10)
        self.pop_entry.insert(0, "50")
        self.pop_entry.grid(row=0, column=1)

        tk.Label(frm_ga, text="Generasi:").grid(row=1, column=0)
        self.gen_entry = tk.Entry(frm_ga, width=10)
        self.gen_entry.insert(0, "100")
        self.gen_entry.grid(row=1, column=1)

        tk.Label(frm_ga, text="Crossover Rate:").grid(row=2, column=0)
        self.cross_entry = tk.Entry(frm_ga, width=10)
        self.cross_entry.insert(0, "0.8")
        self.cross_entry.grid(row=2, column=1)

        tk.Label(frm_ga, text="Mutation Rate:").grid(row=3, column=0)
        self.mut_entry = tk.Entry(frm_ga, width=10)
        self.mut_entry.insert(0, "0.1")
        self.mut_entry.grid(row=3, column=1)

        # Tombol Run
        tk.Button(root, text="Jalankan Semua Algoritma", command=self.run_algorithms).pack(pady=10)

        # Tabel hasil
        self.result_tree = ttk.Treeview(
            root,
            columns=("Nilai", "Item Terpilih", "Waktu (ms)", "Memori (KB)"),
            show="headings",
            height=4
        )
        for col in ("Nilai", "Item Terpilih", "Waktu (ms)", "Memori (KB)"):
            self.result_tree.heading(col, text=col)
        self.result_tree.pack(pady=5)

        # Di __init__(), ganti bagian grafik:
        self.figure = plt.Figure(figsize=(5,3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Konvergensi Genetic Algorithm")
        self.ax.set_xlabel("Generasi")
        self.ax.set_ylabel("Fitness Terbaik")
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack()

    def add_item(self):
        new_win = tk.Toplevel(self.root)
        new_win.title("Tambah Item")

        tk.Label(new_win, text="Berat:").grid(row=0, column=0)
        weight_entry = tk.Entry(new_win)
        weight_entry.grid(row=0, column=1)

        tk.Label(new_win, text="Nilai:").grid(row=1, column=0)
        value_entry = tk.Entry(new_win)
        value_entry.grid(row=1, column=1)

        def save_item():
            try:
                w = int(weight_entry.get())
                v = int(value_entry.get())
                self.tree.insert("", "end", values=(w, v))
                new_win.destroy()
            except:
                messagebox.showerror("Error", "Input harus angka")

        tk.Button(new_win, text="Simpan", command=save_item).grid(row=2, columnspan=2)

    def del_item(self):
        selected = self.tree.selection()
        for item in selected:
            self.tree.delete(item)

    def run_algorithms(self):
        # Hapus hasil lama
        self.result_tree.delete(*self.result_tree.get_children())

        # Ambil input
        items = [self.tree.item(i)["values"] for i in self.tree.get_children()]
        weights = [int(row[0]) for row in items]
        values  = [int(row[1]) for row in items]
        capacity = int(self.capacity_entry.get())

        # DP
        tracemalloc.start()
        t0 = time.perf_counter()
        val, items_chosen = knapsack_dp(weights, values, capacity)
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1] / 1024
        tracemalloc.stop()

        items_str = ", ".join(str(i) for i in items_chosen) if items_chosen else "-"
        self.result_tree.insert(
            "", "end",
            values=(val, items_str, f"{(t1-t0)*1000:.2f}", f"{mem:.1f}"),
            text="Dynamic Programming"
        )

        # Backtracking
        tracemalloc.start()
        t0 = time.perf_counter()
        val, items_chosen = knapsack_backtrack(weights, values, capacity, len(weights))
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1] / 1024
        tracemalloc.stop()

        items_str = ", ".join(str(i) for i in items_chosen) if items_chosen else "-"
        self.result_tree.insert(
            "", "end",
            values=(val, items_str, f"{(t1-t0)*1000:.2f}", f"{mem:.1f}"),
            text="Backtracking"
        )

        # Genetic Algorithm
        tracemalloc.start()
        t0 = time.perf_counter()
        solution, val, history = knapsack_ga(
            weights, values, capacity,
            pop_size=30, generations=50,
            crossover_rate=0.8, mutation_rate=0.1
        )
        t1 = time.perf_counter()
        mem = tracemalloc.get_traced_memory()[1] / 1024
        tracemalloc.stop()

        items_chosen = [i for i in range(len(solution)) if solution[i] == 1]
        items_str = ", ".join(str(i) for i in items_chosen) if items_chosen else "-"
        self.result_tree.insert(
            "", "end",
            values=(val, items_str, f"{(t1-t0)*1000:.2f}", f"{mem:.1f}"),
            text="Genetic Algorithm"
        )

        self.ax.clear()
        self.ax.plot(range(1, len(history)+1), history, marker="o", linestyle="-")
        self.ax.set_title("Konvergensi Genetic Algorithm")
        self.ax.set_xlabel("Generasi")
        self.ax.set_ylabel("Fitness Terbaik")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()
