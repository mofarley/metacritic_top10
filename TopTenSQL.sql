CREATE TABLE critics (
    id INT,
    critic_name TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE films (
    id INT,
    title TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE rankings (
    film_id INT,
    critic_id INT UNIQUE,
    ranking INT,
    FOREIGN KEY (film_id) REFERENCES films(id),
    FOREIGN KEY (critic_id) REFERENCES critics(id)
);