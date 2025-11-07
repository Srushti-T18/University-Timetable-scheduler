import tkinter as tk
from tkinter import ttk, messagebox
from datamanager import load_data, save_data

def open_relations_window(parent):
    sets_data = load_data("sets.json") or {}
    teachers = sets_data.get("teachers", [])
    subjects = sets_data.get("subjects", [])
    classes = sets_data.get("classes", [])
    rooms = sets_data.get("rooms", [])
    timeslots = sets_data.get("timeslots", [])

    if not (teachers and subjects and rooms and timeslots):
        messagebox.showerror("Missing Data", "Please add base data first (teachers, subjects, rooms, timeslots).")
        return

    win = tk.Toplevel(parent)
    win.title("Define Relations")
    win.geometry("760x480")
    win.config(bg="#f9f9f9")

    relations = load_data("relations.json") or []

    tk.Label(win, text="Define Teacher–Subject–Class–Room–Time Relations", font=("Arial", 12, "bold"), bg="#f9f9f9").pack(pady=10)

    top_frame = tk.Frame(win, bg="#f9f9f9")
    top_frame.pack(pady=8)

    def make_cb(values, width=14):
        cb = ttk.Combobox(top_frame, values=values, width=width)
        if values:
            cb.current(0)
        return cb

    teacher_cb = make_cb(teachers)
    subject_cb = make_cb(subjects)
    class_cb = make_cb(classes if classes else ["-"])
    room_cb = make_cb(rooms)
    time_cb = make_cb(timeslots)

    teacher_cb.grid(row=0, column=0, padx=6)
    subject_cb.grid(row=0, column=1, padx=6)
    class_cb.grid(row=0, column=2, padx=6)
    room_cb.grid(row=0, column=3, padx=6)
    time_cb.grid(row=0, column=4, padx=6)

    tk.Label(win, text="Existing Relations:", bg="#f9f9f9").pack(anchor="w", padx=12, pady=(12,0))
    list_frame = tk.Frame(win, bg="#ffffff", bd=1, relief="sunken")
    list_frame.pack(fill="both", expand=True, padx=12, pady=8)

    listbox = tk.Listbox(list_frame)
    listbox.pack(fill="both", expand=True, padx=6, pady=6)

    # show existing
    for r in relations:
        listbox.insert(tk.END, f"{r['time']} | {r['room']} | {r['class']} | {r['subject']} | {r['teacher']}")

    def add_relation():
        r = {
            "teacher": teacher_cb.get(),
            "subject": subject_cb.get(),
            "class": class_cb.get() if class_cb.get() else "",
            "room": room_cb.get(),
            "time": time_cb.get()
        }
        # quick duplicate check
        display = f"{r['time']} | {r['room']} | {r['class']} | {r['subject']} | {r['teacher']}"
        if display in listbox.get(0, tk.END):
            messagebox.showwarning("Duplicate", "This exact relation already exists.")
            return
        relations.append(r)
        listbox.insert(tk.END, display)

    def remove_selected():
        sel = listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        listbox.delete(idx)
        relations.pop(idx)

    def save_relations():
        save_data("relations.json", relations)
        messagebox.showinfo("Saved", "Relations saved to data/relations.json")
        win.destroy()

    btn_frame = tk.Frame(win, bg="#f9f9f9")
    btn_frame.pack(pady=8)

    tk.Button(btn_frame, text="Add Relation", command=add_relation, width=15).grid(row=0, column=0, padx=6)
    tk.Button(btn_frame, text="Remove Selected", command=remove_selected, width=15).grid(row=0, column=1, padx=6)
    tk.Button(btn_frame, text="Save Relations", command=save_relations, bg="#0078D7", fg="white", width=15).grid(row=0, column=2, padx=6)
