# Project: Item Catalog (Version 1.0.1)

Visit live application at http://103.3.62.68.xip.io/

## Description

This project is designed for Udacity Full Stack Web Developer Nanodegree Program. Purpose of this project is to create an application using python. The application is a a list of items within a variety of categories and user registration and authentication system. Registered users will have the ability to add, edit and delete their own items. 

This demo website is  a blog website that has certain features that displays:

* homepage with all current categories along with the latest added items
* items with further details, if selected.
* a functionality to edit, delete or add item. User must be logged in using 3rd party authentication (Google)
* logging in and functionality where a user can add, edit, or delete item information.
* items that can be edited or deleted only by user who posted it.
* A JSON endpoint contains 3 links:

    - Categories & Items - (localhost/catalog/JSON) 
    - Categories - (localhost/catalog/categories/JSON)
    - Items - (localhost/catalog/items/JSON)

## Resources

This application contains a _project_ folder and files _run.py_ and _README.md_. These files can be cloned from [github link]( https://github.com/adeelbarki/udacity_item_catalog.git ) using this commad

`$ git clone https://github.com/adeelbarki/udacity_item_catalog.git`

Make sure to `$ cd udacity_item_catalog` in terminal to access all files. 

### Additional Files

* Virtual enivornment must be installed to run application
* Venv can be installed using command 
    * `$ sudo apt install python3-venv` and
    * `$ python3 -m venv udacity_item_catalog/venv`
* Application folder contains a file requirement.txt. It can be used to install all the required modules to the application
    * Make sure to cd into udacity_item_catalog folder
    * activate virtual environment by typing `$ . venv/bin/activate`
    * Install all the dependencies `$ pip install -r requirements.text`

* To run application a file named 'client_secret.json' must be created with google setup for google authentication

_Note_ : _This file must be placed in the same folder with run.py_

* Don't forget to add client id in template/login.html at `data-clientid="your-client-id-from-google"`


## Initiate Virtual Enivornment

Before running the application make sure to start virtual environment.

Make sure you are in the item catalog directory

`$ cd udacity_item_catalog`

Run virtual environment using following command

`$ . venv/bin/activate` ( _To deactivate environmonet just execute comand `deactivate` in command line_ )


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

* Adeel Ahmed Khan (Adeel Barki)
* _Full Stack Web Developer_
