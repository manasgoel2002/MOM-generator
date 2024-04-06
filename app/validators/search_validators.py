async def validate_search(state: any):
    try:
        state["isComplete"] = True
        if "itineries" in state and (state["itineries"] is not None) and state["itineries"]:
            # Check if the first itinerary has all the required details
            first_itinerary = state["itineries"][0]

            missing_fields = []

            if "departurePoint" not in first_itinerary:
                missing_fields.append("departurePoint")

            if "arrivalPoint" not in first_itinerary:
                missing_fields.append("arrivalPoint")

            if "departureDateTime" not in first_itinerary:
                missing_fields.append("departureDateTime")

            # Set isComplete to False if any field is missing
            state["isComplete"] = not bool(missing_fields)

            # Add the missing_fields list to the state
            state["missingFields"] = missing_fields

        else:
            # If "itineries" is empty or None, include it in missingFields
            state["missingFields"] = ["itineries"]
            state["isComplete"] = False
        
        return state

    except Exception as e:
        # Log the exception and return the original state
        # logger.error(f"An error occurred in validate_search: {str(e)}")
        return state
