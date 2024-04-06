from typing import List, Optional, Dict
from pydantic import BaseModel, Field, TypeAdapter ,ValidationError
from datetime import datetime

class MeetingElement(BaseModel):
    speaker_name: str = Field(None, description="Name of the speaker")
    affiliation: Optional[str] = Field(None, description="Speaker's affiliation (if available)")
    content: str = Field(None, description="Content of the meeting element (decision, task, proposal, issue, or note)")
    speech_time: Optional[datetime] = Field(None, description="Time of the speech segment (if available from transcript timestamps)")  # Added speech_time field

class MeetingMinutes(BaseModel):
    topic: str = Field(
        None, description="Topic of the meeting")
    attendees: List[MeetingElement] = Field(
        None, description="List of attendees with names and affiliations (if available)")
    decisions: List[MeetingElement] = Field([None], description="List of decisions made during the meeting")
    tasks: List[MeetingElement] = Field([None], description="List of tasks assigned during the meeting with assignee and details")
    proposals: List[MeetingElement] = Field([None], description="List of proposals presented during the meeting")
    issues: List[MeetingElement] = Field([None], description="List of issues and challenges discussed")
    notes: List[MeetingElement] = Field([None], description="List of other noteworthy points discussed")
    isComplete: bool = Field(False, description='Indicates if all required information is available (topic & attendees).')  # Improved description

def generate_meeting_minutes(state: dict) -> MeetingMinutes:
    # Ensure required fields are present in state
    if "topic" not in state or not state["topic"]:
        raise ValueError("Missing required field: topic")
    if "attendees" not in state or not state["attendees"]:
        raise ValueError("Missing required field: attendees")

    # Assuming you have populated other fields in state from the transcript
    try:
        meeting_minutes = MeetingMinutes(**state)  # Unpack state dictionary into keyword arguments
        return meeting_minutes
    except ValidationError as e:
        # Handle other validation errors here (e.g., invalid data types)
        print(f"Validation error: {e}")
        return None
