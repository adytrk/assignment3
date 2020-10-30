from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from movies.domain import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('date', Date, nullable=False),
    Column('title', String(255), nullable=False),
    Column('first_para', String(1024), nullable=False),
    Column('hyperlink', String(255), nullable=False),
    Column('rank', String(255), nullable=False),
    Column('director', String(255), nullable=False),
    Column('time', String(255), nullable=False),
    Column('rating', String(255), nullable=False),
    Column('actors', String(255), nullable=False),
    Column('image_hyperlink', String(255), nullable=False)
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)


def map_model_to_tables():
    mapper(model.User, users, properties={
        '_username': users.c.username,
        '_password': users.c.password,
        '_reviews': relationship(model.Review, backref='_user')
    })
    mapper(model.Review, reviews, properties={
        '_review': reviews.c.review,
        '_timestamp': reviews.c.timestamp
    })
    movies_mapper = mapper(model.Movie, movies, properties={
        '_id': movies.c.id,
        '_date': movies.c.date,
        '_title': movies.c.title,
        '_first_para': movies.c.first_para,
        '_hyperlink': movies.c.hyperlink,
        '_rank': movies.c.rank,
        '_director': movies.c.director,
        '_time': movies.c.time,
        '_rating': movies.c.rating,
        '_actors': movies.c.actors,
        '_image_hyperlink': movies.c.image_hyperlink,
        '_reviews': relationship(model.Review, backref='_movie')
    })
    mapper(model.Genre, genres, properties={
        '_genre_name': genres.c.name,
        '_genreged_movies': relationship(
            movies_mapper,
            secondary=movie_genres,
            backref="_genres"
        )
    })