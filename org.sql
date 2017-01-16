CREATE TABLE organizations (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE employees (
  id SERIAL PRIMARY KEY,
  organizationid INTEGER NOT NULL REFERENCES organizations(id),
  name TEXT NOT NULL
);

-- Populate sample data

INSERT INTO organizations (name) VALUES ('ACME Inc');
INSERT INTO organizations (name) VALUES ('Daily Planet');
INSERT INTO organizations (name) VALUES ('Stark Industries');

INSERT INTO employees (organizationid, name) VALUES (1, 'Bugs Bunny');
INSERT INTO employees (organizationid, name) VALUES (1, 'Road Runner');
INSERT INTO employees (organizationid, name) VALUES (2, 'Clark Kent');
INSERT INTO employees (organizationid, name) VALUES (2, 'Louis Lane');
INSERT INTO employees (organizationid, name) VALUES (3, 'Howard Stark');