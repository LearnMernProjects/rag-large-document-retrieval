from dotenv import load_dotenv
from .server import app
load_dotenv()
import uvicorn
def main():
    uvicorn.run(app, port=8000)
    
main()    