from fastapi import APIRouter, HTTPException
from app.models import prompt_model
from app.assistants import  assistant

# Create an instance of APIRouter
router = APIRouter()

@router.post("/")
async def read_root(prompt: prompt_model.Prompt):
    try:
        # Log the received prompt for debugging purposes
        print("Received prompt:", prompt)

        # Assuming `flight_context.getContext` is an asynchronous function
        result = await assistant.process_prompt(prompt)

        # Return the result
        return result

    except Exception as e:
        # Handle exceptions, log them, and return an HTTPException if needed
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
