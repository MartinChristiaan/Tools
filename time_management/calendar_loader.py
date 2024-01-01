# %%
from dataclasses import dataclass
from typing import List

from auth import authenticate

credentials = authenticate()
# print calendar events for the next 4 days
from datetime import datetime

from googleapiclient.discovery import build
from loguru import logger

service = build("calendar", "v3", credentials=credentials)


@dataclass
class Event:
    kind: str
    etag: str
    id: str
    status: str
    htmlLink: str
    created: str
    updated: str
    summary: str
    creator: dict
    organizer: dict
    start: dict
    end: dict
    iCalUID: str
    sequence: int
    reminders: dict
    eventType: str
    colorId: str = None
    recurringEventId: str = None

    @property
    def start_datetime(self):
        return datetime.fromisoformat(self.start["dateTime"])

    @property
    def end_datetime(self):
        return datetime.fromisoformat(self.end["dateTime"])

    def update_date(self, new_date: datetime):
        new_start_datetime = self.start_datetime.replace(day=new_date.day)
        new_end_datetime = self.end_datetime.replace(day=new_date.day)
        # new_start_datetime
        self.start["dateTime"] = new_start_datetime.isoformat()
        self.end["dateTime"] = new_end_datetime.isoformat()
        return self

    def get_event_dict(self):
        event_dict = {
            "summary": self.summary,
            "start": self.start,
            "end": self.end,
        }
        if self.colorId is not None:
            event_dict["colorId"] = self.colorId
        return event_dict

    @staticmethod
    def parse_from_dict(event_dict):
        filtered_dict = {
            key: value
            for key, value in event_dict.items()
            if key in Event.__annotations__
        }
        return Event(**filtered_dict)

    def __str__(self):
        return (
            f"{self.summary} {self.start_datetime.time()} - {self.end_datetime.time()}"
        )

    @staticmethod
    def sort_per_day(events) -> List[List["Event"]]:
        """
        Sort events per day
        """
        sorted_events = [
            [] for _ in range(7)
        ]  # Create a list of empty lists for each day of the week
        for event in events:
            day_of_week = (
                event.start_datetime.weekday()
            )  # Get the day of the week for the event
            sorted_events[day_of_week].append(
                event
            )  # Add the event to the corresponding day's list
        return sorted_events

    @staticmethod
    def get_template_events(service):
        template_start_date = (
            datetime(2024, 1, 1).isoformat() + "Z"
        )  # 'Z' indicates UTC time
        template_end_date = datetime(2024, 1, 7).isoformat() + "Z"
        logger.info(
            "getting template events from {} to {}".format(
                template_start_date, template_end_date
            )
        )
        events_result = (
            service.events()
            .list(
                calendarId="7d502e6601873b74f71eb738488ed0b0e78b366d78dec7c45bc2c0e24e6fb957@group.calendar.google.com",
                timeMin=template_start_date,
                timeMax=template_end_date,
                maxResults=100,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events_dicts = events_result.get("items", [])
        events = [
            Event.parse_from_dict(event)
            for event in events_dicts
            if not event["start"]["dateTime"].endswith("00Z")
        ]
        return Event.sort_per_day(events)


# %%
events_per_day = Event.sort_per_day(events)
# %%
target_date = datetime(2024, 1, 1)
selected_events = events_per_day[3]
for event in selected_events:
    new_event = event.update_date(target_date).get_event_dict()
    created_event = (
        service.events().insert(calendarId="primary", body=new_event).execute()
    )

# %%
