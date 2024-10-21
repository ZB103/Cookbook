-- triggers for displayname syncing, and password hashing
delimiter // 
CREATE TRIGGER DisplayNameDefault before INSERT on users
for each row BEGIN
	set NEW.displayname = NEW.username; 
end 
//

delimiter //
CREATE TRIGGER PasswordHashing before insert on users
for each row BEGIN
	set NEW.pass = md5(new.pass);
end;
//
delimiter //
create trigger PasswordHashingUpdate before update on users
for each row BEGIN
	set NEW.pass = md5(new.pass);
end;
//
