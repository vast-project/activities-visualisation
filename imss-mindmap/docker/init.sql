CREATE DATABASE tasks_f755;
GRANT ALL PRIVILEGES ON DATABASE tasks_f755 TO tasksuser_x354;
\c tasks_f755
CREATE TABLE IF NOT EXISTS public.adminusers (
  id serial NOT NULL,
  email character varying COLLATE pg_catalog."default" NOT NULL,
  password character varying COLLATE pg_catalog."default",
  organization integer NOT NULL,
  active integer,
  resetlink character varying COLLATE pg_catalog."default",
  resetlinkexpdate character varying COLLATE pg_catalog."default",
  fullname character varying COLLATE pg_catalog."default",
  phone bigint,
  typeid integer NOT NULL,
  CONSTRAINT adminusers_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;
CREATE TABLE IF NOT EXISTS public.educationlevel (
  id serial NOT NULL,
  level character varying COLLATE pg_catalog."default" NOT NULL,
  CONSTRAINT educationlevel_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;
CREATE TABLE IF NOT EXISTS public.events (
  id serial NOT NULL,
  datetime timestamp without time zone NOT NULL,
  visitor character varying COLLATE pg_catalog."default" NOT NULL,
  noofvisitors integer NOT NULL,
  educationlevel integer NOT NULL,
  CONSTRAINT events_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;
CREATE TABLE IF NOT EXISTS public.organizations (
  id serial NOT NULL,
  name character varying COLLATE pg_catalog."default" NOT NULL,
  phone integer,
  address character varying COLLATE pg_catalog."default",
  frontendurl character varying COLLATE pg_catalog."default" NOT NULL,
  CONSTRAINT organizations_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;
CREATE TABLE IF NOT EXISTS public.usertypes (
  id serial NOT NULL,
  type character varying COLLATE pg_catalog."default" NOT NULL,
  CONSTRAINT usertypes_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;
INSERT INTO adminusers (email, password, organization, active, fullname, typeid) VALUES ('adminuser@vast.org', 'Abc@12345', 1, 1, 'VAST Admin User',1);
INSERT INTO adminusers (email, password, organization, active, fullname, typeid) VALUES ('user@museum.org', 'Abc@12345', 2, 1, 'VAST Admin User',2);
INSERT INTO educationlevel (level) VALUES ('PRIMARY SCHOOL');
INSERT INTO educationlevel (level) VALUES ('HIGH SCHOOL');
INSERT INTO organizations (name, frontendurl) VALUES ('VAST', 'http://localhost:6071/');
INSERT INTO organizations (name, frontendurl) VALUES ('Galileo Museum', 'http://localhost:6071/');
INSERT INTO usertypes (type) VALUES ('VAST User');
INSERT INTO usertypes (type) VALUES ('Organization User');
