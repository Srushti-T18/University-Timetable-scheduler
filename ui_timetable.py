import tkinter as tk
from tkinter import messagebox, filedialog
from scheduler import generate_timetable
from datamanager import load_data
import csv
import json
import os

def open_timetable_window(parent):
    result = generate_timetable()
    win = tk.Toplevel(parent)
    win.title("Generated Timetable")
    win.geometry("820x520")
    win.config(bg="#ffffff")

    if result["conflicts"]:
        messagebox.showerror("Conflicts Found", "\n".join(result["conflicts"]))
        # Also show what relations exist
    tk.Label(win, text="📅 Generated Timetable", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=12)

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True, padx=12, pady=8)

    headers = ["Time", "Room", "Class", "Subject", "Teacher"]
    for c, h in enumerate(headers):
        lbl = tk.Label(frame, text=h, borderwidth=1, relief="solid", width=18, bg="#e8e8e8")
        lbl.grid(row=0, column=c, sticky="nsew")

    timetable = result["timetable"]
    if not timetable:
        tk.Label(frame, text="No timetable generated (check relations/data).", fg="red").grid(row=1, column=0, columnspan=5, pady=20)
    else:
        for i, ent in enumerate(timetable, start=1):
            tk.Label(frame, text=ent.get("time", ""), borderwidth=1, relief="solid", width=18).grid(row=i, column=0)
            tk.Label(frame, text=ent.get("room", ""), borderwidth=1, relief="solid", width=18).grid(row=i, column=1)
            tk.Label(frame, text=ent.get("class", ""), borderwidth=1, relief="solid", width=18).grid(row=i, column=2)
            tk.Label(frame, text=ent.get("subject", ""), borderwidth=1, relief="solid", width=18).grid(row=i, column=3)
            tk.Label(frame, text=ent.get("teacher", ""), borderwidth=1, relief="solid", width=18).grid(row=i, column=4)

    # Buttons
    btn_frame = tk.Frame(win, bg="#ffffff")
    btn_frame.pack(pady=12)

    def export_csv():
        if not timetable:
            messagebox.showinfo("Nothing", "No timetable to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], initialfile="timetable.csv")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for e in timetable:
                writer.writerow([e.get("time", ""), e.get("room", ""), e.get("class", ""), e.get("subject", ""), e.get("teacher", "")])
        messagebox.showinfo("Saved", f"Timetable exported to {path}")

    def export_json():
        if not timetable:
            messagebox.showinfo("Nothing", "No timetable to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")], initialfile="timetable.json")
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(timetable, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Saved", f"Timetable exported to {path}")

    tk.Button(btn_frame, text="Export CSV", command=export_csv, width=15).grid(row=0, column=0, padx=8)
    tk.Button(btn_frame, text="Export JSON", command=export_json, width=15).grid(row=0, column=1, padx=8)

    # show quick analytics
    def show_report():
        sets = load_data("sets.json") or {}
        total_slots = len(sets.get("timeslots", [])) * len(sets.get("rooms", []))
        used = len(timetable)
        free = max(total_slots - used, 0)
        report = [
            f"Total possible slots (rooms × timeslots): {total_slots}",
            f"Scheduled lectures: {used}",
            f"Free slots remaining: {free}"
        ]
        messagebox.showinfo("Quick Report", "\n".join(report))

    tk.Button(btn_frame, text="Quick Report", command=show_report, width=15).grid(row=0, column=2, padx=8)
