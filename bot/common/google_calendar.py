from datetime import datetime


def create_google_calendar_link(
    event_name: str,
    start_datetime: datetime,
    end_datetime: datetime,
    details: str = "",
    location: str = "",
) -> str:
    """Create google calendar link for client's booking.
    Args:
        event_name: Beauty procedure.
        start_datetime: Beauty procedure's start.
        end_datetime: Beauty procedure's end.
        details: Some specific details.
        location: Beauty salon location.

    Returns:
        Google calendar link based on client's booking data.
    """
    base_url: str = "https://www.google.com/calendar/render?action=TEMPLATE"

    beauty_procedure_start_datetime_str: str = start_datetime.strftime("%Y%m%dT%H%M%SZ")
    beauty_procedure_end_datetime_str: str = end_datetime.strftime("%Y%m%dT%H%M%SZ")

    event_url: str = f"{base_url}&text={event_name}&dates={beauty_procedure_start_datetime_str}/{beauty_procedure_end_datetime_str}&details={details}&location={location}"

    return event_url
