import json, os, requests
from fastapi import FastAPI, Request, Body
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*"
]

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



class Appointments(BaseModel):
    name: str
    mobile: str
    date : str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/po/{po_no}/{token}")
async def po(po_no, token):    
    reqUrl = "https://po-manu.harperdbcloud.com"

    headersList = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json" 
    }

    try:
        payload_po = json.dumps({
        "operation": "sql",
        "sql": "SELECT * from po.first where PO_NUMBER='SM/" + po_no + "'" 
        })


        payload_products = json.dumps({
            "operation": "sql",
            "sql": "SELECT * from po.uuid where PO_NUMBER='SM/" + po_no + "'" 
        })

        pos = requests.request("POST", reqUrl, data=payload_po,  headers=headersList)
        products = requests.request("POST", reqUrl, data=payload_products,  headers=headersList)


        if len(pos.json()[0]) != 0:                
            payload_party = json.dumps({
                "operation": "sql",
                "sql": "SELECT * from po.parties where PARTY='" + pos.json()[0].get('SUPPLIER') + "'" 
            })
            party = requests.request("POST", reqUrl, data=payload_party,  headers=headersList)

            print(pos.json())

            return {
                "purchase_order": pos.json(),
                "products" : products.json(),
                "party" : party.json(),
                "status" : "success",
            }
        else:
            return {
                "status" : "error",
                "msg" : "We could not find any details associated with PO. Please try other PO."
            }

    except:
        return {
            "status" : "error",
            "msg" : "PO Not Found. Please enter Correct Details."
        }
        

    
    #return {"msg" : po_no}

@app.post("/anju/{operation}")
async def anju(operation, payload = Body()): 
    if operation == "create":
        print("Creating new",payload)
    
    if operation == "update":
        print("updating data")

    data = {
        "operation": operation,
        "schema": "anju",
        "table": "appointments",
        "records": [ payload ]
        }   

    print(data)
    reqUrl = "https://po-manu.harperdbcloud.com"
    headersList = {
    "Authorization": "Bearer bWFsd2FyZW1hbnU6TWFudUBoYXJwZXIx",
    "Content-Type": "application/json" 
    }

    pos = requests.request("POST", reqUrl, data=dict(data),  headers=headersList)
    
    
    return {
        "operation" : operation, 
        "raw_data" : data,
         "data" : pos.json()
    }


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