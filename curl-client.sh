#!/bin/bash

MOVIE_API_PORT=5000
MOVIE_API_HOST=127.0.0.1
MOVIE_URL="$MOVIE_API_HOST:$MOVIE_API_PORT/movies"

LAST_POSTED_ID=""  # contains the id of the last posted movie

function create-request-json() {
    [ $# -ne 2 ] && [ $# -ne 3 ] && echo "Usage: create-request-json <title> <release_year> [description]" >&2 && return 1
    JSON_TEMPLATE='{ "title": $title, "release_year": $release_year, "description": $description }'
    if [ -z "$3" ]; then
    jq --null-input --arg title "$1" --argjson release_year "$2" --argjson description null "$JSON_TEMPLATE"
    return 0
    fi
    jq --null-input --arg title "$1" --argjson release_year "$2" --arg description "$3" "$JSON_TEMPLATE"
}

function post-movie() {
    [ $# -ne 2 ] && [ $# -ne 3 ] && echo "Usage: post-movie <title> <release_year> [description]" >&2 && return 1
    RESP=$(curl --silent -X POST "$MOVIE_URL" -H 'Content-Type: application/json' -d "$(create-request-json "$@")")
    echo "$RESP"
    LAST_POSTED_ID=$(echo "$RESP" | jq -r '.id')
}

function get-movies() {
    [ $# -gt 1 ] && echo "Usage: get-movies [id]" >&2 && return 1
    [ $# -eq 0 ] && curl --silent -X GET "$MOVIE_URL" && return 0
    curl --silent -X GET "$MOVIE_URL/$1"
}

function edit-movie() {
    [ $# -ne 3 ] && [ $# -ne 4 ] && echo "Usage: edit-movie <id> <title> <release_year> [description]" >&2 && return 1
    curl --silent -X PUT "$MOVIE_URL/$1" -H 'Content-Type: application/json' \
        -d "$(create-request-json "$2" "$3" "$4")"
}

post-movie
echo "       sets shell variable LAST_POSTED_ID to id of the new movie record"
get-movies random args to get usage string
edit-movie
