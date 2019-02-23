# Project: Item Catalog (Version 1.0.1)

## Description

This project is designed for Udacity Full Stack Web Developer Nanodegree Program. Purpose of this project is to create an application using python. The application is a a list of items within a variety of categories and user registration and authentication system. Registered users will have the ability to add, edit and delete their own items. 

Visit live application at http://172.104.160.122

This demo website is  a blog website that has certain features that displays:

* homepage with all current categories along with the latest added items
* items with further details, if selected.
* a functionality to edit, delete or add item. User must be logged in using 3rd party authentication (Google)
* logging in and functionality where a user can add, edit, or delete item information.
* items that can be edited or deleted only by user who posted it.
* A JSON endpoint, (localhost/catalog.json)

## Resources

The project contains a _project_ folder and files _run.py_ and _README.md_. These files can be cloned from [github link]( https://github.com/adeelbarki/udacity_item_catalog.git ) using this commad

`$ git clone https://github.com/adeelbarki/udacity_item_catalog.git`

Make sure to `$ cd udacity_item_catalog` in terminal to access all files. 

To run code succesfully make sure that the required files are downloaded and unzip in udacity_item_catalog folder. The zip files can also be downloaded from google drive link:

* venv - Virtual environment contains all the required flask related modules used in application.

[Google Drive Link:](https://drive.google.com/open?id=1v66ZexoEw9DlaDcX5fGxTtwRDl6zO6fv)

* To run application a file named 'client_secret.json' must be created with google setup for google authentication

_Note_ : _This file must be placed in the same folder with run.py_

* Add client id in template/login.html at `data-clientid="your-client-id"`


## Initiate Virtual Enivornment

Before running the code make sure to start virtual environment.

Make sure to you are in the item catalog directory

`$ cd udacity_item_catalog`

Run virtual environment using following command

`$ . venv/bin/activate` ( _To deactivate environmonet just execute coomand `deactivate` in command line_ )


## Run the code

To run application, enter this following command.

`$ python run.py`

Open any internet browser like Chrome, Firefox or internet explorer and type URL

`localhost:5000`.  

## Testing

Results of these tasks can be seen on the browser by testing all tabs.


## Code Style

Code is verified with pep8 code style.

## License

Project Item Catalog is a part of Full Stack Web Development Nanodegree Program at [Udactiy](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).  

## Author

Adeel Ahmed Khan (Adeel Barki)
_Full Stack Web Developer_
