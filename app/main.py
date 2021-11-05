from os import stat
from typing import Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

class post_schema(BaseModel):
    title: str
    content: str
    # publish: Optional[bool] = True
filename = "myposts.json"
file = open(filename,"r")
data = file.read()
file.close()
if(len(data)):
    myPosts = json.loads(data)
else:
    myPosts = {"posts":[]}

def format_post(post_data: post_schema):
    if(len(myPosts["posts"])):
        id = myPosts["posts"][-1]["id"] + 1
    else:
        id = 1
    return  {
        "id" : id,
        "data" : {
            "title" : post_data.title,
            "content": post_data.content
        }
    }

def update_db():
    with open(filename,"w") as file:
        file.write(json.dumps(myPosts,indent=2))

@app.get("/")
def read_root():
    return {"Message": "Welcome to my API, go to /docs for documentation."}

@app.get("/posts")
def get_posts():
    if(not len(myPosts["posts"])):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found"
        )
    return myPosts

@app.get("/post/{id}")
def get_post(id: int):
    if(not len(myPosts["posts"])):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail={"No posts found"}
        )
    for post in myPosts["posts"]:
        if(post["id"]==id):
            return post
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )

@app.post("/create")
def create_post(post_data: post_schema):
    mydict =  format_post(post_data)
    myPosts["posts"].append(mydict)
    update_db()
    raise HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail=mydict
    )

@app.delete("/post/{id}")
def delete_post(id: int):
    for i,post in enumerate(myPosts["posts"]):
        if(post["id"]==id):
            myPosts["posts"].pop(i)
            update_db()
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )

@app.put("/post/{id}")
def update_post(id: int, post_data: post_schema):
    if(not len(myPosts["posts"])):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail={"No posts found"}
        )
    for i,post in enumerate(myPosts["posts"]):
        if(post["id"]==id):
            # myPosts["posts"].pop(i)
            myPosts["posts"][i]["data"]["title"] = post_data.title
            myPosts["posts"][i]["data"]["content"] = post_data.content
            update_db()
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )