CREATE TABLE Items (
  item_nbr INTEGER PRIMARY KEY,
  description TEXT,
  name TEXT,
  price INTEGER
);

CREATE TABLE Orders (
  order_nbr INTEGER PRIMARY KEY,
  item INTEGER,
  name TEXT,
  email TEXT,
  fulfilled BIT,
  marketer TEXT,
  FOREIGN KEY (item) REFERENCES Items(item_nbr)
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
