-- 為 publisher 資料表插入假資料
INSERT INTO publisher (name) VALUES
('出版社A'), ('出版社B'), ('出版社C'), ('出版社D'), ('出版社E');

-- 為 author 資料表插入假資料
INSERT INTO author (name, age) VALUES
('作者甲', 30), ('作者乙', 45), ('作者丙', 28), 
('作者丁', 62), ('作者戊', 33), ('作者己', 51);

-- 為 book 資料表插入假資料
INSERT INTO book (title, publisher_id, price) VALUES
('書籍A', 1, 250), ('書籍B', 2, 300), ('書籍C', 3, 180),
('書籍D', 1, 400), ('書籍E', 4, 220), ('書籍F', 5, 350),
('書籍G', 2, 280), ('書籍H', 3, 190);

-- 為 book_author 資料表插入假資料
INSERT INTO book_author (book_id, author_id) VALUES
(1, 1), (1, 2), (2, 3), (3, 4), (3, 5), 
(4, 1), (5, 6), (6, 2), (6, 3), (7, 4), (8, 5);