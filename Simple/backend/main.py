# Importing the necessary libraries
import uvicorn  # Uvicorn is an ASGI server used to run the FastAPI application
from fastapi import FastAPI  # FastAPI is a Python web framework for building APIs
from fastapi.middleware.cors import (
    CORSMiddleware,
)  # Middleware to handle Cross-Origin Resource Sharing (CORS)
from pydantic import (
    BaseModel,
)  # BaseModel from Pydantic is used to define data models with type validation
from typing import List  # List is used to define a list of objects for type hinting


# Define a Pydantic model for a single fruit
class Fruit(BaseModel):
    name: str  # A fruit has a single attribute, `name`, which is a string


# Define a Pydantic model for a collection of fruits
class Fruits(BaseModel):
    fruits: List[Fruit]  # A list of Fruit objects


# Create a FastAPI application instance
app = FastAPI()

# Define the allowed origins for CORS
origins = [
    "http://localhost:3000",  # Allow requests from this origin (commonly for frontend development)
    "http://localhost:5173",  # Another allowed origin, often used by Vite.js or similar tools
]

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow sending credentials (cookies, headers, etc.) with requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all HTTP headers
)

# Simulated in-memory database to store fruits
memory_db = {"fruits": []}  # A dictionary with a key `fruits` that holds a list


# Define an endpoint to get all fruits
@app.get("/fruits", response_model=Fruits)  # HTTP GET method for the `/fruits` endpoint
def get_fruits():
    return Fruits(
        fruits=memory_db["fruits"]
    )  # Return the fruits from the in-memory database in the defined format


# Define an endpoint to add a fruit
@app.post(
    "/fruits", response_model=Fruit
)  # HTTP POST method for the `/fruits` endpoint
def add_fruit(fruit: Fruit):
    memory_db["fruits"].append(
        fruit
    )  # Add the incoming fruit to the in-memory database
    return fruit  # Return the fruit that was added


# Run the application when the script is executed directly
if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0", port=8000
    )  # Start the server at `http://0.0.0.0:8000`
