from datetime import datetime


def create_google_calendar_link(
    event_name: str,
    start_datetime: datetime,
    end_datetime: datetime,
    details="",
    location="",
):
    base_url = "https://www.google.com/calendar/render?action=TEMPLATE"

    start_str = start_datetime.strftime("%Y%m%dT%H%M%SZ")
    end_str = end_datetime.strftime("%Y%m%dT%H%M%SZ")

    event_url = f"{base_url}&text={event_name}&dates={start_str}/{end_str}&details={details}&location={location}"

    return event_url
