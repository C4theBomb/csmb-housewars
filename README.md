# Collegiate Housewars

Welcome to the repository for the Collegiate School of Medicine and Bioscience House Wars site. This is a project that is completely made in the Python Django framework, and should contain all the features that are necessary to run House Wars (if it doesn't please let us know). This repository is open-source, so feel free to download, play around, and/or contribute. Below is a guide detailing the basic usage of the site and instructions for installation of a local development server. Enjoy!

| Table of Contents |
| ------- |
| [Usage](#usage-instructions) |
| [Setup](#setup) |
| [Hosting](#hosting) |
| [Contributing](#contributing) |

## Usage Instructions
So far there are three primary pages on this site. They include the: 
1. Student signup form - this is accessed at `/`, and contains the form for students to signup for House Wars activities.
2. Teacher points form - this is accessed at `/points` and contains the form to award points for activities.
3. Facilitator signup form - this is accessed at `/facilitator` and contains the form for volunteers to signup to facilitate activities.
4. Admin - this is accessed through `/admin`, and contains the function for managing everything related to House Wars that the general population should not be able to see.

## Setup
Welcome to the installation section of the guide. This will walk you through installing the site and spinning up a local development server. There are two methods to settings up the development server. One uses docker and the other just boots up a local development server. I would highly recommend setting up docker for contributing, it is used by very many other projects and is a great tool for development.
- [With Docker](#setup-with-docker)
- [Without Docker](#setup-without-docker)

### Setup with Docker:

#### Prerequisites:
- `git` - You can test if you have git installed using the command `git -v`, which should output a version number. If you do not have git installed you can download it [here](https://git-scm.com/downloads).
- `docker` - You can test if you have docker installed by typing `docker -v` in the terminal. The resulting output should be a version number. If you do not have docker installed, you can download it [here](https://www.docker.com/get-started/).
  
#### Instructions
1. Clone the repository into the desired directory using `git clone https://github.com/C4theBomb/collegiate-housewars.git`.
2. Navigate into the repository using `cd collegiate-housewars`.
3. Open Docker and run the command `docker compose up -d` in a shell.
4. In Docker, open the shell of the `app-1`.
5. Server should be running automatically. The site will be accessible using the [default url](http://localhost:8000). Any changes made in the filesystem will update live on the local server.

#### Relevant Commands:
- `docker compose up`: This will run the docker server on the default url.
  - `-d`: Removed terminal output from the command (disconnected mode). AKA docker doesn't steal your terminal
- `docker compose down`: This will stop the currently running containers and free up other ports for other apps (if you have them).
  - `-v`: Removes volumes as well. Docker volumes can get very large and this will wipe all data contained in your database. WARNING: IRREVERSIBLE.

### Setup without Docker:

#### Prerequisites:
- `git` - You can test if you have git installed using the command `git -v`, which should output a version number. If you do not have git installed you can download it [here](https://git-scm.com/downloads).
- `python` - You can test if you have docker installed by typing `docker -v` in the terminal. The resulting output should be a version number. If you do not have docker installed, you can download it [here](https://www.docker.com/get-started/).
- `pip` - You can test if you have pip installed using `python -m pip --version`. If you do not have it installed then installation instructions can be found [here](https://pip.pypa.io/en/stable/installation/).

#### Instructions:
1. Clone the repository into the desired directory using `git clone https://github.com/C4theBomb/collegiate-housewars.git`.
2. Navigate into the repository using `cd collegiate-housewars`.
3. Install virtualenv by running `python -m pip install virtualenv`.
4. Create a virtualenv using the command `python -m virtualenv venv`.
5. Activate the virtualenvironment using the command for your os:
    - Linux/Mac: `source ./venv/bin/activate`
    - Windows: `.\venv\Scripts\activate`
6. Install dependencies using the command `pip install -r requirements.txt`.
7. Run migrations using the command `python manage.py migrate`.
8. Run the local development server using `python manage.py runserver`.

### Relevant Commands:
- `python manage.py test`: Runs all tests for current features of the site. If something fails, your broke something, please fix it. If you think its not your fault, it probably is. However, if your REALLY think its not your fault, create an issue and we will try our best to resolve it as soon as possible.
- `python manage.py makemigrations`: If you end up making any changes to the files in `housewars/models`, please run this command to log your changes. This will allow us to make the relevant changes to our production database and display the new features on the site.

## Hosting

### Options
There are several options that you can use for hosting the site on a production server. My personal recommendation would either be Heroku or Linode, since it comes pre-configured with the website. Linode is very cheap at only $5 a month, while Heroku is completely free (albeit more restricted).

### Environment Variables
The server environment variables are used to secure data and keep it from entering a cloud, open-acccess environment. Because of this, you will need to define a them file yourself. These are only needed in production and are completely unnecessary if you are using a local development server. The varaibles that you will need are:
- SECRET_KEY - This will contain the secret encryption key of your django server. It can be generated using the command `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`.
- DATABASE_USERNAME - This will be the username of your production database.
- DATABASE_PASSWORD - This will be the password of your production database.
- DATABASE_HOST - This will be the IP address of your production database.

## Contributing
As an open-source school repository we welcome all contributors willing to help make the House Wars website better (by hacking it or otherwise). 

### Instructions
1. Follow the [setup instructions above](#setup) to install the required dependencies and run the local server. You will want to fork the repository and clone your own repository.
2. Commit your new features to your new forked repository.
3. Create a pull request that details the changes/improvements that you have made.
4. Wait for @C4theBomb (C4 Patino), @gywn9081 (Henry Bloch), or @dylanfritz (Dylan Fritz) to open discussion or merge your pull request.
5. After your pull request is merged, it will automatically be uploaded into production code and will show up on the website.
