CREATE TABLE critics (
    id INTEGER NOT NULL PRIMARY KEY,
    critic_name TEXT
);

CREATE TABLE films (
    id INTEGER NOT NULL PRIMARY KEY,
    title TEXT
);

CREATE TABLE rankings (
    film_id INTEGER,
    critic_id INTEGER,
    ranking INTEGER,
    FOREIGN KEY (film_id) REFERENCES films(id),
    FOREIGN KEY (critic_id) REFERENCES critics(id)
);