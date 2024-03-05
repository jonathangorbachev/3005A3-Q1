
# Flask CRUD Application with Docker and PostgreSQL

This is a simple CRUD (Create, Read, Update, Delete) application that provides various REST API endpoints to interact with a PostgreSQL database. This application allows you to:

- Add a student to the database.
- Retrieve all students from the database.
- Update a student's email in the database.
- Delete a student from the database.

Built using Python and Flask for backend logic, and Docker for containerization and deployment. 

## Prerequisites

Before you begin, ensure you have Docker installed on your machine. You can check your Docker installation by running:

```bash
docker --version
```
- If Docker is not installed, follow the installation guide [here](https://docs.docker.com/engine/install/).


# Deployment Steps
## Start the Application:
To deploy the application, open a terminal and run the following command to build and start the Docker containers:
```
docker compose up --build
```
## Verify containers
In a new terminal window, check the running Docker containers with:

 ```docker container ls```
- you will then see something like
```
TS                           NAMES
a9261a3befd1   jonathangorbachev/flask_live_app:1.0.0   "flask run --host=0.…"   6 seconds ago    Up 4 seconds    0.0.0.0:4000->4000/tcp          flask_app
91787334cbd2   dpage/pgadmin4                           "/entrypoint.sh"         51 minutes ago   Up 4 seconds    443/tcp, 0.0.0.0:5050->80/tcp   pgadmin4_container
397c771289f8   postgres:12                              "docker-entrypoint.s…"   2 hours ago      Up 42 minutes   0.0.0.0:5432->5432/tcp          flask_db
```
## Find PostgreSQL Container IP:
- Copy the TS id of the postgres image (e.g., 397c771289f8) and then run:
 ```docker inspect 397c771289f8```
- Look for the "IPAddress" in the output, which is your container's IP address.
## Access pgAdmin
- Navigate to `localhost:5050` in your browser. When prompted for credentials, use `admin@admin.com` for the username and `root` for the password.
## Connect to Your PostgreSQL Database:
- In pgAdmin, under quick links on the dashboard, click on the `Add New Server` button.
- In the General tab, give your server a name like "ps_db".
- Switch to the Connection tab, and paste the previously found IP address into the "Host name/address" field.
- Enter `postgres` for both the Username and Password fields.
- Click the save button at the bottom right of the popup.

## You should now have access to your pgAdmin dashboard and be able to manage your PostgreSQL database directly from there.
