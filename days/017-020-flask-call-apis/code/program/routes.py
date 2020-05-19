from datetime import datetime

import requests
from flask import render_template, request

from program import app

VALID_POKE_COLOURS = [
    "black",
    "blue",
    "brown",
    "gray",
    "green",
    "pink",
    "purple",
    "red",
    "white",
    "yellow",
]


@app.route("/")
@app.route("/index")
def index():
    time_now = str(datetime.today())
    return render_template("index.html", title="Template Demo", time=time_now)


@app.route("/100Days")
def p100days():
    return render_template("100Days.html", title="100 days")


@app.route("/chuck")
def chuck():
    joke = get_chuck_joke()
    return render_template("chuck.html", title="Chuck Jokes", joke=joke)


@app.route("/pokemon", methods=["GET", "POST"])
def pokemon():
    pokemon = []
    if request.method == "POST" and "pokecolour" in request.form:
        colour = request.form.get("pokecolour")
        if colour.lower() not in VALID_POKE_COLOURS:
            error_msg = f"Valid colours are {VALID_POKE_COLOURS}"
            return render_template(
                "pokemon.html", title="Pokemons", error_msg=error_msg
            )
        pokemon = get_poke_colours(colour)
    return render_template("pokemon.html", title="Pokemons", pokemon=pokemon)


@app.route("/country", methods=["GET", "POST"])
def country():
    countries = []
    if request.method == "POST" and "country" in request.form:
        user_input = request.form.get("country")
        countries = get_country(user_input)
        if isinstance(
            countries, dict
        ):  # searches that are not found return a dictionary rather than a list
            error_msg = f"Not found '{user_input}', please repeat your serch"
            return render_template(
                "country.html", title="Countries", error_msg=error_msg
            )
    return render_template("country.html", title="Countries", countries=countries)


def get_chuck_joke():
    r = requests.get("https://api.chucknorris.io/jokes/random")
    data = r.json()
    return data["value"]


def get_poke_colours(colour):
    r = requests.get("https://pokeapi.co/api/v2/pokemon-color/" + colour.lower())
    pokedata = r.json()
    pokemon = []

    for i in pokedata["pokemon_species"]:
        pokemon.append(i["name"])

    return pokemon


def get_country(name):
    r = requests.get(f"https://restcountries.eu/rest/v2/name/{name}")
    data = r.json()
    return data
