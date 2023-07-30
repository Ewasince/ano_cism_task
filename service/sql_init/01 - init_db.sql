-- create user
CREATE ROLE cism_user LOGIN PASSWORD 'cism_user';


-- create db
CREATE DATABASE "USERS_DB" WITH OWNER = cism_user;


-- grant user cism_user access to db 'USERS_DB'
GRANT ALL ON DATABASE "USERS_DB" TO "cism_user";

--
