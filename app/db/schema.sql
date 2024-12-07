CREATE TABLE attempts (
    exercise TEXT,
    section TEXT,
    student TEXT,
    is_complete INTEGER DEFAULT 0,
    starting_time INTEGER DEFAULT (strftime('%s', 'now')),
    submission_time INTEGER,
    created INTEGER DEFAULT (strftime('%s', 'now')),
    PRIMARY KEY (exercise, section, student)
);