#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

echo "${green}[Finished]${reset}"
echo "  - Create virtualenv"
echo "  - Install development requirements inside virtualenv."
echo "  - Create a postgres database"
echo "  - Create .env variables"
echo "  - Run './manage.py migrate'."
echo "  - Initialize git."