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
3. Running the FastAPI Application with Docker Compose

3.1 Installation
Before running the FastAPI application with Docker Compose, ensure that you have Docker Compose installed on your system. You can install Docker Compose by following the instructions provided in the official Docker documentation.

3.2. Docker Configuration Files
Prepare the necessary Docker configuration files within your project directory. These files typically include the Dockerfile and docker-compose.yaml. The Dockerfile contains instructions for building the Docker image, while the docker-compose.yaml defines the configuration for Docker Compose.

3.3. Building the Docker Image
To build the Docker image that contains your FastAPI application, use the following command:
```shell
docker-compose build
```
This command will initiate the image-building process according to the instructions defined in the Dockerfile.



3.4. Running Containers
Once the Docker image is built, you can start the Docker containers using the following command:

```shell
docker-compose up
```
Docker Compose will automatically start all services defined in the docker-compose.yaml file.

3.5. Accessing the Application
After the containers are up and running, your FastAPI application will be accessible at http://localhost:8000. You can test your application by navigating to this location in your web browser or using API testing tools like Postman or curl.

3.6. Stopping Containers
To stop the Docker containers, press Ctrl + C in the terminal where Docker Compose is running, or use the following command:


`   docker-compose down
`
This command will gracefully stop and remove the Docker containers.

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

APP is started in docker checout point 3 how to start. You can also get from dockerhub.
To check it on desktop you can visit: https://hub.docker.com/repository/docker/max997/ship_rental_fast_api/general
![Dockerhub.png](img%2FDockerhub.png)

## Authentication

1. The login and password come from the form data.
2. If the password is incorrect, an exception will be returned.
3. If the password is OK, a token valid for 30 minutes will be returned.