CREATE TABLE section (
    pk_section_id INTEGER PRIMARY KEY, -- alias for ROWID
    txt_section_name TEXT,
    -- txt_instructor_name TEXT,
    ts_time_recorded INTEGER
) STRICT;

CREATE TABLE exercise (
    pk_exercise_id INTEGER PRIMARY KEY, -- alias for ROWID
    fk_section_id INTEGER,
    txt_exercise_name TEXT,
    txt_starting_code TEXT,
    txt_desired_output TEXT,
    ts_time_recorded INTEGER,
    FOREIGN KEY (fk_section_id) REFERENCES section (pk_section_id)
) STRICT;

CREATE TABLE student (
    pk_student_id INTEGER PRIMARY KEY, -- alias for ROWID
    txt_student_name TEXT,
    fk_section_id INTEGER,
    ts_time_recorded INTEGER,
    FOREIGN KEY (fk_section_id) REFERENCES section (pk_section_id)
) STRICT;

CREATE TABLE student_submission (
    pk_student_submission_id INTEGER PRIMARY KEY, -- alias for ROWID
    txt_student_program TEXT,
    txt_student_program_output TEXT,
    bool_is_complete INTEGER,
    ts_starting_time INTEGER,
    ts_submission_time INTEGER,
    ts_time_recorded INTEGER,
    fk_exercise_id INTEGER,
    fk_student_id INTEGER,
    FOREIGN KEY (fk_exercise_id) REFERENCES exercise (pk_exercise_id)
    FOREIGN KEY (fk_student_id) REFERENCES student (pk_student_id)
) STRICT;