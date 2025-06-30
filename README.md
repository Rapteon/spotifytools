# Spotifytools

A Django web app for exporting playlists from your Spotify account.

## Project setup

1. Clone/Download this repository.
2. Create the Python environment by following [these steps](#python-environment)
3. Install pre-commit hook by running: `pre-commit install`. This will setup  
automatic code formatting using the [black formatter](https://github.com/psf/black).
4. Setup the database by following [these steps](#database-setup)
5. Obtain the client ID and client secret by logging into your [Spotify developer account](https://developer.spotify.com/). Also copy your Spotify user ID from your
account (can be found in the [desktop/web app](https://open.spotify.com/) under profile settings).
6. Run the application locally using the command:  
```
python manage.py runserver
``` 
7. Login to the admin console through this URL [http://localhost:8000/admin](http://localhost:8000/admin)
8. Create a new `Credential` object using the web UI with your client ID  
and client secret. This will be used to automatically obtain a token for   authentication from Spotify.
9. Then create a `SpotifyUser` object with your Spotify user ID.  
You can usually find this in your Spotify account settings.
9. You can visit [http://localhost:8000/playlists/](http://localhost:8000/playlists/) to check if your token is working. Note that this page takes time to  load if you have too many songs or too many playlists.
10. Start coding 😄

### Python environment

1. Install conda.
2. Open the checked-out repository in the terminal.
3. Create the environment using:
```
conda env create
```

If you need to add/update dependencies, install the dependency  
in the environment using  
`pip install <some_package>`  
and then run  
`conda env export -n django --ignore-channels --from-history -f environment.yml`  
This will update the environment.yml file, which must then be committed.

### Database setup

This project uses a sqlite3 database. It can be setup by following these steps:

1. Run the command  
`python manage.py migrate`  
after navigating to the project directory in the terminal.
2. Create an admin account by running the command  
`python manage.py createsuperuser`  
Remember the username and password because it will be used to store  
Spotify credentials.