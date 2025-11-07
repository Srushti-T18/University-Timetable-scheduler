from datamanager import load_data

def validate_relations():
    relations = load_data("relations.json") or []
    conflicts = []

    # Check teacher/time and room/time conflicts
    teacher_time = {}
    room_time = {}

    for r in relations:
        t_key = (r.get("teacher"), r.get("time"))
        rm_key = (r.get("room"), r.get("time"))
        cls_key = (r.get("class"), r.get("time"))

        # Teacher conflict
        if t_key in teacher_time:
            conflicts.append(f"Teacher {r['teacher']} double-booked at {r['time']}")
        teacher_time[t_key] = r

        # Room conflict
        if rm_key in room_time:
            conflicts.append(f"Room {r['room']} double-booked at {r['time']}")
        room_time[rm_key] = r

        # Class conflict
        if cls_key in teacher_time and cls_key in room_time:
            # Not necessary exact, but keep for detection if same class/time mapped multiple times
            pass

    # Pigeonhole principle check
    sets = load_data("sets.json") or {}
    times = sets.get("timeslots", [])
    rooms = sets.get("rooms", [])
    total_slots = len(times) * len(rooms)
    if total_slots == 0 and relations:
        conflicts.append("No timeslots or rooms defined — cannot schedule.")
    elif len(relations) > total_slots:
        conflicts.append("Pigeonhole Alert: number of lectures > available room×timeslot slots.")

    return conflicts
