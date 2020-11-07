#!/bin/bash

function install {
    pip3 install --user .;
}

function uninstall {
    pip3 uninstall raspi_dashboard
}

while [ -n "$1" ]; do
    
    case "$1" in
        
        -i) install; exit ;;
        
        -u) uninstall; exit ;;
        
        *) echo "Option $1 not recognized"; exit ;;
        
    esac
    
    shift
    
done

install
