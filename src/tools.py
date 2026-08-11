import json
import os
from datetime import datetime

TICKETS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tickets.json")
DEMOS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "demo_bookings.json")

def _load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def _save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def book_demo(input_text):
    bookings = _load_json(DEMOS_FILE)
    booking = {
        "id": len(bookings) + 1,
        "details": input_text,
        "booked_at": datetime.now().isoformat()
    }
    bookings.append(booking)
    _save_json(DEMOS_FILE, bookings)
    return "Demo booked successfully (ID #" + str(booking["id"]) + ") for: " + input_text

def create_ticket(input_text):
    tickets = _load_json(TICKETS_FILE)
    ticket = {
        "id": len(tickets) + 1,
        "issue": input_text,
        "status": "open",
        "created_at": datetime.now().isoformat()
    }
    tickets.append(ticket)
    _save_json(TICKETS_FILE, tickets)
    return "Support ticket #" + str(ticket["id"]) + " created for: " + input_text

def check_demo_status(input_text):
    bookings = _load_json(DEMOS_FILE)
    if not bookings:
        return "I don't see any demo bookings on file yet. Would you like to book one?"
    latest = bookings[-1]
    return "Your most recent demo booking is ID #" + str(latest["id"]) + ", booked for: " + latest["details"]

def check_ticket_status(input_text):
    tickets = _load_json(TICKETS_FILE)
    if not tickets:
        return "I don't see any support tickets on file yet. Would you like me to create one?"
    latest = tickets[-1]
    return "Your most recent ticket is #" + str(latest["id"]) + ", status: " + latest["status"] + ", issue: " + latest["issue"]
