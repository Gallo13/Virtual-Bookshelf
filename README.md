# Virtual-Bookshelf
Virtual bookshelf Website using Python, Flask, HTML, and MySQL

This virtual bookshelf uses HTML, CSS, WS-CSS, and Bootstrap on the front end to create and style the website. It also uses Python with Flask to make the backend and connects to MySQL with MySQL connector.

It allows for registration with an email address and adds users to the database. If you are already registered, you are able to log in (and log out). The password is hashed for security. It takes input such as Title, Author, Genre, Publisher, Pages, personal Rating (on a scale of 1-5), and if it is a series, series name, and number in series. That input gets appended to the MySQL database. The books are then associated with an account. If a book exists within the database, it will not add another book, but add it to the account_books table. The database is compliant with 1NF, 2NF, 3NF and 4NF. 

FUTURE:
- It will show analytics on what kind of books I generally read, my average book length and my average book ratings, most read genre, and most read author.
- will have a book recommender for future books based on what I've read

![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/9edf9b2b-a881-489c-8405-c1a0e409bcd9)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/14277c80-b7f8-476c-8b11-796f5a61e547)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/0ce16640-f934-4a2c-9bd8-29ac4960fa32)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/3707fd0f-3d79-479d-91c7-4afc48c1e48f)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/d79f958e-248c-48bb-921b-649438424434)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/7177f3ef-e577-44ce-aa34-01b564258d12)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/c4599664-c833-40e5-a0c2-222c5fcd5f12)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/ba8acd67-ba78-4214-a063-59db6c7048d3)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/6a372335-d4e7-4eba-98ef-91f963a29a5b)

EER Diagram
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/cce6f3c4-9425-4bee-9e83-de47e21b464c)


Next to be done: <br>
(1) Tooltip to show how to input genre and author ("Please use commas to separate multiple genres") <br>
(2) SQL -> Database <br>
(3) Finish recommender system (content filtering) based on title, author, genre, rating of entire library <br>
(4) Give user a choice to select a specific book to have rec sys use to recommend books <br>
(5) Add rest of my books <br>
(6) Create unit test for adding books and rec sys <br>
(7) Have other users test application <br>
(8) Add collaborative filtering on rec sys <br>
(9) add OpenCV for barcode scanner/realtime image detection <br>
