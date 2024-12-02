CREATE TABLE section (
    section_id INTEGER PRIMARY KEY, -- alias for ROWID
    section_name TEXT,
    instructor_name TEXT,
    time_recorded INTEGER
) STRICT;

CREATE TABLE exercise (
    exercise_id INTEGER PRIMARY KEY, -- alias for ROWID
    section_id INTEGER,
    exercise_name TEXT,
    starting_code TEXT,
    desired_output TEXT,
    time_recorded INTEGER,
    FOREIGN KEY (section_id) REFERENCES section (section_id)
) STRICT;

CREATE TABLE student (
    student_id INTEGER PRIMARY KEY, -- alias for ROWID
    student_name TEXT,
    section_id INTEGER,
    time_recorded INTEGER,
    FOREIGN KEY (section_id) REFERENCES section (section_id)
) STRICT;

CREATE TABLE student_submission (
    student_submission_id INTEGER PRIMARY KEY, -- alias for ROWID
    student_program TEXT,
    student_program_output TEXT,
    is_complete INTEGER,
    starting_time INTEGER,
    submission_time INTEGER,
    time_recorded INTEGER,
    exercise_id INTEGER,
    student_id INTEGER,
    FOREIGN KEY (exercise_id) REFERENCES exercise (exercise_id)
    FOREIGN KEY (student_id) REFERENCES student (student_id)
) STRICT;