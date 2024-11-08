
## USER FUNCTIONS

# get user function
delimiter $$ 
create function getUser(id INT) returns varchar(30)
DETERMINISTIC
READS SQL DATA
begin 
	declare username varchar(30);		-- variable declaration
	select users.username into username	-- select username from table, using id 
	from users 
    	where userid = id;
    	return username;			-- return username
end $$
delimiter ; 

# example running
-- select getUser(1); 


# get ID from username 
delimiter $$ 
create procedure getId(func_user_name varchar(30), out user_id int)
begin 
	set user_id = 0;				-- variable declaration and default
	select users.userid into user_id		-- select username from table
    	from users
    	where users.username = func_user_name;
end $$ 
delimiter ; 

# example running
-- call getId('keysmasher', @user_id);
# example usage if value needs to be referenced after running
-- select @user_id;

# get Email from user or ID
delimiter //
create procedure getEmail(in id int, out user_email varchar(30))
begin
    select email into user_email		-- selects email from table and returns it as user_email
    from users
    where userid = id;
end //
delimiter ;

# example running 
-- call getEmail(1, @user_email); 
-- select @user_email;


# getSettings directory from id 
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

# get logfile directory from id
delimiter $$ 
create procedure getLogfile(in id int, out user_logfile varchar(100))
begin
	select `logfile` into user_logfile
    	from users
    	where userid = id;
end $$
delimiter ;

# example running
-- call getLogfile(1, @user_logfile); 
-- select @user_logfile;


# get followers, returns directory for followers 
delimiter $$ 
create procedure getFollowers(in id int, out user_followers varchar(100))
begin
	select followers into user_followers
    	from users
    	where userid = id;
end $$
delimiter ;

# example calling 
-- call getFollowers(1, @user_followers); 
-- select @user_followers;

# get following, returns directory for following
delimiter $$ 
create procedure getFollowing(in id int, out user_following varchar(100))
begin
	select `following` into user_following
    from users
    where userid = id;
end $$
delimiter ;

# example calling
-- call getFollowing(1, @user_following); 
-- select @user_following;

# get bookmarks directory from id 
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
setUser: begin
	declare if_username varchar(30);					-- variable declaration
	select username into if_username from users where userid = id; 		-- selects username into if_username for comparison

	if if_username = concat("deleted_user", id) then leave setUser;		-- checks if a user is already deleted, if so leave setUser (aka do not change username)
    	end if;
    
	update users					-- update and select statements for changing and updating the username 
    	set username = new_username
    	where userid = id;
    
    	select username into updated_username
    	from users 
    	where userid = id;
end //
delimiter ;

# example calling
-- call setUser(1, "testerman", @updated_username);	
-- select @updated_username;

# set email
delimiter //
create procedure setEmail(in id int, in new_email varchar(30), out updated_email varchar(30))
setEmail: begin
	declare if_username varchar(30);					-- variable declaration for comparison 
    	select username into if_username from users where userid = id;
		
	if if_username = concat("deleted_user", id) then leave setEmail;	-- checks for deleted username, and leaves if username deleted 
    	end if;
    
	update users								-- changes and updates the username on the table
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
setPassword: begin
	declare if_pass varchar(100);					-- variable declaration for comparison
	select pass into if_pass from users where userid = id;
	
	if if_pass = md5("archive_password") then leave setPassword;	-- checks if the user has been archived, if so, leave. 
    	end if;
    
	update users							-- changes and updates the variables in the table 
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
	select creator into post_creator		-- returns the creator of the post's username
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
	select title into post_title		-- returns the post's title 
    	from posts
    	where postid = post_id;
end $$
delimiter ;

-- call getTitle(1, @post_title); 
-- select @post_title;

# get postpath
delimiter //
create procedure getPostPath(in post_id int, out postPath varchar(500))
begin
	select post_path into postPath		-- returns directory to the post's path 
    	from posts
    	where postid = post_id;
end //
delimiter ;

-- call getPostPath(100, @postPath);
-- select @postPath; 

# get post image 
delimiter // 
create procedure getPostImage(in post_id int, out postImage varchar(500))
begin
	select post_image into postImage		-- returns the user's profile picture directory
    	from posts
    	where postid = post_id;
end // 
delimiter ;

-- call getPostImage(100, @postImage);
-- select @postImage; 


# get post tags JSON 
delimiter //
create procedure getPostTags(in post_id int, out post_tags JSON)
begin 
	select tags into post_tags		-- returns the json objects of the post's tags 
    	from posts
    	where postid = post_id;
end //
delimiter ; 

-- call getPostTags(100, @post_tags);
-- select @post_tags; 


# Archive profile function
delimiter //
create procedure archiveUser(in id int)
begin
	update users				-- updates the password to the decided archive password 
    	set pass = "archive_password" 
    	where userid = id;
   
    call setEmail(id, Null, @updated_email);	-- and sets the user's email to Null to avoid contact 
end //
delimiter ; 

# example calling 
-- call archiveUser(1); 


# Delete profile function
delimiter //
create procedure deleteUser(in id int)
begin
	update users				-- sets the username to the deleted user distinction
    	set username = CONCAT('deleted_user', id)
    	where userid = id;
    
    	call archiveUser(id);			-- also archives the user. 
end //
delimiter ;

-- call deleteUser(1);




