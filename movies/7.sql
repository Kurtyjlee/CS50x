SELECT title, rating FROM movies JOIN ratings
ON movies.id = ratings.movie_id
where year = 2010 ORDER by rating DESC, title ASC;