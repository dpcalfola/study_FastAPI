import typing

from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository, RepositoryException


class MemoryMovieRepository(MovieRepository):

    def __init__(self):
        self._storage: dict = {}

    def create_movie(self, movie: Movie):
        self._storage[movie.id] = movie

    def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        return self._storage.get(movie_id)

    def get_by_title(self, title: str) -> typing.List[Movie]:
        return_value = []
        for key, value in self._storage.items():
            if title == value.title:
                return_value.append(value)
        return return_value

    def update_movie(self, movie_id: str, update_parameter: dict):
        movie = self._storage.get(movie_id)
        if movie is None:
            raise RepositoryException(f"movie: {movie_id} not found")
        for key, value in update_parameter.items():
            if key == "id":
                raise RepositoryException(f"can't update movie id")

            # Check that update_parameters are fields form Movie entity
            if hasattr(movie, key):
                # Update the Movie entity field
                setattr(movie, key, value)

    def delete_movie(self, movie_id: str):
        self._storage.pop(movie_id, None)
