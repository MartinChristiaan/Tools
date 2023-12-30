# %%
from dataclasses import dataclass
from datetime import datetime, timedelta

from plot_schedule import plot_schedule


@dataclass
class Event:
    title: str
    start_time: datetime
    duration: int  # minutes
    description: str = ""
    preparation: str = None
    tasks: list = None

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration)

    def __str__(self):
        start_time = self.start_time.strftime("%H:%M")
        end_time = self.end_time.strftime("%H:%M")
        return f"{self.title.ljust(20)} {start_time}-{end_time}"


# create an example day planning using the Event class


def set_time(date, hour, minute):
    base_time = datetime(date.year, date.month, date.day, hour, minute)
    return base_time


# Event templates
def morning_routine(date: datetime, hour=7, minute=30):
    return Event(
        "Morning Routine",
        set_time(date, hour, minute),
        60,
        "Wake up, Shower, Breakfast",
    )


def bike_to_work(date: datetime, hour=8, minute=30):
    return Event("Bike to Work", set_time(date, hour, minute), 30, "Bike to Work")


def planning(date: datetime, hour=10, minute=0):
    return Event("Planning", set_time(date, hour, minute), 30, "Planning")


def software_development(date: datetime, hour=10, minute=30, duration=120):
    return Event(
        "Software Development",
        set_time(date, hour, minute),
        duration,
        "Software Development",
    )


def meeting(meetingname, date: datetime):
    base_time = set_time(date, 10, 0)
    return Event(meetingname, base_time, 90, "Meeting")


today = datetime.today()

schedule = [
    morning_routine(today),
    bike_to_work(today),
    planning(today),
    meeting("Meeting 1", today),
]

for event in schedule:
    print(str(event))

plot_schedule(schedule)
