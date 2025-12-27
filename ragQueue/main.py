from dotenv import load_dotenv
load_dotenv()
from .server import app
import uvicorn
def main():
    uvicorn.run(app, port=8000)
    
main()    