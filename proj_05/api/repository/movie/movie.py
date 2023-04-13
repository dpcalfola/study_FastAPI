import typing

from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository, RepositoryException


class MemoryMovieRepository(MovieRepository):
    def __init__(self):
        """
        _storage: dict
        key: movie_object.movie_id
        value: movie_object
        """
        self._storage: dict = {}

    def create_movie(self, movie: Movie) -> typing.Optional[Movie]:
        self._storage[movie.movie_id] = movie
        return self.get_by_id(movie.movie_id)

    def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        return self._storage.get(movie_id)

    def get_by_title(self, title: str) -> typing.List[Movie]:
        return_value = []
        for key, value in self._storage.items():
            if title == value.title:
                return_value.append(value)
        return return_value

    def update_movie(
        self, movie_id: str, update_parameter: dict
    ) -> typing.Optional[Movie]:
        movie = self._storage.get(movie_id)
        if movie is None:
            raise RepositoryException(f"movie: {movie_id} not found")
        for key, value in update_parameter.items():
            if key == "movie_id":
                raise RepositoryException(f"can't update movie id")

            # Check that update_parameters are fields form Movie entity
            # hasattr => If movie has {key} attribute
            if hasattr(movie, key):
                # Update the Movie entity attribute
                # In movie object, update key(from for loop) value to new value
                setattr(movie, f"_{key}", value)
        return self._storage.get(movie_id)

    def delete_movie(self, movie_id: str):
        # If movie_id does not exist, .pop(key, None) returns None
        return self._storage.pop(movie_id, None)
