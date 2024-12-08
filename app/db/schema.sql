CREATE TABLE checkpoints (
    exercise TEXT,
    section TEXT,
    student TEXT,
    name TEXT CHECK(name IN ('start','complete')) NOT NULL DEFAULT 'start',
    created INTEGER DEFAULT (strftime('%s', 'now')),
    PRIMARY KEY (exercise, section, student, name)
);