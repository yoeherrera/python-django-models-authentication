% Module 0 -- Setup

# Install python

Install python3 per your OS instructions.
    
# Setup a virtual environment with venv

`python -m venv venv`
`source venv/bin/activate`

# Install django and other requirements

Run the following command to install the project’s required libraries: `python -m pip install -r requirements.txt`

# Run server
Verify that you can run your app by running: python manage.py runserver.  Then go to `localhost:8000`.  
**Note:** You will see the below warning that you have unapplied migrations, ignore this for now.  You don’t want to add migrations before you add a User model.  
```
You have 19 unapplied migration(s). Your project may not work properly until you apply the migrations
for app(s): admin, auth, contenttypes, mainapp, sessions.
Run 'python manage.py migrate' to apply them.
```
