CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    width INT NOT NULL,
    height INT NOT NULL,
    split VARCHAR(10) CHECK (split IN ('train', 'val', 'test'))
);

CREATE TABLE annotations (
    id SERIAL PRIMARY KEY,
    image_id INT REFERENCES images(id) ON DELETE CASCADE,
    x_center FLOAT NOT NULL, -- YOLO x_center (relative)
    y_center FLOAT NOT NULL, -- YOLO y_center (relative)
    width FLOAT NOT NULL,    -- YOLO box width (relative)
    height FLOAT NOT NULL,   -- YOLO box height (relative)
    class_name TEXT NOT NULL
);
