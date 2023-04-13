class Movie:
    def __init__(
        self,
        *,
        movie_id: str,
        title: str,
        description: str,
        released_year: int,
        watched: bool = False
    ):
        if movie_id is None:
            raise ValueError("Movie id is required")
        self._movie_id = movie_id
        self._title = title
        self._description = description
        self._released_year = released_year
        self._watched = watched

    @property
    def movie_id(self) -> str:
        return self._movie_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def released_year(self) -> int:
        return self._released_year

    @property
    def watched(self) -> bool:
        return self._watched

    # Although they are different object,
    # If all attribute are same each other,
    # these two object consider same
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Movie):
            return False
        if (
            self.movie_id == o.movie_id
            and self.title == o.title
            and self.description == o.description
            and self.released_year == o.released_year
            and self.watched == o.watched
        ):
            return True
