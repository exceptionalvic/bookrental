# WhatsApp API Server

This repository demonstrates simple book rental app built with Python/Django and Dockerized for deployment.
Code follows PEP8 and PEP20 standards.

**Steps to run application in Docker container**
1. Clone repo: git clone "https://github.com/exceptionalvic/bookrentalo.git"
2. CD into the cloned directory
3. Create a virtual environment and activate it: `python -m venv env`
4. Admin login details and SECRET_KEY is provided in env.txt file. Test user login also provided.
5. Create a .env file at the root of the project and add SECRET_KEY variable copied from env.txt above. This is sample best practice to hide sensitive details from public. Web container will look for this variable in the .env file as specified in the docker compose file.
6. Ensure that Docker CE and Docker Compose version 2 is installed on your machine
7. To build the 2 images web and nginx and run their containers, if Docker Compose version 1 is installed on your local machine, run `docker-compose -f docker-compose.yml build`, for Docker compose version 2, run `docker compose -f docker-compose.yml build` to build the images. Using Docker compose makes configuration and seperation of concerns easier since it utilizes the principle behind Infrastructure as a code. It comes also handy when running CI/CD operations with multiple customizations. Effectively ensuring local dev setup is not much different from production makes maintainability and lifecycle management easier.
8. To run application, `docker-compose -f docker-compose.yml up -d` for Docker Compose version 1, `docker compose -f docker-compose.yml up -d` for Version 2.
9. This will install requirements and instruct gunicorn to run the web application using Nginx as reverser proxy orchestrated by Docker Compose.
10. Access the running application to login at http://localhost/auth/login/ either as user or Admin. You will be redirected to appropriate custom dashboard. 
Logged in Admin can also access Django Main Admin Area at http://localhost/auth-admin/

11. To inspect that containers are running and up, run `docker ps`and to inspect logs, run `docker logs web` or `docker logs nginx` from the root of the project


**Steps to run application directly without Docker**
1. Clone repo: git clone "https://github.com/exceptionalvic/bookrentalo.git"
2. CD into the cloned directory
3. Create a virtual environment and activate it: `python -m venv env`
4. Install required packages: `pip install -r requirements.txt`
5. Admin login details and SECRET_KEY is provided in env.txt file. Test user login also provided.
6. Create a .env file at the root of the project and add SECRET_KEY variable copied from env.txt above. This is sample best practice to hide sensitive details from public. Web container will look for this variable in the .env file as specified in the docker compose file.
7. Run application: `python manage.py runserver`
8. Access the running application to login at http://localhost:8000/auth/login/ either as user or Admin. You will be redirected to appropriate custom dashboard. 
Logged in Admin can also access Django Main Admin Area at http://localhost:8000/auth-admin/
