from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import random
import json

# FastAPI app definition
api_app = FastAPI(
    title="ACROSS API",
    summary="Astrophysics Cross-Observatory Science Support (ACROSS).",
    description="API providing information on various NASA missions to aid in coordination of large observation efforts.",
    contact={
        "email": "support@gcn.nasa.gov",
    }
)

origins = [
    "http://localhost:5000"
]

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api_app.get("/api/v0/hello")
def hello():
    return "API says hello"


# Path for all the static files (compiled JS/CSS, etc.)
@api_app.route("/<path:path>")
def home(path):
    return FileResponse('src/web/client/public', path)

@api_app.get("/")
@api_app.get("/index")
async def read_index():
    return FileResponse("src/web/client/public/index.html")

# Tests Python Flask connection
@api_app.get("/rand")
def get_rand():
    val = str(random.randint(0, 100))
    return val

# Tests Python Flask Svelte connection
@api_app.get("/randData")
def randData(request: Request):
    print('randData')
    params = request.args.get('params')
    randomNumber = random.randint(0, 100)

    data = json.dumps({
        "randomNumber": str(randomNumber), 
        "params": str(int(params)), 
        "sumRandomParams": str(randomNumber + int(params))
        })
    
    print(data)
    return data