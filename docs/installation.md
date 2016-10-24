##Installation
As the project is fairly simple and only a few packages were used, 
installation should be pretty straightforward on all OS'es. However, 
instructions are geared towards OS X & Linux distributions, though 
Windows should be fairly similar as well.

1. Open terminal.
2. Ensure that Python 3.5.2 is installed: `>>> python --version`.
3. Ensure Git is installed: `>>> git --version`.
4. Navigate to the folder where `Cookme` project should live: `>>> cd path/to/where/the/project/should/be`.
5. Enter: `>>> git clone https://github.com/vilisimo/cookme`.
6. __(Optional)__ Ensure virtualenvwrapper is installed: `>>> pip list`. 
  * If it is not, enter `>>> pip install virtualenvwrapper`.
7. __(Optional)__ Create virtual environment for the project: `>>> mkvirtualenv -p python3.5 cookme`.
8. Once cloned, move to project's directory: `>>> cd cookme`.
9. Install required packages: `>>> pip install -r requirements.txt`.
10. Comment out `from .local_settings import SECRET_KEY`.
11. Uncomment `SECRET_KEY = ...` line to use sample secret key.
13. Apply migrations: `>>> python manage.py migrate`.
12. Run the server: `>>> python manage.py runserver`.
14. Celebrate the fact that the project is written in Python, and there are 
no more setup steps.
15. Access the website by entering `127.0.0.1:8000` in the browser.
