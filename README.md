### Before Running 

- [ ] Make sure you have Python 3.8,MySql and MySql WorkBench installed
- [ ] create schema in mysql workbench using yellow icon 
![alt text](https://i.stack.imgur.com/fddKr.jpg)
- [ ] then create user with this link 

    https://dev.mysql.com/doc/workbench/en/wb-mysql-connections-navigator-management-users-and-privileges.html
- [ ] Open the command line and go to the directory you want to start your project in.
- [ ] Start your project using:

- [ ] Navigate to the project's directory through your command line.
- [ ] Create a new virtualenv `python -m venv venv`
- [ ] Make sure the virtualenv is activated  `source venv/bin/activate`


- [ ] **if using windows:**

    download the precompiled binary installer. Download the "static" flavor of your Operating System (32bit or 64bit) and simple run the installer.
    https://mlocati.github.io/articles/gettext-iconv-windows.html

    Update the system PATH:

    Control Panel > System > Advanced > Environment Variables

    In the System variables list, click Path, click Edit and then New. Add C:\Program Files\gettext-iconv\bin value.

### Running the project (without docker)
- Open a command line window and go to the backend's directory.
- `pip install -r requirements.txt`
`source venv/bin/activate` 
- `python manage.py testDeploy`

### db config for mysql:
        NAME: planBdb
        USER: planBuser
        PASSWORD: planB_pass_1399
        
#### for reset database:
        python manage.py resetdb

#### for backend developers : 
use `pip freeze > requirements.txt` to add your libraries to site

#### for use backup :
        if need recreate database : python manage.py resetdb
        
        copy .sql text into mysqlworckbench and then click on lightning icon !

use `locust --config=locust.conf` to run locust
