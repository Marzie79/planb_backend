



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

#### If you are using plain python:
- Create the migrations for `users` app: 
  `python manage.py makemigrations`
- Run the migrations:
  `python manage.py migrate`

### Running the project (without docker)
- Open a command line window and go to the backend's directory.
- `pip install -r requirements.txt`
`source venv/bin/activate` 
- `npm install`
- `npm run start`
- Go to the `backend` directory.
- `python manage.py runserver`

### db config for mysql:
        NAME: planBdb
        USER: planBuser
        PASSWORD: planB_pass_1399
