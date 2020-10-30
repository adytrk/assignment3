from datetime import date, datetime

import pytest

from movies.adapters.database_repository import SqlAlchemyRepository
from movies.domain.model import User, Movie, Genre, Review, make_review
from movies.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_movie_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movies()

    # Check that the query returned 177 Movies.
    assert number_of_movies == 177

def test_repository_can_add_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = repo.get_number_of_movies()

    new_movie_id = number_of_movies + 1

    movie = Movie(
        date.fromisoformat('2020-03-09'),
        'Second US coronavirus cruise tests negative amid delays and cancellations',
        'It was revealed ...',
        'https://www.nzherald.co.nz/travel/news/movie.cfm?c_id=7&objectid=12315024',
        'https://www.nzherald.co.nz/resizer/ix7hy3lzkMWUkD8hE6kdZ-8oaOM=/620x349/smart/filters:quality(70)/arc-anglerfish-syd-prod-nzme.s3.amazonaws.com/public/7VFOBLCBCNDHLICBY3CTPFR2L4.jpg',
        new_movie_id
    )
    repo.add_movie(movie)

    assert repo.get_movie(new_movie_id) == movie

def test_repository_can_retrieve_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(1)

    # Check that the Movie has the expected title.
    assert movie.title == 'Coronavirus: First case of virus in New Zealand'

    # Check that the Movie is reviewed as expected.
    review_one = [review for review in movie.reviews if review.review == 'Oh no, COVID-19 has hit New Zealand'][
        0]
    review_two = [review for review in movie.reviews if review.review == 'Yeah Freddie, bad news'][0]

    assert review_one.user.username == 'fmercury'
    assert review_two.user.username == "thorke"

    # Check that the Movie is genreged as expected.
    assert movie.is_genreged_by(Genre('Health'))
    assert movie.is_genreged_by(Genre('New Zealand'))

def test_repository_does_not_retrieve_a_non_existent_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(201)
    assert movie is None

def test_repository_can_retrieve_movies_by_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_date(date(2020, 3, 1))

    # Check that the query returned 3 Movies.
    assert len(movies) == 3

    # these movies are no jokes...
    movies = repo.get_movies_by_date(date(2020, 4, 1))

    # Check that the query returned 5 Movies.
    assert len(movies) == 5

def test_repository_does_not_retrieve_an_movie_when_there_are_no_movies_for_a_given_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_date(date(2020, 3, 8))
    assert len(movies) == 0

def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genres = repo.get_genres()

    assert len(genres) == 10

    genre_one = [genre for genre in genres if genre.genre_name == 'New Zealand'][0]
    genre_two = [genre for genre in genres if genre.genre_name == 'Health'][0]
    genre_three = [genre for genre in genres if genre.genre_name == 'World'][0]
    genre_four = [genre for genre in genres if genre.genre_name == 'Politics'][0]

    assert genre_one.number_of_genreged_movies == 53
    assert genre_two.number_of_genreged_movies == 2
    assert genre_three.number_of_genreged_movies == 64
    assert genre_four.number_of_genreged_movies == 1

def test_repository_can_get_first_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_first_movie()
    assert movie.title == 'Coronavirus: First case of virus in New Zealand'

def test_repository_can_get_last_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_last_movie()
    assert movie.title == 'Covid 19 coronavirus: Kiwi mum on the heartbreak of losing her baby in lockdown'

def test_repository_can_get_movies_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_id([2, 5, 6])

    assert len(movies) == 3
    assert movies[
               0].title == 'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary'
    assert movies[1].title == "Australia's first coronavirus fatality as man dies in Perth"
    assert movies[2].title == 'Coronavirus: Death confirmed as six more test positive in NSW'

def test_repository_does_not_retrieve_movie_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_id([2, 209])

    assert len(movies) == 1
    assert movies[
               0].title == 'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary'

def test_repository_returns_an_empty_list_for_non_existent_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies = repo.get_movies_by_id([0, 199])

    assert len(movies) == 0

def test_repository_returns_movie_ids_for_existing_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie_ids = repo.get_movie_ids_for_genre('Health')

    assert movie_ids == [1, 2]

def test_repository_returns_an_empty_list_for_non_existent_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie_ids = repo.get_movie_ids_for_genre('United States')

    assert len(movie_ids) == 0


def test_repository_returns_date_of_previous_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(6)
    previous_date = repo.get_date_of_previous_movie(movie)

    assert previous_date.isoformat() == '2020-03-01'


def test_repository_returns_none_when_there_are_no_previous_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(1)
    previous_date = repo.get_date_of_previous_movie(movie)

    assert previous_date is None


def test_repository_returns_date_of_next_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(3)
    next_date = repo.get_date_of_next_movie(movie)

    assert next_date.isoformat() == '2020-03-05'


def test_repository_returns_none_when_there_are_no_subsequent_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(177)
    next_date = repo.get_date_of_next_movie(movie)

    assert next_date is None


def test_repository_can_add_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre('Motoring')
    repo.add_genre(genre)

    assert genre in repo.get_genres()


def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('thorke')
    movie = repo.get_movie(2)
    review = make_review("Trump's onto it!", user, movie)

    repo.add_review(review)

    assert review in repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(2)
    review = Review(None, movie, "Trump's onto it!", datetime.today())

    with pytest.raises(RepositoryException):
        repo.add_review(review)


def test_repository_can_retrieve_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_reviews()) == 3


def make_movie(new_movie_date):
    movie = Movie(
        new_movie_date,
        'Coronavirus travel restrictions: Self-isolation deadline pushed back to give airlines breathing room',
        'The self-isolation deadline has been pushed back',
        'https://www.nzherald.co.nz/business/news/movie.cfm?c_id=3&objectid=12316800',
        'https://th.bing.com/th/id/OIP.0lCxLKfDnOyswQCF9rcv7AHaCz?w=344&h=132&c=7&o=5&pid=1.7'
    )
    return movie

def test_can_retrieve_an_movie_and_add_a_review_to_it(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Fetch Movie and User.
    movie = repo.get_movie(5)
    author = repo.get_user('thorke')

    # Create a new Review, connecting it to the Movie and User.
    review = make_review('First death in Australia', author, movie)

    movie_fetched = repo.get_movie(5)
    author_fetched = repo.get_user('thorke')

    assert review in movie_fetched.reviews
    assert review in author_fetched.reviews

