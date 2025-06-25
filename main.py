import uvicorn
from socket_server.ws import sio_app

if __name__ == "__main__":
    uvicorn.run(sio_app, host="0.0.0.0", port=8000)

