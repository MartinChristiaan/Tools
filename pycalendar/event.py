# %%
from dataclasses import dataclass
from datetime import datetime, timedelta


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
        return f"{self.title.ljust(40)} {self.start_time.hour}:{self.start_time.minute}-{self.end_time.hour}:{self.end_time.minute}"


# create an example day planning using the Event class


def morning_routine(date: datetime):
    base_time = datetime(date.year, date.month, date.day, 7, 30)
    return Event("Morning Routine", base_time, 60, "Wake up, Shower, Breakfast")


def bike_to_work(date: datetime):
    base_time = datetime(date.year, date.month, date.day, 8, 30)
    return Event("Bike to Work", base_time, 30, "Bike to Work")


def planning(date: datetime):
    base_time = datetime(date.year, date.month, date.day, 9, 0)
    return Event("Planning", base_time, 30, "Planning")


def meeting(meetingname, date: datetime):
    base_time = datetime(date.year, date.month, date.day, 9, 30)
    return Event(meetingname, base_time, 30, "Meeting")


today = datetime.today()

schedule = [
    morning_routine(today),
    bike_to_work(today),
    planning(today),
    meeting("Meeting 1", today),
]
for event in schedule:
    print(event)
