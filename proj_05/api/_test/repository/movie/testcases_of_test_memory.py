import pytest

from api.entities.movie import Movie


class TestCases:
    # TEST-SET
    # pytest.param("movies_seed: list[Movie], movie_id: str, expected_result": Movie)
    get_by_id_test_case: list = [
        pytest.param([], "test_movie_id", None, id="empty"),
        pytest.param(
            [
                Movie(
                    movie_id="test_movie_id",
                    title="My-title",
                    description="My description",
                    released_year=1990,
                )
            ],
            "test_movie_id",
            Movie(
                movie_id="test_movie_id",
                title="My-title",
                description="My description",
                released_year=1990,
            ),
            id="actual-movie",
        ),
    ]

    # TEST-SET
    # pytest.param("movie_seed: list[Movie], movie_title: str, expected_results: list[Movie]")
    get_by_title_test_case: list = [
        # Case 1: Empty movie seed
        pytest.param([], "some-title", [], id="empty-results"),
        # Case 2: Movie is in memory, but target title does not exist
        pytest.param(
            [
                Movie(
                    movie_id="test_movie_id",
                    title="test_wrong_movie_title",
                    description="My description",
                    released_year=1990,
                ),
            ],
            "some-title",
            [],
            id="No-matched-movie",
        ),
        # Case 3: Target movie is in the memory
        pytest.param(
            [
                Movie(
                    movie_id="My_movie",
                    title="target_title",
                    description="My description",
                    released_year=1990,
                )
            ],
            "target_title",
            [
                Movie(
                    movie_id="My_movie",
                    title="target_title",
                    description="My description",
                    released_year=1990,
                )
            ],
            id="expected_movie",
        ),
    ]

    # TEST-SET
    # pytest.param("movie_seed: list[Movie], movie_id: str, expected_result: None")
    delete_movie_test_case: list = [
        # Case 1: If there's no movie_id data, expected_result would be None
        pytest.param([], "wrong_movie_id", None, id="No-movie-id"),
        # Case 2: Success to delete
        pytest.param(
            [
                Movie(
                    movie_id="test_delete_movie",
                    title="Will_be_deleted_movie",
                    description="Test_description",
                    released_year=1990,
                )
            ],
            "test_delete_movie",
            # expected_result: If movie is deleted, method returns deleted Movie object
            Movie(
                movie_id="test_delete_movie",
                title="Will_be_deleted_movie",
                description="Test_description",
                released_year=1990,
            ),
            id="deleting-movie",
        ),
    ]

    # TEST-SET
    # pytest.param("movie_seed: list[movie], movie_id: str, update_parameter: dict, expected_result
    update_movie_test_case: list = [
        # Case 1: Successful update
        pytest.param(
            [
                Movie(
                    movie_id="test_update_movie",
                    title="old_title",
                    description="old_description",
                    released_year=1990,
                )
            ],
            "test_update_movie",
            {"title": "new_title", "description": "new_description", "watched": True},
            Movie(
                movie_id="test_update_movie",
                title="new_title",
                description="new_description",
                released_year=1990,
                watched=True,
            ),
            id="Successful-update-case",
        ),
    ]

    # TEST-SET
    # pytest.param("movie_seed: list[movie], movie_id: str, update_parameter: dict")
    update_movie_fail_test_case = [
        # Case 1: movie is None
        pytest.param(
            [], "wrong_movie_id", {"title": "new_title"}, id="movie-id-not-found"
        ),
        # Case 2: Abandon to update movie_id
        pytest.param(
            [
                Movie(
                    movie_id="movie_id_immutable",
                    title="title",
                    description="description",
                    released_year=1990,
                )
            ],
            "movie_id_immutable",
            {"movie_id": "trying_update_movie_id"},
            id="cannot-update-movie-id",
        ),
    ]
