import tkinter as tk
from ui_add_data import open_add_data_window
from ui_relations import open_relations_window
from ui_timetable import open_timetable_window

def main_window():
    root = tk.Tk()
    root.title("University Timetable Scheduler")
    root.geometry("520x380")
    root.config(bg="#f7f7f7")

    tk.Label(root, text="🎓 University Timetable Scheduler",
             font=("Helvetica", 18, "bold"), bg="#f7f7f7").pack(pady=24)

    tk.Button(root, text="➕ Add Base Data", width=28, height=2,
              command=lambda: open_add_data_window(root)).pack(pady=8)
    tk.Button(root, text="🔗 Define Relations", width=28, height=2,
              command=lambda: open_relations_window(root)).pack(pady=8)
    tk.Button(root, text="🗓️ Generate & View Timetable", width=28, height=2,
              command=lambda: open_timetable_window(root)).pack(pady=8)

    tk.Label(root, text="Created using Set Theory · Relations · Logic · Pigeonhole Principle",
             font=("Arial", 9), bg="#f7f7f7", fg="gray").pack(side="bottom", pady=18)

    root.mainloop()

if __name__ == "__main__":
    main_window()
