# Introduction
Wizchat is a multimodal chatbot interface with supervisor functionality. This chat interface is intended for use in settings where user-chatbot conversations need supervision.
Supervisors can choose different roles, including:
- verify/edit all chatbot messages before sending to user
- verify/edit chatbot messages when chatbot asks for help
- observing user and chatbot messages only
- messaging the user directly without the chatbot
Conversations can involve exchanging text and images, and all chat data are saved to a database.

# Editing this repo
## Chatbot/NLP Models
This repo comes without an nlp model to drive the chatbot. This should be included in the file nlp.py. 
## Image
To demonstrate the multimodal functionality of wizchat, this repo comes with an example interactive image. This can also be edited and replaced.
## Django
Wizchat is a Django web project: https://www.djangoproject.com/

Inspiration for the text chat interface came from here: https://onaircode.com/javascript-js-chat-box-examples

# Installation
- Open Terminal and download the wizchat project folder onto your computer
```sh
$ git clone git@github.com:jpbywater/wizchat.git
```
- Install python3 and required python packages
- Install docker: https://www.docker.com/products/docker-desktop
- Run redis (more info here: https://channels.readthedocs.io/en/latest/tutorial/part_2.html)
```sh
$ docker run -p 6379:6379 -d redis:5
```
- From wizchat folder, run the Django server
```sh
$ python manage.py runserver
```
- Copy and paste the server location into a browser: https://127.0.0.1:8000

# User access
Use the following login credentials (Change these if publically deploying):
- Admin. can access as user and supervisor (Username: admin_user Password: admin_pass)
- Test. can access as user only (Username: test_user Password: test_pass)

To add additional users, use the Django https://127.0.0.1:8000/admin interface. 
New users can be given: 
- user interface access by adding a user to the 'participant' group
- supervisor interface access by adding a user to the 'oz' group

# Supervisor functions
After logging in, supervisors can pick from a list of logged in users and can pick their supervisor role. 

![saved_chat](https://user-images.githubusercontent.com/14824994/120213852-b60d1a80-c201-11eb-8c08-3634eed666a0.png)

# Saved chat data
The chat data for each conversation is saved in JSON format in the chat_data field of the 'Saved Chat' database table.
