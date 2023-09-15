### Conceptual Exercise

Answer the following questions below:

- What is PostgreSQL?
  PostgreSQL is a free, open source relational database management system.
- What is the difference between SQL and PostgreSQL?
  There are some minor syntactical differences. PostgreSQL is a DMS that uses Structured Query Language. (SQL)
- In `psql`, how do you connect to a database?
  \c <dbName.
- What is the difference between `HAVING` and `WHERE`?
  HAVING applies to rows in a result set representing groups. WHERE represents indifidual rows.
- What is the difference between an `INNER` and `OUTER` join?
  INNER only keeps info. from both tables that are related to eachother. OUTER keeps info from both tables that are not related to eachother. 
- What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?
  Left Outer Join: Returns all the rows from the LEFT table and matching records between both the tables. Right Outer Join: Returns all the rows from the RIGHT table and matching records between both the tables. 
- What is an ORM? What do they do?
  A piece of software designed to translate between the data representations used by databases and those used in object-oriented programming.
- What are some differences between making HTTP requests using AJAX 
  and from the server side using a library like `requests`?
  
- What is CSRF? What is the purpose of the CSRF token?

- What is the purpose of `form.hidden_tag()`?
  It generates a hidden field that includes a token that is used to protect the form against CSRF attacks.
