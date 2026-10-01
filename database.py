import sqlite3

DATABASE = "blog.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def get_all_posts():
    connection = get_connection()

    posts = connection.execute("""
        SELECT *
        FROM posts
        ORDER BY created_at DESC
    """).fetchall()

    connection.close()

    return posts


def get_post(post_id):
    connection = get_connection()

    post = connection.execute(
        """
        SELECT *
        FROM posts
        WHERE id = ?
        """,
        (post_id,)
    ).fetchone()

    connection.close()

    return post


def create_post(title, content, category):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO posts (title, content, category)
        VALUES (?, ?, ?)
        """,
        (title, content, category)
    )

    connection.commit()
    connection.close()


def update_post(post_id, title, content, category):
    connection = get_connection()

    connection.execute(
        """
        UPDATE posts
        SET title = ?, content = ?, category = ?
        WHERE id = ?
        """,
        (title, content, category, post_id)
    )

    connection.commit()
    connection.close()


def delete_post(post_id):
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM posts
        WHERE id = ?
        """,
        (post_id,)
    )

    connection.commit()
    connection.close()
