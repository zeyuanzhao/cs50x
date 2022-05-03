# 50List
## Video Demo: https://youtu.be/vY6u2ahDW8A
## Description:
\
50List is a simple web app that allows users to create lists of items. Users are able to add and delete entries to different lists, while having everything saved to their account.

The app is built with Flask and Python 3. Bootstrap, the CS50 library, SQLite, Axios, and Werkzeug are also used.

### Project Structure

- static - JavaScript libraries, CSS stylesheets, and other files
- templates - HTML pages rendered by Flask
- 50list.db - SQLite database for storing user data such as logins, lists, and entries
- app.py - Flask application, the backend
- helpers.py - Helper functions used by the backend (app.py)
- README.md - You are here!

### Routes (pages):


| Route | Description | Features |
| --- | --- | --- |
| /login | User login page | A form consisting of a username and password field. Users must enter both fields, or an error message will display. If username and password are not valid, the user is notified. Otherwise, the user is logged in and redirected to /lists. If the page is visited while logged in, the user will be logged out. |
| /register | User registration page | A form consisting of a username, a password, and a password confirmation field. All fields must be entered, or an error message will display. If the username is already taken, the user is notified. The password and confirmation must also match. If everything is successful, the password is hashed and stored, and the user is logged in and redirected to /lists. If the page is visited while logged in, the user will be logged out.|
| /logout | Logs user out | Logs the user out when visited. The user is then redirected to /login. There is no page associated with this route. |
| / | Redirects to /lists | If the user is logged in, the user is redirected to /lists. If the user is not logged in, the user is redirected to /login. |
| /lists | Home page with all lists | Lists all lists created by the user as well as number of items, creation and update timestamp, and a button to access the list. |
| /lists/\<name> | A page for a specific list | Lists all the entries in a specific list, as well as a button to add a new entry. The title and description of the list are also displayed. Clicking on an entry deletes it. |
| /create | Page for creating a new list | A form for creating a new list, with fields for a name and description. The user must enter both fields, or an error message will display. If the name is already taken, the user is notified. If everything is successful, the list is created and the user is redirected to /lists/\<name>. | 