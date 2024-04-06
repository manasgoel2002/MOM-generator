import datetime
from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, TypeAdapter


class TripType(Enum):
    ROUND_TRIP = "ROUND_TRIP"
    ONE_WAY = "ONE_WAY"
    MULTICITY = "MULTI_CITY"


class DateTimeDetails(BaseModel):
    date: str = Field(None, description="date to will be converted to yyyy-mm-dd (able to process today and tommorrow and converted to yyyy-mm-dd)")
    time: Optional[str] = Field(None, description="This is optional parameter (if date is today time is must.) ")


class FlightItineries(BaseModel):
    departurePoint: str = Field(
        " ", description="City name in IATA code for example (Chennai:MAA,New York City:JFK , London: LHR,Tokyo: NRT")
    arrivalPoint: str = Field(
        " ", description="City name in IATA code for example (Chennai:MAA,New York City:JFK , London: LHR,Tokyo: NRT")
    departureDateTime: DateTimeDetails = None
    arrivalDateTime: Optional[DateTimeDetails] = Field(None,description='arrivalDateTime is only required for ROUND_TRIP means it is take value for return dateTime else None')


class Traveler(BaseModel):  
    ADT: int = Field(
        1, description="Number of adult travelers, if not provided set default value as '1' ")
    CHD: int = Field(
        0, description="Number of child travelers, if not provided set default value as '0'")
    INF: int = Field(
        0, description="Number of infant travelers,  if not provided set default value as '0'")


class RequestType(BaseModel):
    messageIntention: str = Field(
        None, description="e.g 'search','update','filter'")


class Flight(BaseModel):
    # Default to Economy
    cabinId: str = Field(
        default="Y", description="F = First , C = Club (Business), W = Economy/Coach Premium , M = Economy (other) , Y = Economy")
    # flightType: str = Field(
    #     None, description="C = Connecting , N = Nonstop , D = Direct , this is an optional catagory")
    tripType: TripType = Field(
        TripType.ONE_WAY, description="ROUND_TRIP,ONE_WAY,MULTI_CITY If only one itinery then ONE_WAY,And More than 2 always be a MULT_CITY,same departure and arrival point just reverse that will be ROUND_TRIP")
    itineraries: List[FlightItineries] = []
    travelers: Dict[str, int] = Field({'ADT':1,'CHD':0,'INF':0},description="user count is imp,if any not provided always add with 0 value,if not any provided then default.")


class FlightDetails(BaseModel):
    flightinfo: Flight = None
    isComplete: bool = Field(False,description='when required information is avialalbe in prompt then it will be true. else false. required fields are departurePoint,arrivalPoint,cabinId,tripType,departureDateTime.date')
    messageIntention: str = Field(
        None, description="e.g 'search','update','filter'")
    otherRequirement: Optional[str] = Field(
        None, description="Add  Budget,Seating preferences,Baggage requirement etc which user require(optional)")
    nextStep: Optional[str] = Field('USER_FEEDBACK',description='If isComplete is true or all required information is colletcted then next step is FLIGHT_SEARCH else USER_FEEDBACK')


# Modifications to match the desired output:
flight_details = FlightDetails(
    cabinId="Y",
    flightType="C",
    tripType=TripType.ONE_WAY,
    travelers={
        "ADT": 1,
        "CHD": 0,
        "INF": 0,
    },
    itineraries=[
        FlightItineries(
            arrivalPoint="PNQ",
            departurePoint="BOM",
            dateTimeDetails=DateTimeDetails(date="2024-03-06"),
            returnDateTimeDetails=DateTimeDetails(date="2024-03-07"),
        )
    ],
)
