#!/bin/bash

# set -e

source ./scripts/run.sh
# ---------------------------------------------------------------------- #
# Define Docker Variables
# ---------------------------------------------------------------------- #
declare -a reloads=(
    # django
)

declare -a logs=(
    # django
)

# ---------------------------------------------------------------------- #
# OPTIONS
# ---------------------------------------------------------------------- #
run_docker(){
    reload_services ${reloads[*]}
    handle_errors $?
    docker image prune -f
    follow_logs ${logs[*]}
    exit 0
}

# Devcontainer
run_python_dev(){
    local msg="Running Python in devcontainer venv"
    printf "\n$icon_start $msg\n\n"
    use_venv
    cd src && python3 main.py
    printf "\n\n"
    exit 0
}
run_django_dev(){
    local msg="Running Django in devcontainer venv"
    printf "\n$icon_start $msg\n\n"
    use_venv
    cp .env web/config/.env
    cd web && bash docker.sh
    printf "\n\n"
    exit 0
}

# Local Environment
run_python(){
    local msg="Running Python in local venv"
    printf "\n$icon_start $msg\n\n"
    use_venv
    cd src && python main.py $1
    printf "\n\n"
    exit 0
}
run_django(){
    local msg="Running Django in local venv"
    printf "\n$icon_start $msg\n\n"
    cp .env web/config/.env
    use_venv
    cd web
    python manage.py runserver
    printf "\n\n"
    exit 0
}

# ENV FILE
use_env_file(){
    if [[ $(get_bool RUN_SERVER) == "true" ]] ; then
        [[ $(get_bool DEVCONTAINER) == "true" ]] && run_django_dev
        [[ $(get_bool RUN_LOCAL) == "true" ]] && run_django
    else
        [[ $(get_bool DEVCONTAINER) == "true" ]] && run_python_dev
        [[ $(get_bool RUN_LOCAL) == "true" ]] && run_python
    fi
    run_docker
}

# ---------------------------------------------------------------------- #
# Main Function
# ---------------------------------------------------------------------- #
main(){
    while getopts "spdlch" OPTION; do
        case $OPTION in
            s) run_django_dev   ;;
            p) run_python_dev   ;;
            d) run_django       ;;
            l) run_python       ;;
            c) run_docker       ;;
            h) display_usage    ;;
            ?) display_usage    ;;
        esac
    done
    shift $((OPTIND -1))
    
    use_env_file
}

main $@
