#!/bin/bash

while [ -n "$1" ]; do # while loop starts

	case "$1" in

	-i) pip3 install --user .; exit ;;

	-u) pip3 uninstall raspi_dashboard; exit ;;

    *) echo "Option $1 not recognized"; exit ;;

	esac

	shift

done

pip3 install --user .