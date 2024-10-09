create database virtual_bookshelf;

use virtual_bookshelf;

DROP TABLE IF EXISTS books, authors, book_author, publisher, book_publisher, genre, book_genre, series, book_series, accounts, account_books;  /* cleanup old stuff */

create table books
  (isbn		 		    char(13) NOT NULL PRIMARY KEY,
   title	 		    varchar(225) NOT NULL,
   pages	 		    smallint(5) NOT NULL,
   rating	 		    char(1),
   date_added	 		date NOT NULL,
   date_published 		date NOT NULL,
   number_in_series 	int(3)
   );

create table authors
  (aID	     		char(36) PRIMARY KEY,
   firstname		varchar(20) NOT NULL,
   lastname		    varchar(20) NOT NULL
   );

create table book_author
  (isbn		char(13) NOT NULL,
   aID		char(36) NOT NULL,
   CONSTRAINT FOREIGN KEY (isbn) REFERENCES books(isbn),
   CONSTRAINT FOREIGN KEY (aID) REFERENCES authors(aID)
   );

create table publisher
  (pID			char(36) NOT NULL PRIMARY KEY,
   publisher	varchar(64) NOT NULL
   );

create table book_publisher
  (isbn		char(13) NOT NULL,
   pID		char(36) NOT NULL,
   CONSTRAINT FOREIGN KEY (isbn) REFERENCES books(isbn),
   CONSTRAINT FOREIGN KEY (pID) REFERENCES publisher(pID)
   );

create table genre
  (gID		char(36)  NOT NULL PRIMARY KEY,
   genre	varchar(32) NOT NULL);

create table book_genre
  (isbn		char(13) NOT NULL,
   gID		char(36) NOT NULL,
   CONSTRAINT FOREIGN KEY (isbn) REFERENCES books(isbn),
   CONSTRAINT FOREIGN KEY (gID) REFERENCES genre(gID)
   );

create table series
(
    sID             char(36) NOT NULL PRIMARY KEY,
    seriesName      varchar(225) NOT NULL
);

create table book_series
(
    isbn		char(13) NOT NULL,
    sID		    char(36) NOT NULL,
    CONSTRAINT FOREIGN KEY (isbn) REFERENCES books(isbn),
    CONSTRAINT FOREIGN KEY (sID) REFERENCES series(sID)
);

create table accounts
(
    uID			char(36) NOT NULL PRIMARY KEY,
    email		varchar(100) NOT NULL,
    password	varchar(50) NOT NULL
);

create table account_books
(
    uID		    char(36) NOT NULL,
    isbn		char(13) NOT NULL,
    CONSTRAINT FOREIGN KEY (isbn) REFERENCES books(isbn),
    CONSTRAINT FOREIGN KEY (uID) REFERENCES accounts(uID)
);
