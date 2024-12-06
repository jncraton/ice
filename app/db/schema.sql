CREATE TABLE section (
    section_id INTEGER PRIMARY KEY, -- alias for ROWID
    section_name TEXT,
    instructor_name TEXT,
    created INTEGER DEFAULT (strftime('%s', 'now'))
);

CREATE TABLE exercise (
    exercise_id INTEGER PRIMARY KEY, -- alias for ROWID
    section_id INTEGER,
    exercise_name TEXT,
    starting_code TEXT,
    desired_output TEXT,
    created INTEGER DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (section_id) REFERENCES section (section_id)
);

CREATE TABLE student (
    student_id INTEGER PRIMARY KEY, -- alias for ROWID
    student_name TEXT,
    section_id INTEGER,
    created INTEGER DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (section_id) REFERENCES section (section_id)
);

CREATE TABLE student_submission (
    student_submission_id INTEGER PRIMARY KEY, -- alias for ROWID
    student_program TEXT,
    student_program_output TEXT,
    is_complete INTEGER DEFAULT 0,
    starting_time INTEGER,
    submission_time INTEGER,
    created INTEGER DEFAULT (strftime('%s', 'now')),
    exercise_id INTEGER,
    student_id INTEGER,
    FOREIGN KEY (exercise_id) REFERENCES exercise (exercise_id)
    FOREIGN KEY (student_id) REFERENCES student (student_id)
);