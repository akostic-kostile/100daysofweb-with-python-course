import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse


# helpers


def _load_movie_data():
    with open("movies.json") as f:
        movies = json.loads(f.read())
        for movie in movies:
            movie["genre"] = movie.get("genre").split("|")
        return {movie["id"]: movie for movie in movies}


movies = _load_movie_data()
all_genres = (movie.get("genre") for movie in movies.values())
VALID_GENRES = set(
    # (item for sublist in all_genres for item in sublist if item != "(no genres listed)")
    (item for sublist in all_genres for item in sublist)
)
VALID_LANGUAGES = set((movie.get("language") for movie in movies.values()))
MOVIE_NOT_FOUND = "movie not found"

# definition


class Movie(types.Type):
    id = validators.Integer(allow_null=True)  # assign in POST
    genre = validators.Array(items=validators.String(enum=list(VALID_GENRES)))
    director_name = validators.String(max_length=100)
    year = validators.Integer(minimum=1900, maximum=2050)
    language = validators.String(
        max_length=100, enum=list(VALID_LANGUAGES), allow_null=True
    )
    title = validators.String(max_length=100)


# API methods


def list_movies() -> List[Movie]:
    return [Movie(movie[1]) for movie in sorted(movies.items())]


def list_movies_by_genre(genre: str) -> List[Movie]:
    return [
        Movie(movie[1])
        for movie in sorted(movies.items())
        if genre.title() in movie[1].get("genre")
    ]


def create_movie(movie: Movie) -> JSONResponse:
    movie_id = len(movies) + 1
    movie["id"] = movie_id
    movies[movie_id] = movie
    return JSONResponse(Movie(movie), status_code=201)


def get_movie(movie_id: int) -> JSONResponse:
    movie = movies.get(movie_id)
    if not movie:
        error = {"error": MOVIE_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    return JSONResponse(Movie(movie), status_code=200)


def update_movie(movie_id: int, movie: Movie) -> JSONResponse:
    if not movies.get(movie_id):
        error = {"error": MOVIE_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    movie.id = movie_id
    movies[movie_id] = movie
    return JSONResponse(Movie(movie), status_code=200)


def delete_movie(movie_id: int) -> JSONResponse:
    if not movies.get(movie_id):
        error = {"error": MOVIE_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    del movies[movie_id]
    return JSONResponse({}, status_code=204)


routes = [
    Route("/", method="GET", handler=list_movies),
    Route("/", method="POST", handler=create_movie),
    Route("/{movie_id}/", method="GET", handler=get_movie),
    Route("/{movie_id}/", method="PUT", handler=update_movie),
    Route("/{movie_id}/", method="DELETE", handler=delete_movie),
    Route("/genre/{genre}/", method="GET", handler=list_movies_by_genre),
]

app = App(routes=routes)


if __name__ == "__main__":
    app.serve("127.0.0.1", 5000, debug=True)
