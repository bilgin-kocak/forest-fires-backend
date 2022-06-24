from fastapi import FastAPI, HTTPException
import requests
import json
 
URL = "https://www.ogm.gov.tr/tr/orman-yanginlari"

from model import Todo

# an HTTP-specific exception class  to generate exception information

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:3000",
]

# what is a middleware? 
# software that acts as a bridge between an operating system or database and applications, especially on a network.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World1"}


@app.get("/forest-fire")
async def get_forest_fires():
    r = requests.get(URL)
    content = r.content.decode("utf-8") 
    view_name = "ForestFiresView"
    index = content.find(view_name)
    first_index = index + len(view_name)
    i = 0
    while True:
        if content[first_index + i] == "{":
            print(content[first_index + 1])
            break
        first_index += 1
    new_cont = content[first_index:]
    last_index = new_cont.find('),')
    res = new_cont[:last_index]


    res = res.replace('initialState','\"initialState\"')
    res = res.replace('items','\"items\"')
    res = json.loads(res)

    return res['initialState']['items'][0]
