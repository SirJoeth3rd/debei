CREATE TABLE Items (
  item_nbr INTEGER PRIMARY KEY,
  description TEXT,
  name TEXT,
  price INTEGER
);

CREATE TABLE ItemColors (
  item_nbr INTEGER NOT NULL REFERENCES Items(item_nbr),
  color_nbr INTEGER NOT NULL REFERENCES Colors(color_nbr)
);
CREATE TABLE Colors (
  color_nbr INTEGER PRIMARY KEY,
  name TEXT,
  price_modifier INTEGER DEFAULT 0
);

CREATE TABLE Orders (
  order_nbr INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  marketer TEXT DEFAULT '',
  createtime DATETIME DEFAULT CURRENT_TIMESTAMP,
  status TEXT CHECK(status IN ('new','matched','cancelled','done')) DEFAULT 'new'
);

-- many to many between orders and items
CREATE TABLE OrderItems (
  order_item_nbr INTEGER PRIMARY KEY,
  item_nbr INTEGER REFERENCES Items(item_nbr),
  order_nbr INTEGER REFERENCES Orders(order_nbr),
  item_size TEXT CHECK(item_size IN ('S','M','L')),
  item_color INTEGER NOT NULL REFERENCES Colors(color_nbr)
);

-- Populate Items

INSERT INTO Colors (name, price_modifier)
  VALUES
    ('blue', 0),('pink', 0),('zebra', 0);

INSERT INTO Items (description, name, price)
  VALUES
  ('cheeky in the summer sun', 'tanga', 30000),
  ('twins of the gazelle','bikini', 20000),
  ('elegant lady, dancing in the water','slip',30000),
  ('a waterfall of shimmering skin','triangle_top', 30000),
  ('beauty in the eyes of all beholders','one_piece', 60000),
  ('a rising crescent moon', 'one_shoulder_top', 40000);
