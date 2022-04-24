SELECT DISTINCT(name) FROM stars
JOIN people ON stars.person_id = people.id
WHERE movie_id IN  -- Use IN when searching through a list of things
(SELECT movie_id FROM stars
JOIN people ON stars.person_id = people.id
WHERE name = "Kevin Bacon" AND birth = 1958)
AND name != "Kevin Bacon";