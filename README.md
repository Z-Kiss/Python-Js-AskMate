# AskMate

## About

**AskMate** is a Stackoverflow like web application,
where you can ask Questions, write answers and comments

<img src="static\image\readme_pic.png" width="400px"/>

<p>
This project once was a Group project on the Full stack developer course at CodeCool Web Module.
<p>

The application built up with:

* Python
* Flask/Jinja
* HTML


## Setup

To run this application required:
- _**Python 3.8**_ Download here:https://www.python.org/downloads/
- _**PostgresSQL**_ Download here:https://www.postgresql.org/download/


* 1 You need to create a virtual environment at the root directory
```
python -m venv venv
```
* 2 Then you need to activate the virtual environment

**if you're on a Unix-based system**
```
source venv/bin/activate
``` 
**if you're on a Windows system.**
```
venv\Scripts\activate.bat
```

3 Then you need to install the requirements
-  Enter the command
```
pip install -r requirements.txt
```

4 After this you need to configurate a PSQL database and fill out the _**config.env**_ file

## Status

It was a year ago when we finished this project.
I decided to refactor. I feel the need to mention,
how great it felt realizing how much, my skills grown since this project.

Currently, i worked on the Backend side,
and with the help of Flask Blueprint I made the endpoints more readable, and understandable.
I corrected some of the queries, but I feel that layer need more work.


## Features

# Implemented features:

### Questions

You are able to _write_, _edit_, _delete_, _vote_ questions. List all the questions and sort it by: _vote_, _view_, _title_ and _submission time_.

### Answers

You are able to _write_, _edit_, _delete_, _vote_ answers. After you wrote a answer to a question, if the owner of the question find the answer useful,
he/she can accept it and give Honor(little bit later about the Honor system) to the person who answered it.

### Comments

You can _write_, _edit_, _delete_ comments. You can write comment both to Questions and Answers.

### Tags

You can _write_, _delete_ tags and connect it to the Questions.

### Honor system

After the Answers or Questions got up/down vote, the owner will get/loose Honor points.

### Smaller features

* Can upload images
* Check out your own profile
* Check out all the user
* Security

# Future plans

* Implement better Security
* Frontend overhaul
* Refactor queries
* More backend refactoring
