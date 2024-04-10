# Starship Rental Service with FastApi
Fast API application to rent starship

This is a FastAPI application for renting starships.

### Requirements

- Python 3.10+
- FastAPI
- uvicorn

### Installation

1. Clone the repository:
    ```shell
        git clone https://github.com/MaxKuzaj13/ShipRentalFastApi.git
        cd ShipRentalFastApi
2. Install dependencies:
pip install -r requirements.txt
3. Run the FastAPI application using uvicorn:
uvicorn main:app --reload
4. The application will be running at http://127.0.0.1:8000/ by default.

5. Explore the API using Swagger UI at http://127.0.0.1:8000/docs.

### API Endpoints
# TODO update endpoint
- `GET /starships/`: Get a list of all available starships.
- `GET /starships/{starship_id}`: Get details of a specific starship by ID.
- `POST /starships/`: Create a new starship.
- `PUT /starships/{starship_id}`: Update details of an existing starship.
- `DELETE /starships/{starship_id}`: Delete a starship.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

### License

This project is licensed under the [MIT License](LICENSE).


### Alembic
1.Project is using Alembic. For initial structure creation, Alembic import should be used shell:
    ```shell
        alembic init alembic

        
After that in new alembic.ini file change sqlalchemy.url to you're postgresql from:

        sqlalchemy.url = driver://user:pass@localhost/dbname

In my case it is like this:

        sqlalchemy.url = postgresql://user:password@localhost:6543/db

2.Add models to alembic (in alembic folder env.py file you have to modify env.py)
In my case it will be change from: 

        target_metadata = None

to:

        import models
        target_metadata = models.Base.metadata


3.Create First migration. To create firs use command


        alembic revision --autogenerate -m "First migration"

After check in version if everything is ok:
![img.png](img/img.png)
after that you can make migration using command
        
        alembic upgrade head

