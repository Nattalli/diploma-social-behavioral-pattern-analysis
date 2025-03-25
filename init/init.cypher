LOAD CSV WITH HEADERS FROM 'file:///users.csv' AS row
CREATE (:User {id: row.id, name: row.name});

LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
MATCH (a:User {id: row.source}), (b:User {id: row.target})
CREATE (a)-[r:FRIENDS_WITH]->(b);
