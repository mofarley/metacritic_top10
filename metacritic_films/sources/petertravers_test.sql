-- SQLite
SELECT title FROM films WHERE id IN (SELECT film_id FROM rankings WHERE critic_id IN (SELECT id FROM critics WHERE critic_name = 'Peter Travers'));