from os import stat
from typing import Optional
from dns.resolver import query
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from time import sleep
import mysql.connector

while(True):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="fastapi",
            password="fastapi",
            database="fastapi",
        )
        cursor = conn.cursor()
        break
    except Exception as e:
        print("Unable to connect to the mysql server.")
        print("ERROR: ",e)
        sleep(4)


app = FastAPI()

class post_schema(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

def format_post(post: list):
    return {
        "id": post[0],
        "title":post[1],
        "content":post[2],
        "published" : "true" if post[3] else "false",
        "timestamp" : str(post[4])
    }


@app.get("/")
def read_root():
    return {"Message": "Welcome to my API, go to /docs for documentation."}

@app.get("/posts")
def get_posts():
    query = """SELECT * from `posts`"""
    cursor.execute(query)
    all_posts = cursor.fetchall()
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail=list(map(format_post,map(list,all_posts)))
    )

@app.get("/post/{id}")
def get_post(id: int):
    # query = "SELECT * from `posts` WHERE `id` = %s"
    cursor.execute("SELECT * from `posts` WHERE `id` = %s",(id,))
    post = cursor.fetchone()
    if(post):
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=format_post(list(post))
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="404: Post not found"
        )

@app.post("/create")
def create_post(post_data: post_schema):
    cursor.execute("""
    INSERT INTO `posts` (`id`, `title`, `content`, `published`, `timestamp`) 
    VALUES (NULL, %s, %s, %s, CURRENT_TIMESTAMP)
    """,(post_data.title, post_data.content, int(post_data.published),))
    conn.commit()
    cursor.execute("SELECT * FROM `posts` WHERE `id` = last_insert_id()") 
    result = cursor.fetchone()
    post = {
        "id" : result[0],
        "title" : result[1],
        "content" : result[2],
        "published" : "true" if result[3] else "false",
        "timestamp" : str(result[4])
    }
    raise HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail=post
    )

@app.delete("/post/{id}")
def delete_post(id: int):
    cursor.execute("SELECT * from `posts` WHERE `id` = %s",(id,))
    post = cursor.fetchone()
    if(post):
        cursor.execute("DELETE FROM `posts` WHERE `id` = %s",(id,))
        conn.commit()
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="404: Post not found"
    )

@app.put("/post/{id}")
def update_post(id: int, post_data: post_schema):
    # update_query = f""""""
    # check_query = f""

    cursor.execute("select * from `posts` where `id` = %s",(id,))
    if(cursor.fetchone()):
        cursor.execute("update `posts` set `title` = %s, `content` = %s, `published` = %s, `timestamp` = CURRENT_TIMESTAMP where `id` = %s",(post_data.title, post_data.content, int(post_data.published), id,))
        conn.commit()
        cursor.execute("select * from `posts` where `id` = %s",(id,))
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=format_post(cursor.fetchone())
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="404: Post not found"
        )
                