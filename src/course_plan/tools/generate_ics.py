from ics import Calendar, Event
from datetime import datetime, timedelta

def generate_course_ics(course_name: str, weekly_plan: list, start_date: datetime) -> str:
    calendar = Calendar()

    for i, week in enumerate(weekly_plan):
        event = Event()
        event.name = f"Week {i+1}: {week['title']}"
        event.description = week.get("description", "")
        event.begin = (start_date + timedelta(weeks=i)).replace(hour=9, minute=0)
        event.duration = timedelta(hours=week.get("duration", 2))  # default to 2 hours
        calendar.events.add(event)

    return str(calendar)
