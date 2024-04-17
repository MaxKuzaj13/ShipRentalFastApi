# Starship Rental Service with FastApi

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
```

2. Install dependencies:
```shell
pip install -r requirements.txt
```
3. Run the FastAPI application using uvicorn:
```shell
uvicorn main:app --reload
```
4. The application will be running at http://127.0.0.1:8000/ by default.

5. Explore the API using Swagger UI at http://127.0.0.1:8000/docs.

### API Endpoints

##### Spaceships
- `POST /spaceships/`: Create a new spaceship.
- `GET /spaceships/{spaceship_id}`: Get details of a specific spaceship by ID.
- `GET /spaceships/`: Get a list of all available spaceships.
- `PUT /spaceships/{spaceship_id}`: Update details of an existing spaceship.
- `DELETE /spaceships/{spaceship_id}`: Delete a spaceship.

##### Customers
- `POST /customers/`: Create a new customer.
- `GET /customers/{customer_id}`: Get details of a specific customer by ID.
- `GET /customers/`: Get a list of all customers.
- `PUT /customers/{customer_id}`: Update details of an existing customer.
- `DELETE /customers/{customer_id}`: Delete a customer.

##### Bookings
- `POST /bookings/`: Create a new booking.
- `GET /bookings/{booking_id}`: Get details of a specific booking by ID.
- `GET /bookings/`: Get a list of all bookings.
- `PUT /bookings/{booking_id}`: Update details of an existing booking.
- `DELETE /bookings/{booking_id}`: Delete a booking.

##### Attachments
- `POST /attachments/files`: Upload and save files on the server.

## Contributing

Contributions are welcome! Before starting, please review the CONTRIBUTING.md file. If you find any issues or have suggestions for improvements, please open an issue, create ticket in [ClickUp](https://sharing.clickup.com/9015557545/b/h/6-901504164692-2/bdb3443a77bb105) or submit a pull request.

### License

This project is licensed under the [MIT License](LICENSE).


### Alembic
1. Project is using Alembic. For initial structure creation, Alembic import should be used shell:

    ```shell
    alembic init alembic
    ```

    After that in new alembic.ini file change sqlalchemy.url to you're postgresql from:
    ```shell
    sqlalchemy.url = driver://user:pass@localhost/dbname
    ```
    In my case it is like this:
    
    ```shell
   sqlalchemy.url = postgresql://user:password@localhost:6543/db
    ```
2. Add models to Alembic by modifying the env.py file located in the Alembic folder. Inside the env.py file, include the following code snippet:
   ``` 
   config.set_main_option('sqlalchemy.url', get_connection_string())
   ```
   Additionally, create a function named get_connection_string() or something similar within the env.py file to generate the SQLAlchemy connection string.

3. Create First migration. To create firs use command 
```shell   
alembic revision --autogenerate -m "First migration"
```
After check in version if everything is ok:
![img.png](img/img.png)
after that you can make migration using command
```shell
alembic upgrade head
```
4. If you have any change of schema you need make revision and upgrade like on previous point 


## Docker

1. To start project in docker use `docker-compose up`
2. To check containers use `docker ps`
3. To create and push it to Dockerhub use command `docker tag shiprentalfastapi-app max997/ship_rental_fast_api:0.1` you can change revision changing last number. After that use to push `docker push max997/ship_rental_fast_api:0.1`.
4. To check it on desktop you can visit: https://hub.docker.com/repository/docker/max997/ship_rental_fast_api/general
![Dockerhub.png](img%2FDockerhub.png)

## Authentication

1. The login and password come from the form data.
2. If the password is incorrect, an exception will be returned.
3. If the password is OK, a token valid for 30 minutes will be returned.