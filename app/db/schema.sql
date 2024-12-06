CREATE TABLE student_submission (
    exercise_name TEXT,
    section_name TEXT,
    student_name TEXT,
    is_complete INTEGER DEFAULT 0,
    starting_time INTEGER DEFAULT (strftime('%s', 'now')),
    submission_time INTEGER,
    created INTEGER DEFAULT (strftime('%s', 'now')),
    PRIMARY KEY (exercise_name, section_name, student_name)
);