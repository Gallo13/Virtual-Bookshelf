# Virtual-Bookshelf
Virtual bookshelf Website using Python, Flask, HTML, and MySQL

This virtual bookshelf uses HTML, CSS, WS-CSS, and Bootstrap on the front end to create and style the website. It also uses Python with Flask to make the backend and connects to MySQL with MySQL connector.

It allows for registration with an email address and adds users to the database. If you are already registered, you are able to log in (and log out). The password is hashed for security. It takes input such as Title, Author, Genre, Publisher, Pages, personal Rating (on a scale of 1-5), and if it is a series, series name, and number in series. That input gets appended to the MySQL database. The books are then associated with an account. If a book exists within the database, it will not add another book, but add it to the account_books table. The database is compliant with 1NF, 2NF, 3NF and 4NF. 

FUTURE:
- It will show analytics on what kind of books I generally read, my average book length and my average book ratings, most read genre, and most read author.
- will have a book recommender for future books based on what I've read

![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/c53caf3d-c308-4766-b073-8b9fb3a40832)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/1bf020c0-3b6d-4f68-b147-4c8df98e3ccf)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/9980ab4c-f8a0-4c88-bcfc-30e5416d1380)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/0ad74030-5a6f-42b3-81a4-c8d55d9abc5b)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/630e88fc-312b-4fd7-9e6d-f72b76e0fca0)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/b1c83cd9-94a0-42c8-8f87-77545d20e75d)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/af7676b3-326e-44d5-b73c-fe90cac59dac)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/ced2e96b-dd8f-4ff2-98c2-f994047b36a6)
![image](https://github.com/Gallo13/Virtual-Bookshelf/assets/54815820/4799411c-c4ec-4fa0-a16c-8b5c7300174a)


Next to be done: <br>
(1) tooltip to show how to input genre and author ("Please use commas to separate multiple genres") <br>
(2) add chart.js charts to show query results/statistics on books or just use seaborn/matplotlib <br>
(3) add recommender system <be>
(4) add OpenCV for barcode scanner/realtime image detection
