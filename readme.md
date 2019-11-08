# Install python and django.

Install python3 per your OS instructions.

# Optional: Use virtual env to setup a new environment.

`virtualenv venv`
`source venv/bin/activate`

# Install django and other requirements.

`pip install -r requirements.txt`

# Run server

python blogproj/manage.py runserver


# Create a user account.

Run the create super user command and follow terminal insctructions.

`python blogproj/manage.py createsuperuser`


# Create some content

Navigate to the admin page, login with your new account, and create a few blog posts.
http://localhost:8000/admin

# Navigate to main page and browse around

http://localhost:8000

