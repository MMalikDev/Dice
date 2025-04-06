#!/bin/bash

# Icons
icon_log="\xF0\x9F\x93\x91" # Bookmark Tabs (U+1F4D1)
icon_start="\xF0\x9F\x9B\xA0 " # Hammer and Wrench (U+1F6E0)

display_usage() {
    cat << EOF

Usage: $0 [OPTIONS]

Run Project in specified environment

    OPTIONS
     -s     Run Django server in devcontainer
     -p     Run Python in devcontainer
     -d     Run Django server locally
     -l     Run Python locally
     -c     Run in Docker
     -h     Display this help

Configure $0 defaults using .env file

    Environment:
        - Docker (Default)  (N/A)
        - DEVCONTAINER=True ( 1 )
        - RUN_LOCALLY=True  ( 1 )
        - RUN_SERVER=True   ( 1 )

    Keep Docker Logs:
        - KEEP_LOGS=True    ( 1 )


EOF
    exit 1
}

# Generic
get_env(){
    echo $(grep -i "$@" .env | cut -d "=" -f 2)
}
get_bool(){
    local variable=$(get_env "$@" | tr '[A-Z]' '[a-z]')
    
    if [[ $variable =~ (1|true) ]]; then
        echo true
    else
        echo false
    fi
}
handle_errors(){
    if [[ $(get_bool KEEP_LOGS) == "true" ]]; then
        printf "\n$icon_log Keeping logs...\n\n"
        return
    fi
    if [[ $@ != 0 ]]; then
        printf "\n$icon_start Error encountered!\n\n"
        exit 1
    fi
    
    clear
    printf "\n$icon_log Cleared logs...\n\n"
}

# Linux Binaries
log_error() {
    >&2 echo "$1";
    exit 1;
}
handle_os(){
    local script="$@"
    local os=$(uname | tr '[A-Z]' '[a-z]')
    
    case ${os} in
        linux*)
            printf "\n$icon_start Using Linux binary locally\n\n"
            ${script}
        ;;
        mingw* | cygwin*)
            if ! command -v wsl &> /dev/null; then
                log_error "$icon_start Please Turn on WSL to use this binary"
            fi
            printf "\n$icon_start Using Linux binary with WSL\n\n"
            wsl -e ${script}
        ;;
        darwin*) log_error "$icon_start This program doesn't yet support macOS system" ;;
        *) log_error "$icon_start Unsupported operating system: $os" ;;
    esac
}

# Docker
reload_services(){
    local services=$@
    if [[ -n $services ]]; then
        printf "\n$icon_start Reloading the following service(s): "
        printf "$services\n\n"
    else
        printf "\n$icon_start Reloading all services\n\n"
    fi
    
    docker compose up -d
    echo "$services" | xargs docker compose kill
    echo "$services" | xargs docker compose up --force-recreate --build -d
}
follow_logs(){
    local services=$@
    if [[ -n $services ]]; then
        printf "\n$icon_log Getting logs from the following service(s): "
        printf "$services\n\n"
    else
        printf "\n$icon_log Getting logs from all services\n\n"
    fi
    
    echo "$services" | xargs docker compose logs -f
}
cp_docker(){
    local container=$1
    local source=$2
    local target=$3
    
    local containerID=$(docker-compose ps -qa $container)
    docker cp $containerID:$source $target
}

# Reverse Proxy
start_proxy(){
    cd proxy
    reload_services
    handle_errors $?
    
    docker image prune -f
    cd ..
}

# Python
use_venv(){
    local os=$(uname | tr '[A-Z]' '[a-z]')
    case ${os} in
        linux* | darwin*) source .venv/bin/activate ;;
        mingw* | cygwin*) source .venv/Scripts/activate ;;
        *) log_error "$icon_start Unsupported operating system: $os" ;;
    esac
}
