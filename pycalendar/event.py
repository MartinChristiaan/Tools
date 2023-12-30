from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Event:
    title: str
    start_time: datetime
    duration: int  # minutes
    preparation: str = None

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration)

    def __str__(self):
        return f"{self.title} ({self.start_time})-{self.end_time}"
