from datamanager import load_data, save_data
from validator import validate_relations

def generate_timetable():
    # Validate first
    conflicts = validate_relations()
    if conflicts:
        return {"conflicts": conflicts, "timetable": []}

    relations = load_data("relations.json") or []
    sets = load_data("sets.json") or {}
    times = sets.get("timeslots", [])
    rooms = sets.get("rooms", [])

    # If relations already have assigned room and time, we will respect them.
    # But ensure uniqueness: if duplicates exist, we tried to prevent that in validator.
    # We'll produce a timetable sorted by time then room.
    timetable = sorted(relations, key=lambda x: (times.index(x["time"]) if x["time"] in times else 0, x["room"]))
    save_data("timetable.json", timetable)
    return {"conflicts": [], "timetable": timetable}
