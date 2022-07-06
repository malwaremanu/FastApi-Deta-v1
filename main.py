import json, os, requests
from fastapi import FastAPI, Request, Body
from deta import Deta
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = {
    'users' : [
        {
          'name' : 'Manu',
          'password' : '1234',
          'age' : 25,
          'id' : 477
        },
        {
          'name' : 'Pralay',
          'password' : '124567',
          'age' : 32,
          'id' : 478
        },
        {
          'name' : 'Jibin',
          'password' : '124563',
          'age' : 32,
          'id' : 479
        }
    ]
}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/store")
async def store():
    with open('data/db.json', 'w+') as db_file:
        db_file.write(json.dump(db))
    return {"message": "Data Dumped"}

@app.get("/db")
async def database():    
    os.system('cls')
    #jsf= json.load(open('data/db.json').readlines()[0])
    ff = open('data/db.json')
    js = ''
    for f in ff:
        js = f.strip()
    js_data = js.replace("'", '"')

    return {"message": "data fetched successfully", "data" : json.loads(js_data)}


@app.post("/save")
async def save(payload: dict = Body(...)):
    os.system('cls')
    print(payload)
    db['users'].append(payload)
    with open('data/db.json', 'w+') as db_file:
        db_file.write(str(db))
    #return {"message": "Data Dumped"}

    return {"message": "data saved successfully", "data" : db}



# deta = Deta('myProjectKey') # configure your Deta project
# db = deta.Base('simpleDB')  # access your DB
# app = Flask(__name__)