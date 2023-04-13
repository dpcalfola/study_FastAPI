import pytest

from api.entities.movie import Movie
from api.repository.movie.movie import MemoryMovieRepository

from .testcases_of_test_movie import TestCases
from ..abstractions import RepositoryException


def test_creat_movie():
    repo = MemoryMovieRepository()
    movie = Movie(
        movie_id="test",
        title="My_Movie",
        description="My description",
        released_year=1990,
    )
    repo.create_movie(movie)
    assert repo.get_by_id("test") is movie


@pytest.mark.parametrize(
    "movies_seed, movie_id, expected_result", TestCases.get_by_id_test_case
)
def test_get_by_id(movies_seed, movie_id, expected_result):
    repo = MemoryMovieRepository()
    for movie in movies_seed:
        repo.create_movie(movie)
    result = repo.get_by_id(movie_id=str(movie_id))
    assert result == expected_result


@pytest.mark.parametrize(
    "movie_seed, movie_title, expected_results", TestCases.get_by_title_test_case
)
def test_get_by_title(movie_seed, movie_title, expected_results):
    repo = MemoryMovieRepository()
    for movie in movie_seed:
        repo.create_movie(movie)

    result = repo.get_by_title(title=str(movie_title))
    assert result == expected_results


@pytest.mark.parametrize(
    "movie_seed, movie_id, update_parameter, expected_result",
    TestCases.update_movie_test_case,
)
def test_update_movie(movie_seed, movie_id, update_parameter, expected_result):
    repo = MemoryMovieRepository()
    for movie in movie_seed:
        repo.create_movie(movie)

    result = repo.update_movie(
        movie_id=str(movie_id), update_parameter=dict(update_parameter)
    )
    assert result == expected_result


@pytest.mark.parametrize(
    "movie_seed, movie_id, update_parameter",
    TestCases.update_movie_fail_test_case,
)
def test_update_movie_fail(movie_seed, movie_id, update_parameter):
    repo = MemoryMovieRepository()
    for movie in movie_seed:
        repo.create_movie(movie)

    with pytest.raises(RepositoryException):
        repo.update_movie(movie_id=movie_id, update_parameter=update_parameter)


@pytest.mark.parametrize(
    "movie_seed, movie_id, expected_result", TestCases.delete_movie_test_case
)
def test_delete_movie(movie_seed, movie_id, expected_result):
    repo = MemoryMovieRepository()
    for movie in movie_seed:
        repo.create_movie(movie)

    result = repo.delete_movie(movie_id=str(movie_id))
    assert result == expected_result
