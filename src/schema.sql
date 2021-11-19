CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "hstore";


CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    api_key uuid DEFAULT uuid_generate_v4 (),
    name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS frames (
    id SERIAL PRIMARY KEY,
    code TEXT,
    file_name VARCHAR(250),
    line TEXT,
    line_number INT,
    method_name VARCHAR(100)
);

CREATE TYPE status AS ENUM ('resolved', 'unresolved', 'ignored');

CREATE TABLE IF NOT EXISTS issues  (
    id SERIAL PRIMARY KEY,
    current_status status DEFAULT 'unresolved',
    -- Used w/ foreign key to tell what project this is linked with
    project_id INT,
    error_name VARCHAR(150),
    environment hstore, -- key-value pair
    request jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    -- Link each issue to a project
    CONSTRAINT fk_project
      FOREIGN KEY(project_id) 
	    REFERENCES projects(id)
);

-- Creating a issues_frames junction table
-- Each issue has multiple frames, so we can't use a foreign key constraint like above.
-- Using a foreign key constraint would only allow each issue to have one frame, which wouldn't be very helpful :)
CREATE TABLE IF NOT EXISTS issues_frames (
	issue_id INT REFERENCES issues (id),
	frame_id INT REFERENCES frames (id),
	PRIMARY KEY (issue_id, frame_id)
);