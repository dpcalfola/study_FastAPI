import typing

from motor import motor_asyncio

from api.entities.movie import Movie
from api.repository.movie.abstractions import MovieRepository, RepositoryException
from env import MONGODB_CONN


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
