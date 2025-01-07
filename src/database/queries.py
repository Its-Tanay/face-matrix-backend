ENABLE_VECTOR_EXTENSION = """
CREATE EXTENSION IF NOT EXISTS vector;
"""

CREATE_USER_TABLE = """
CREATE TABLE IF NOT EXISTS "user" (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    birthdate DATE NOT NULL,
    face_vectors vector(512) NOT NULL
);
"""

CREATE_CACHE_TABLE = """
CREATE TABLE IF NOT EXISTS "vectors_cache" (
    timestamp timestamp NOT NULL DEFAULT NOW(),
    key VARCHAR PRIMARY KEY,
    face_vectors vector(512) NOT NULL
);
"""

CREATE_VECTOR_INDEX = """
CREATE INDEX IF NOT EXISTS user_face_vectors_idx 
ON "user" USING hnsw (face_vectors vector_cosine_ops);
"""

INSERT_USER = """
INSERT INTO "user" (id, name, birthdate, face_vectors) 
VALUES (%s, %s, %s, %s)
RETURNING id, name, birthdate;
"""

FIND_SIMILAR_FACE = """
SELECT id, name, birthdate, 1 - (face_vectors <=> %s) as similarity
FROM "user"
ORDER BY face_vectors <=> %s
LIMIT 1;
"""

CACHE_VECTORS = """
INSERT INTO vectors_cache (key, face_vectors, timestamp)
VALUES (%s, %s, NOW())
RETURNING key;
"""

GET_CACHED_VECTORS = """
SELECT face_vectors 
FROM vectors_cache 
WHERE key = %s 
"""

DELETE_CACHED_VECTORS = """
DELETE FROM 
vectors_cache 
WHERE key = %s;
"""

"AND timestamp > NOW() - INTERVAL '10 minutes';"