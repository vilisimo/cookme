## Installation
As the project is fairly simple and only a few packages were used, installation 
should be pretty straightforward on all OS'es. Instructions are for OS X & Linux
distributions, though Windows should be fairly similar as well.

1. Open terminal.
2. Ensure that Python 3.6 is installed:
    ~~~
    python --version
    ~~~
3. Ensure Git is installed:
    ~~~
    git --version
    ~~~
4. Navigate to the folder where `cookme` project should live:
    ~~~
    cd path/to/where/the/project/should/be
    ~~~
5. Clone the repository: 
    ~~~
    git clone https://github.com/vilisimo/cookme
    ~~~
6. __(Recommended)__ Ensure `virtualenvwrapper` is installed:
    ~~~
    pip list | grep virtualenvwrapper
    ~~~ 
  * If it is not, enter:
    ~~~
    pip install virtualenvwrapper.
    ~~~
7. __(Recommended)__ Create virtual environment for the project:
    ~~~ 
    mkvirtualenv -p python3.6 cookme.
    ~~~
8. Set up environment key (`SECRET_KEY`) that is used by Django. For example:
    ~~~
    export SECRET_KEY="z+ogt(o0760*rl6%n$_2u3$$m=d$t-fzx0e)+rmbtv*vj6$wp2" 
    ~~~
9. Once cloned, move to project's directory: 
    ~~~
    cd cookme/
    ~~~
10. Install required packages:
    ~~~
    pip install -r requirements.txt
    ~~~
11. Move to `utilities` directory: 
    ~~~
    cd utilities
    ~~~
12. Once there, run 
    ~~~
    python populate.py
    ~~~
13. Once population is done, move back to the root folder.
14. Run the server:
    ~~~
    python manage.py runserver
    ~~~
15. Access the website by entering `127.0.0.1:8000` in the browser.
