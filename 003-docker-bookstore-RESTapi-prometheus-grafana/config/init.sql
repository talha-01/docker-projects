CREATE TABLE bookstore_db.books(
    book_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100),
    is_sold BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY (book_id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO bookstore_db.books (title, author, is_sold) VALUES ("Where the Crawdads Sing", "Delia Owens", 1 );
INSERT INTO bookstore_db.books (title, author, is_sold) VALUES ("The Vanishing Half: A Novel", "Brit Bennett", 0);
INSERT INTO bookstore_db.books (title, author, is_sold) VALUES ("1st Case", "James Patterson, Chris Tebbetts", 0);