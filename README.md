# Collegiate Housewars

Welcome to the repository for the Collegiate School of Medicine and Bioscience Housewars site. This repository is open-source, so feel free to download, play around, or contribute. Below is a guide detailing the basic usage of the site and instructions for installation of a local server. Enjoy!

| Table of Contents |
| ------- |
| [Usage](#Usage-Instructions) |
| [Installation](#Installation) |
| [Contributing](#Contributing) |

## Usage Instructions
So far there are three primary pages on this site. They include the: 
1. Admin page - this is accessed through `/admin`, and contains the function for managing the activities in the latest housewars and managing points totals and student signups.
2. Student signup form - this is accessed at `/`, and contains the form needed for students to signup for housewars activities.
3. Teacher points form - this is accessed at `/points` and contains the form needed for teachers to add points to houses for activities.

## Installation
Welcome to the installation section of the guide. This will walk you through installing the site and spinning up a local development server. 

### Prerequisites:
- git - You can test if you have git installed using the command `git -v`, which should output a version number. If you do not have it installed you can install it [here](https://git-scm.com/downloads).
- python - You can test if you have python installed by typing `python -v` in the terminal. The resulting output should be a version number. If you do not have python installed, you can download it [here](https://www.python.org/downloads/).
- python-pip - Test if you have it installed by typing `python -m pip --version`. You should see a version number for the current version of pip. There are two ways to download it if you do not have it. You can either run the command `python -m ensurepip --upgrade` if your python installation contains the ensurepip module. Otherwise, you will have to download the [get-pip.py](https://bootstrap.pypa.io/get-pip.py) file from online and run that.
- virtualenv - You will need to install virtualenv by using the command `python -m virtualenv <virtualenv name> <root project directory>`.
  
### Instructions
1. Clone the repository into the desired directory using `git clone https://github.com/C4theBomb/collegiate-housewars.git`
2. Navigate into the repository using `cd collegiate-housewars`
3. Run the command `python -m virtualenv <virtual env name>`, then activate the environment using `./<virtual env name>/Scripts/activate`.
4. Install all the required packages using `pip install -r requirements.txt`.
5. Run migrations and create a development sqlite3 database using `python manage.py migrate`.
6. Server should be available to run. You can activate the server using `python manage.py runserver`. The site will be accessible using the [default url](http://localhost:8000).

## Contributing
As an open-source school repository we welcome all contributors willing to help make our website better.

### Instructions
1. Follow the [Installation instructions above](#Installation-Instructions) to install the required packages and run the local server. You will want to fork the repository before cloning it.
2. Commit your new features to your new forked repository.
3. Create a pull request that details the changes/improvements that you have made.
4. Wait for @C4theBomb to open discussion/merge your pull request.
