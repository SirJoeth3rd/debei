CREATE TABLE Items (
  item_nbr INTEGER PRIMARY KEY,
  description TEXT,
  name TEXT,
  price INTEGER
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
  item_size TEXT CHECK(item_size IN ('S','M','L'))
);

-- Populate Items

INSERT INTO Items (description, name, price)
  VALUES
    ('a lover darkly', 'dress-1', 50000),
    ('the killer', 'dress-2', 80000),
    ('a tall glass of water', 'dress-3', 30000),
    ('mumbo jumbo', 'dress-4', 10000),
    ('a classy beetle', 'dress-5', 70000),
    ('the modest mirror', 'dress-6', 35000);
