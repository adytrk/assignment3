from datetime import date

from movies.domain.model import User, Movie, Genre, make_review, make_genre_association, ModelException

import pytest


@pytest.fixture()
def movie():
    return Movie(
        date.fromisoformat('2020-03-15'),
        'atitle',
        'adesc',
        'https://www.nzherald.co.nz/business/news/movie.cfm?c_id=3&objectid=12316800',
        'https://th.bing.com/th/id/OIP.0lCxLKfDnOyswQCF9rcv7AHaCz?w=344&h=132&c=7&o=5&pid=1.7',
        1,
        'me',
        'also me',
        4,
        5


    )


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def genre():
    return Genre('New Zealand')


def test_user_construction(user):
    assert user.username == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for review in user.reviews:
        # User should have an empty list of Reviews after construction.
        assert False


def test_movie_construction(movie):
    assert movie.id is None
    assert movie.date == date.fromisoformat('2020-03-15')
    assert movie.title == 'atitle'
    assert movie.first_para == 'adesc'
    assert movie.hyperlink == 'https://www.nzherald.co.nz/business/news/movie.cfm?c_id=3&objectid=12316800'
    assert movie.image_hyperlink == 'https://th.bing.com/th/id/OIP.0lCxLKfDnOyswQCF9rcv7AHaCz?w=344&h=132&c=7&o=5&pid=1.7'

    assert movie.number_of_reviews == 0
    assert movie.number_of_genres == 0

    assert repr(
        movie) == '<Movie 2020-03-15 atitle>'


def test_movie_less_than_operator():
    movie_1 = Movie(
        date.fromisoformat('2020-03-15'), None, None, None, None, None, None, None, None, None
    )

    movie_2 = Movie(
        date.fromisoformat('2020-04-20'), None, None, None, None, None, None, None, None, None
    )

    assert movie_1 < movie_2


def test_genre_construction(genre):
    assert genre.genre_name == 'New Zealand'

    for movie in genre.genreged_movies:
        assert False

    assert not genre.is_applied_to(Movie(None, None, None, None, None, None, None, None, None, None))


def test_make_review_establishes_relationships(movie, user):
    review_text = 'COVID-19 in the USA!'
    review = make_review(review_text, user, movie)

    # Check that the User object knows about the Review.
    assert review in user.reviews

    # Check that the Review knows about the User.
    assert review.user is user

    # Check that Movie knows about the Review.
    assert review in movie.reviews

    # Check that the Review knows about the Movie.
    assert review.movie is movie


def test_make_genre_associations(movie, genre):
    make_genre_association(movie, genre)

    # Check that the Movie knows about the Genre.
    assert movie.is_genreged()
    assert movie.is_genreged_by(genre)

    # check that the Genre knows about the Movie.
    assert genre.is_applied_to(movie)
    assert movie in genre.genreged_movies


def test_make_genre_associations_with_movie_already_genreged(movie, genre):
    make_genre_association(movie, genre)

    with pytest.raises(ModelException):
        make_genre_association(movie, genre)
