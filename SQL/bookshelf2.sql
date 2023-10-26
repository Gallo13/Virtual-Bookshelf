create database bookshelf2;

use bookshelf2;

DROP TABLE IF EXISTS books, authors, book_author, publisher, book_publisher, book_courses, genre, book_genre;  /* cleanup old stuff */

create table books
  (bID		 char(36) NOT NULL PRIMARY KEY,	 
   title	 varchar(225) NOT NULL,		
   pages	 smallint(5) NOT NULL, 
   rating	 char(1),
   date_added	 date NOT NULL,
   number_in_series 	 int(3));


create table authors
  (aID	     	char(36) PRIMARY KEY,
   firstname	varchar(20) NOT NULL,
   lastname	varchar(20) NOT NULL);

create table book_author
  (bID		char(36) NOT NULL,
   aID		char(36) NOT NULL,
   CONSTRAINT FOREIGN KEY (bID) REFERENCES books(bID),
   CONSTRAINT FOREIGN KEY (aID) REFERENCES authors(aID));


create table publisher
  (pID		char(36) NOT NULL PRIMARY KEY,
   publisher	varchar(64) NOT NULL);

create table book_publisher
  (bID		char(36) NOT NULL,
   pID		char(36) NOT NULL,
   CONSTRAINT FOREIGN KEY (bID) REFERENCES books(bID),
   CONSTRAINT FOREIGN KEY (pID) REFERENCES publisher(pID));

create table book_courses
  (bID		char(36) NOT NULL,
   dept		char(3) NOT NULL,
   course	char(32),
   CONSTRAINT FOREIGN KEY (bID) REFERENCES books(bID));

create table genre
  (gID		char(36)  NOT NULL PRIMARY KEY,
   genre	varchar(32) NOT NULL);

create table book_genre
  (bID		char(36) NOT NULL,
   gID		char(36) NOT NULL,
   CONSTRAINT FOREIGN KEY (bID) REFERENCES books(bID),
   CONSTRAINT FOREIGN KEY (gID) REFERENCES genre(gID));

create table series
(
	sID char(36) NOT NULL PRIMARY KEY,
    seriesName varchar(225) NOT NULL
);

create table book_series
(
	bID		char(36) NOT NULL,
    sID		char(36) NOT NULL,
    CONSTRAINT FOREIGN KEY (bID) REFERENCES books(bID),
    CONSTRAINT FOREIGN KEY (sID) REFERENCES series(sID)
);
