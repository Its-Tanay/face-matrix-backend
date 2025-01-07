import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector
import numpy as np
from typing import Optional, Dict, Any
from contextlib import contextmanager

import psycopg2.pool
from exception.exceptions import ServiceUnavailable

class Database:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.init_db()

    @contextmanager
    def get_connection(self):
        try:
            pool = psycopg2.pool.ThreadedConnectionPool(
                4, 10, self.connection_string
            )
            conn = pool.getconn()
            register_vector(conn) 
            yield conn
        except Exception as e:
            raise ServiceUnavailable(message=f"Database connection failed") from e
        finally:
            if 'conn' in locals():
                conn.close()

    def init_db(self):
        from database.queries import (
            ENABLE_VECTOR_EXTENSION,
            CREATE_USER_TABLE,
            CREATE_VECTOR_INDEX,
            CREATE_CACHE_TABLE
        )
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(ENABLE_VECTOR_EXTENSION)
                cur.execute(CREATE_USER_TABLE)
                cur.execute(CREATE_VECTOR_INDEX)
                cur.execute(CREATE_CACHE_TABLE)
            conn.commit()

    async def add_user(self, user_id: str, name: str, birthdate: str, face_vectors: np.ndarray) -> Dict[str, Any]:
        from database.queries import INSERT_USER
        
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(INSERT_USER, (
                        user_id,
                        name,
                        birthdate,
                        face_vectors 
                    ))
                    result = cur.fetchone()
                conn.commit()
                return dict(result)
        except Exception as e:
            raise ServiceUnavailable(message="Failed to add user") from e

    async def find_similar_faces(self, vectors: np.ndarray, threshold: float) -> Optional[Dict[str, Any]]:
        from database.queries import FIND_SIMILAR_FACE
        
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(FIND_SIMILAR_FACE, (vectors, vectors))
                    result = cur.fetchone()
                    
                    if result and float(result['similarity']) >= threshold:
                        return {
                            'id': result['id'],
                            'name': result['name']
                        }
                    return None
        except Exception as e:
            raise ServiceUnavailable(message="Failed to search for similar faces") from e
        
    async def cache_vectors(self, vectors: np.ndarray, key: str) -> Optional[str]:
        from database.queries import CACHE_VECTORS
        try : 
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(CACHE_VECTORS, (
                        key,
                        vectors 
                    ))
                    result = cur.fetchone()
                conn.commit()
                return dict(result)

        except Exception as e:
            raise ServiceUnavailable(message="Failed to add vectors to the cache") from e
        
    async def get_cached_vectors(self, key: str) -> Optional[np.ndarray]: 
        from database.queries import GET_CACHED_VECTORS
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(GET_CACHED_VECTORS, [key])
                    result = cur.fetchone()
                    return result if result else None
        except Exception as e:
            raise ServiceUnavailable(message=f"Failed to retrieve cached vectors") from e
        
    async def delete_cached_vectors(self, key: str) -> None:
        from database.queries import DELETE_CACHED_VECTORS
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(DELETE_CACHED_VECTORS, [key])
                conn.commit()
        except Exception as e:
            raise ServiceUnavailable(message="Failed to delete cached vectors") from e