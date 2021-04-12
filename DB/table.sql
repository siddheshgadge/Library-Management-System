drop database if exists library;

create database library;

use library;

create table books(

bookId int unsigned primary key,
bookTitle varchar(50) not null,
bookAuthor varchar(20) not null,
bookISBN bigint unsigned,
bookQuantity int not null,
UNIQUE(bookISBN)

);

create table issueDetails(

issueId int unsigned primary key auto_increment,
bookId int unsigned not null,
reader varchar(20) not null,
contact bigint(10),
issueDate date,
returnDate varchar(20),
foreign key(bookId) references books(bookId) ON DELETE CASCADE ON UPDATE CASCADE

);


