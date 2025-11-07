import tkinter as tk
from tkinter import messagebox
from datamanager import save_data, load_data

def open_add_data_window(parent):
    win = tk.Toplevel(parent)
    win.title("Add Base Data")
    win.geometry("480x520")
    win.config(bg="#ffffff")

    tk.Label(win, text="Enter base sets (comma separated)", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=12)

    entries = {}

    def make_field(label_text, key):
        tk.Label(win, text=label_text, anchor="w", bg="#ffffff").pack(fill="x", padx=20)
        e = tk.Entry(win)
        e.pack(fill="x", padx=20, pady=6)
        entries[key] = e

    make_field("Teachers (e.g. Alice,Bob,Carol)", "teachers")
    make_field("Subjects (e.g. Math,Physics,CS)", "subjects")
    make_field("Rooms (e.g. R101,R102)", "rooms")
    make_field("Classes (e.g. FE,SE,TE)", "classes")
    make_field("Time Slots (e.g. 9-10,10-11,11-12)", "timeslots")

    # Load existing if any
    existing = load_data("sets.json")
    if existing:
        for k, ent in entries.items():
            if k in existing:
                ent.delete(0, tk.END)
                ent.insert(0, ",".join(existing.get(k, [])))

    def save_all():
        data = {}
        for k, ent in entries.items():
            raw = ent.get().strip()
            items = [x.strip() for x in raw.split(",") if x.strip()] if raw else []
            data[k] = items
        # Basic validation
        if not data["teachers"] or not data["subjects"] or not data["rooms"] or not data["timeslots"]:
            if not messagebox.askyesno("Warning", "Some essential sets are empty (teachers/subjects/rooms/timeslots). Save anyway?"):
                return
        save_data("sets.json", data)
        messagebox.showinfo("Saved", "Base data saved to data/sets.json")
        win.destroy()

    tk.Button(win, text="Save & Close", bg="#0078D7", fg="white", command=save_all).pack(pady=18)

    tk.Label(win, text="Tip: separate items with commas. Leave optional fields blank if not needed.",
             font=("Arial", 9), bg="#ffffff", fg="gray").pack(side="bottom", pady=12)
