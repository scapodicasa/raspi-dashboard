# Raspi Dashboard

## Installation

Clone this repositroy and then from the root directory of this project run
```bash
bash install.sh
```
this script makes use of ```pip3``` executable.
After installation please run
```bash
raspi-dashboard-init
```
to initialize Spotify login.

## Running

```install.sh``` will install ```raspi-dashboard``` executablein a folder that usually already is in your ```PATH```. So you can run this program with
```bash
raspi-dashboard
```

## Setting up ```raspi-dashboard``` as service

Create a file ```.raspi-dashboard.ini``` in the home directory of the user who will run the service. The file will look like this:

```ini
[SPOTIFY]
SPOTIFY_CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"
```
