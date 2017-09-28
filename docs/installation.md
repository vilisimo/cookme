## Note
Since the project is already deployed, the settings reflect that. To fiddle 
around with the project, it's best to look at the older commits or commit 
history to see what's changed and how to develop purely on local machine.

## Installation
Instructions are for OS X & Linux distributions. However, Windows set-up
should be relatively similar.

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
8. Set up environment keys:
    ~~~
    export AWS_ACCESS_KEY_ID = [your access key id]
    export AWS_SECRET_ACCESS_KEY = [your aws secret access key]
    export AWS_STORAGE_BUCKET_NAME = [your bucket name]
    export AWS_S3_REGION_NAME = [your region name]
    export COOKME_SECRET_KEY = [your secret key]
    export COOKME_DEBUG = True 
    ~~~
   Alternatively, you can set up your `virtualenvwrapper` to initialize them every time it
   is activated. Please refer to this [StackOverflow](https://stackoverflow.com/a/11134336/4543382) 
   thread to find out how.
   
   For AWS-related info, [this](https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/)
   is a good place to learn more about how to set up AWS for static & media file serving. 
   While following it, you will set up all of the AWS_* keys above.
   
   Alternatively, for development purposes, static/media files could simply be served from
   local machine. This [commit](https://github.com/vilisimo/cookme/blob/636aa49ebaff2e899c2f22d32f86d56657a5e372/cookme/settings.py)
   settings could serve as a starting point for the setup.
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
   This will not only set up migrations, but also create two users: 
   _test_ (password: _test_) and _admin_ (superuser, password: _admin_)  
13. Once population is done, move back to the root folder.
14. Run the server:
    ~~~
    python manage.py runserver
    ~~~
15. Access the website by entering `127.0.0.1:8000` in the browser.
