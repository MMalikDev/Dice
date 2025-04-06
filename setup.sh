#!/bin/bash

set -e

# Icons
icon_log="\xF0\x9F\x93\x91" # Bookmark Tabs (U+1F4D1)
icon_start="\xF0\x9F\x9B\xA0 " # Hammer and Wrench (U+1F6E0)

source ./scripts/run.sh
# ---------------------------------------------------------------------- #
# Define Project Variables
# ---------------------------------------------------------------------- #
initialize_venv(){
    rm -rf .venv/
    python3 -m venv .venv
}

add_requirements(){
    local deps=$1
    use_venv
    pip3 install -r "$deps/requirements/versions.txt"
}

# ---------------------------------------------------------------------- #
# Main Function
# ---------------------------------------------------------------------- #
main(){
    if [[ $1 == "new" ]] || [ ! -d ".venv" ]; then
        initialize_venv
    fi
    add_requirements "src"
    add_requirements "web"
}

main $@
