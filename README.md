# Collegiate Housewars

Welcome to the repository for the Collegiate School of Medicine and Bioscience Housewars site. This repository is open-source, so feel free to download, play around, or contribute. Below is a guide detailing the basic usage of the site and instructions for installation of a local server. Enjoy!

| Table of Contents |
| ------- |
| [Usage](#Usage-Instructions) |
| [Installation](#Installation) |
| [Defining .env](#Defining-env) |
| [Contributing](#Contributing) |

## Usage Instructions
So far there are three primary pages on this site. They include the: 
1. Admin page - this is accessed through `/admin`, and contains the function for managing the activities in the latest housewars and managing points totals and student signups.
2. Student signup form - this is accessed at `/`, and contains the form needed for students to signup for housewars activities.
3. Teacher points form - this is accessed at `/points` and contains the form needed for teachers to add points to houses for activities.

## Installation
Welcome to the installation section of the guide. This will walk you through installing the site and spinning up a local development server. 

### Prerequisites:
- `git` - You can test if you have git installed using the command `git -v`, which should output a version number. If you do not have git installed you can download it [here](https://git-scm.com/downloads).
- `docker` - You can test if you have docker installed by typing `docker -v` in the terminal. The resulting output should be a version number. If you do not have docker installed, you can download it [here](https://www.docker.com/get-started/).
  
### Instructions
1. Clone the repository into the desired directory using `git clone https://github.com/C4theBomb/collegiate-housewars.git`.
2. Navigate into the repository using `cd collegiate-housewars`.
3. Open Docker and run the command `docker compose up` in a shell.
4. In Docker, open the shell of the `app-1`.
5. Run migrations and create a development database using `python manage.py migrate`.
6. Server should be available to run. You can activate the server using `python manage.py runserver`. The site will be accessible using the [default url](http://localhost:8000).

## Defining .env
The `.env` file is used to secure data and keep it from entering a cloud, open-acccess environment. Because of this, you will need to define a `.env` file yourself. The parameters that you will need are:
- SECRET_KEY - This will contain the server key of your django local server. It can be generated using the command `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`.
- DATABASE_USERNAME - This will be the username of your production database.
- DATABASE_PASSWORD - This will be the password of your production database.

## Contributing
As an open-source school repository we welcome all contributors willing to help make our website better.

### Instructions
1. Follow the [installation instructions above](#Installation) to install the required packages and run the local server. You will want to fork the repository before cloning it.
2. Commit your new features to your new forked repository.
3. Create a pull request that details the changes/improvements that you have made.
4. Wait for @C4theBomb to open discussion/merge your pull request.
