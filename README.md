# Starship Rental Service with FastApi
Fast API application to rent starship

This is a FastAPI application for renting starships.

### Requirements

- Python 3.10+
- FastAPI
- uvicorn

### Installation

1. Clone the repository:
    git clone <repository_url>
    cd ShipRentalFastApi
2. Install dependencies:
pip install -r requirements.txt
3. Run the FastAPI application using uvicorn:
uvicorn main:app --reload
4. The application will be running at http://127.0.0.1:8000/ by default.

5. Explore the API using Swagger UI at http://127.0.0.1:8000/docs.

### API Endpoints

- `GET /starships/`: Get a list of all available starships.
- `GET /starships/{starship_id}`: Get details of a specific starship by ID.
- `POST /starships/`: Create a new starship.
- `PUT /starships/{starship_id}`: Update details of an existing starship.
- `DELETE /starships/{starship_id}`: Delete a starship.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

### License

This project is licensed under the [MIT License](LICENSE).







