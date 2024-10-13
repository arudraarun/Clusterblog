from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel

app = FastAPI()

# Set up Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = MongoClient("mongodb+srv://arunmuthujothiraj:PWr3TM96UAaO7rLI@clusterblog.rt5pb.mongodb.net/?retryWrites=true&w=majority&appName=clusterblog")
db = client['clusterblog_db']  # Use your database name
collection = db['user_messages']  # Use your collection name

# Model to define the expected input structure
class Message(BaseModel):
    user_name: str
    user_message: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
async def submit(message: Message):
    new_message = {"user_name": message.user_name, "user_message": message.user_message}
    collection.insert_one(new_message)

    # Retrieve all documents from the collection
    all_documents = list(collection.find())
   
    # Convert ObjectId to string for JSON response
    for doc in all_documents:
        doc["_id"] = str(doc["_id"])

    return JSONResponse(content=all_documents)
