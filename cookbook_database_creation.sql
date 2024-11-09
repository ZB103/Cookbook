-- create scheme

CREATE SCHEMA `cookbook_database`;

--------------------------------------------------------- 
-- create table

CREATE  TABLE users (
 userid int NOT NULL AUTO_INCREMENT PRIMARY KEY, -- create user id variable that cannot be null and will auto_increment and is the primary key
 username varchar(30) not null unique,  -- create username var, cant be null and is unique
 pass varchar(30) not null,  							-- create password var, cant be null, is not unique
 email varchar(30) unique, 							-- create email var, can be null (optional) and is unique 
 displayname varchar(30), 							-- create displayname var, cant be null (optional) and is not unique 
 settings varchar(500) not null, -- unique, commented out until needed
 `logfile` varchar(500) not null, -- unique, commented out until needed
 followers VARCHAR(500) NOT NULL default 0,
 `following` VARCHAR(500) NOT NULL default 0,
 bookmarks VARCHAR(500) NOT NULL default 'empty'
); 								

-- Example insertion into table

-- INSERT INTO users (username, pass, email, settings, `logfile`) VALUES ('testerman', 'testing', 'testerman@testing.com','settings_dir', 'logfile_dir');

-- Example update on table
-- update users set email = 'bobbysux@bobbyflay.com' where userid = 3;

-- fills default constraint of displayname using username
-- UPDATE users SET displayname = username WHERE displayname IS NULL;


--------------------------------------------------------- 

-- create table 

CREATE TABLE posts
(
postid int NOT NULL AUTO_INCREMENT PRIMARY KEY,
post_creator varchar(30) not null, 
-- ## consider adding a check that post creator has to be in users/usernames or making this column user userid
post_title varchar(30) not null,
post_path varchar(500) not null unique,
post_image varchar(500), -- can be null
tags JSON,
likes int default 0
)
AUTO_INCREMENT = 100;

-- example insertion
-- INSERT INTO posts (post_creator, post_title, post_path, post_image)
-- VALUES ('testerman', 'sometestedfood', 
-- 'etc/banana/notbananas/food/sometestedfood','etc/banana/notbananas/food/sometestedfoodimage');

--------------------------------------------------------- 

-- To view a table 
Select * from users; 										-- select all from users

