import typing

from motor import motor_asyncio

from env import MONGODB_CONN

from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository, RepositoryException


class MemoryMovieRepository(MovieRepository):
    """
    This class implements the repository pattern by using simple in Memory repository pattern
    """

    def __init__(self):
        """
        _storage: dict
        key: movie_object.movie_id
        value: movie_object
        """
        self._storage: dict = {}

    async def create_movie(self, movie: Movie) -> typing.Optional[Movie]:
        # Return None if the movie already exists in the repository
        if movie.movie_id in self._storage:
            return None
        # Create movie object
        self._storage[movie.movie_id] = movie
        if await self.get_by_id(movie_id=movie.movie_id) is not None:
            # If movie object is exist in repository, return movie:Movie parameter
            # Return self.get_by_id is likely to make coroutine
            # The reason why return parameter itself but self.get_by_id
            return movie
        else:
            # Return none if movie was not added to the repository
            return None

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        return self._storage.get(movie_id)

    async def get_by_title(self, title: str) -> typing.List[Movie]:
        return_value = []
        for key, value in self._storage.items():
            if title == value.title:
                return_value.append(value)
        return return_value

    async def update_movie(
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

    async def delete_movie(self, movie_id: str):
        # If movie_id does not exist, .pop(key, None) returns None
        return self._storage.pop(movie_id, None)


class MongoMovieRepository(MovieRepository):
    """
    This class implements the repository pattern for Movie entity using MongoDB
    """

    def __init__(self, conn: str = MONGODB_CONN):
        self._client = motor_asyncio.AsyncIOMotorClient(conn)
        self._database = self._client["movie_track_db"]
        # Movie collection which hold movie documents
        self._movies = self._database["movies"]

    async def create_movie(self, movie: Movie) -> typing.Optional[Movie]:
        # Return None if the movie already exists in the DB
        if await self._movies.find_one({"movie_id": movie.movie_id}) is not None:
            return None

        # Insert movie document into DB
        await self._movies.insert_one(
            {
                "movie_id": movie.movie_id,
                "title": movie.title,
                "description": movie.description,
                "released_year": movie.released_year,
                "watched": movie.watched,
            }
        )

        if await self._movies.find_one({"movie_id": movie.movie_id}) is not None:
            return movie
        else:
            return None

    async def get_by_id(self, movie_id: str) -> typing.Optional[Movie]:
        document = await self._movies.find_one({"movie_id": movie_id})
        if document is not None:
            return Movie(
                movie_id=document.get("movie_id"),
                title=document.get("title"),
                description=document.get("description"),
                released_year=document.get("released_year"),
                watched=document.get("watched"),
            )
        else:
            return None

    async def get_by_title(self, title: str) -> typing.List[Movie]:
        return_value: typing.List[Movie] = []
        # Get cursor from DB
        documents_cursor = self._movies.find({"title": title})
        # Iterate through documents
        async for document in documents_cursor:
            return_value.append(
                Movie(
                    movie_id=document.get("movie_id"),
                    title=document.get("title"),
                    description=document.get("description"),
                    released_year=document.get("released_year"),
                    watched=document.get("watched"),
                )
            )
        return return_value

    async def update_movie(
        self, movie_id: str, update_parameter: dict
    ) -> typing.Optional[Movie]:
        # Error: Trying to modify movie_id
        if "id" in update_parameter.keys():
            raise RepositoryException("can't update movie id")

        result = self._movies.update({"movie": movie_id}, {"$set": update_parameter})

        # Error: Nothing to modified ==> No matched movie_id
        if result.modified_count == 0:
            raise RepositoryException(f"movie: {movie_id} not found")

        updated_document = await self.get_by_id(movie_id=movie_id)
        return updated_document

    async def delete_movie(self, movie_id: str) -> typing.Optional[Movie]:
        delete_movie_document = await self.get_by_id(movie_id=movie_id)
        delete_result = self._movies.delete_one({"movie_id": movie_id})

        if delete_result.deleted_count == 1:
            return delete_movie_document
        else:
            return None
