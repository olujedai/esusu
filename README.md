# Esusu API
Esusu societies finally digitised.


## Getting Started
1. Make sure you have the following installed on your machine:
* Git: [Windows](https://git-scm.com/download/win), [Mac](https://git-scm.com/download/mac). (Linux: Please install using your system's package manager)
* Docker: [Windows](https://docs.docker.com/docker-for-windows/install/), [Mac](https://docs.docker.com/docker-for-mac/install/), [Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/) (ensure you have the latest version).

2. Ensure that docker is running on your machine by running ```docker run hello-world``` 

3. Clone (copy to your local machine) the repository using the command:
```git clone git@github.com:olujedai/esusu.git```

4. Navigate to the esusu folder (```cd esusu```)

5. Set up the environment variables by running ```cp env.sample .env``` and modify the defaults.

6. Build the backend and datebase images using ```docker-compose build```.
It will take a fair bit of time the first time you do it, subsequently it will be much faster. If you get any errors, please get in touch.  

7. Launch the containers using ```docker-compose up``` .

8. The first time you run the app, you may need to run the **migrations** to ensure that all the tables are created in the database. While the app is running (after following the previous step), run the following in **another terminal/command prompt**: 
```docker-compose run esusu_api python esusu/manage.py migrate```

## Endpoint Documention
Documentation of how to use the endpoints is found [here](https://github.com/olujedai/esusu/blob/master/ENDPOINTS.md)


## Running Tests
* ```pipenv install -d```
* ```pipenv shell```
* ```cd esusu/esusu```
* ```python manage.py tests```


## Assumptions
* Users can only belong to one Esusu society throughout the duration of a tenure.
* Each collection period lasts for 4 weeks instead of a month so that everyone in a society gets the same amount of money throughout the savings tenure.


## Technology Stack
* **Language**: [Python](https://www.python.org/)
* **Web Framework**: [Django](https://www.djangoproject.com/)
* **REST API**: [Django Rest Framework](https://django-rest-framework.org/)
* **Database**: [PostgreSQL](https://www.postgresql.org/)
* **OpenAPI**: [Yet another Swagger generator](https://github.com/axnsan12/drf-yasg/)
