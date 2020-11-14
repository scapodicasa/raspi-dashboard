<div align="center">
<strong>
    <h1>Raspi Dashboard</h1>

    A dashboard built for RaspberryPi and Inky pHAT displaying what is now playing on your Spotify

</strong>
</div>

## Environment

This project is developed to run on a [Raspberry Pi](https://www.raspberrypi.org/ "Official Raspberry Pi website") with GPIO header and an [Inky pHAT](https://shop.pimoroni.com/products/inky-phat?variant=12549254217811 "Manufacturer's website"). The reference operating system of this document is [Raspberry Pi OS](https://www.raspberrypi.org/downloads/raspberry-pi-os/ "Download webpage") Lite (without user interface).

### Prerequisites

#### Install some packages

``` bash
sudo apt install python3 python3-pip python3-numpy libtiff5 libopenjp2-7 pigpiod
```

#### Enable SPI kernel module

You can enable it using `raspi-config` tool under Interfacing options.

#### Create a Spotify API application

You will need to create an API application with your Spotify account as explained in the [official Spotify documentation](https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app "Documentation on registering a Spotify application"). Take note of your ```Client ID```, ```Client Secret``` and whitelist one redirect URI of your choice. The redirect URI does not need to be remotely accessible.

## Installation and initialization

Clone this repositroy and then from the root directory run:

``` bash
bash install.sh
```

The installation script will install a couple of executables in a folder that usually already is on yout ```PATH``` . If you encounter problems running our executable please check installation log to verify if the installation folder is on your ```PATH```.

Now you can initializer Spotify login:

``` bash
raspi-dashboard-init --spotify_client_id YOUR_CLIENT_ID --spotify_client_secret YOUR_CLIENT_SECRET --spotify_redirect_uri YOUR_REDIRECT_URI
```

you will be asked to visit an URL with your browser that asks you for Spotify login. Then you have to paste the URL on which the browser will be redirected on console.

If no error is shown, your dashboard is correctly initialized!

## Running

You can simply run the dashboard in a terminal windows with:

``` bash
raspi-dashboard
```

### Set up ```raspi-dashboard``` as service

My choice is to run the dashboard as a service at startup. You can follow [official Raspberry documentation](https://www.raspberrypi.org/documentation/linux/usage/systemd.md "systemd Raspberry official documentation") to setup a service. Please check ```raspi-dashboard.service``` file in this repository as an example to make yours.
