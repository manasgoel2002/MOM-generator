import unittest
from app.models.search_request_model import FlightDetails, Flight, TripType, DateTimeDetails, FlightItineries

class TestFlightDetails(unittest.TestCase):

    def test_flight_details_complete(self):
        # Create instances of the inner classes
        departure_date_time = DateTimeDetails(date='2024-04-05')
        arrival_date_time = DateTimeDetails(date='2024-04-12')
        
        flight_itinerary = FlightItineries(
            departurePoint='MAA',
            arrivalPoint='JFK',
            departureDateTime=departure_date_time,
            arrivalDateTime=arrival_date_time
        )
        
        flight_info = Flight(
            cabinId='Y',
            tripType=TripType.ROUND_TRIP,
            itineraries=[flight_itinerary]
        )
        
        flight_details = FlightDetails(
            flightinfo=flight_info,
            isComplete=True,
            messageIntention='search'
        )
        
        # Convert to JSON
        flight_details_json = flight_details.json()
        
        # Check if the 'isComplete' field is True
        self.assertTrue(flight_details.isComplete)
        
        # Check if the JSON contains the expected keys
        self.assertIn('flightinfo', flight_details_json)
        self.assertIn('isComplete', flight_details_json)
        self.assertIn('messageIntention', flight_details_json)

    def test_flight_details_incomplete(self):
        # Create an instance of FlightDetails with missing required fields
        flight_details = FlightDetails()
        
        # Convert to JSON
        flight_details_json = flight_details.json()
        
        # Check if the 'isComplete' field is False
        self.assertFalse(flight_details.isComplete)
        
        # Check if the JSON does not contain 'flightinfo' key as it's None
        self.assertNotIn('flightinfo', flight_details_json)

if __name__ == '__main__':
    unittest.main()
