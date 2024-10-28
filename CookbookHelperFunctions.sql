
## USER FUNCTIONS

# get user function
delimiter $$ 
create function getUser(id INT) returns varchar(30)
DETERMINISTIC
READS SQL DATA
begin 
	declare username varchar(30);
	select users.username into username
    from users 
    where userid = id;
    return username;
end $$
delimiter ; 

# example running
-- select getUser(1); 


# get ID from username 
delimiter $$ 
create procedure getId(func_user_name varchar(30), out user_id int)
begin 
	set user_id = 0;
	select users.userid into user_id
    from users
    where users.username = func_user_name;
end $$ 
delimiter ; 

-- call getId('keysmasher', @user_id); 
-- select @user_id;

# get Email from user or ID
delimiter //
create procedure getEmail(in id int, out user_email varchar(30))
begin
    select email into user_email
    from users
    where userid = id;
end //
delimiter ;
# example running 
-- call getEmail(1, @user_email); select @user_email;


# getSettings from id 
delimiter $$ 
create procedure getSettings(in id int, out user_settings varchar(100))
begin
	select settings into user_settings
    from users
    where userid = id;
end $$
delimiter ;

# Example calling
-- call getSettings(1, @user_settings); 
-- select @user_settings

# get logfile from id
delimiter $$ 
create procedure getLogfile(in id int, out user_logfile varchar(100))
begin
	select `logfile` into user_logfile
    from users
    where userid = id;
end $$
delimiter ;

-- call getLogfile(1, @user_logfile); 
-- select @user_logfile;


# get followers
delimiter $$ 
create procedure getFollowers(in id int, out user_followers varchar(100))
begin
	select followers into user_followers
    from users
    where userid = id;
end $$
delimiter ;

-- call getFollowers(1, @user_followers); 
-- select @user_followers;

# get following
delimiter $$ 
create procedure getFollowing(in id int, out user_following varchar(100))
begin
	select `following` into user_following
    from users
    where userid = id;
end $$
delimiter ;

-- call getFollowing(1, @user_following); 
-- select @user_following;

# get bookmarks
delimiter $$ 
create procedure getBookmarks(in id int, out user_bookmarks varchar(100))
begin
	select bookmarks into user_bookmarks
    from users
    where userid = id;
end $$
delimiter ;

-- call getBookmarks(1, @user_bookmarks); 
-- select @user_bookmarks;

# set user
delimiter //
create procedure setUser(in id int, in new_username varchar(30), out updated_username varchar(30))
begin
	update users
    set username = new_username
    where userid = id;
    
    select username into updated_username
    from users 
    where userid = id;
end //
delimiter ;

-- call setUser(1, "testerman", @updated_username);	
-- select @updated_username;

# set email
delimiter //
create procedure setEmail(in id int, in new_email varchar(30), out updated_email varchar(30))
begin
	update users
    set email = new_email
    where userid = id;
    
    select email into updated_email
    from users 
    where userid = id;
end //
delimiter ;

-- call setEmail(1, 'testingmantester@gmail.com' , @updated_email);	
-- select @updated_email;

# set password
delimiter // 
create procedure setPassword(in id int, in new_password varchar(100), out updated_password varchar(100)
)
begin
	update users
    set pass = new_password
    where userid = id;
    
    select pass into updated_password
    from users 
    where userid = id;
end //
delimiter ;

-- call setPassword(1, 'newtestingpassword' , @updated_password);	
-- select @updated_password;


## POSTS
# get creator
delimiter $$ 
create procedure getCreator(in post_id int, out post_creator varchar(30))
begin
	select creator into post_creator
    from posts
    where postid = post_id;
end $$
delimiter ;

-- call getCreator(1, @post_creator); 
-- select @post_creator;

# get title
delimiter $$ 
create procedure getTitle(in post_id int, out post_title varchar(30))
begin
	select title into post_title
    from posts
    where postid = post_id;
end $$
delimiter ;

-- call getTitle(1, @post_title); 
-- select @post_title;





