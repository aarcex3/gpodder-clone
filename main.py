import uvicorn
from fastapi import FastAPI, status

from routes import router

app = FastAPI(debug=True)
app.include_router(router, prefix='/users',tags=['Users'])

@app.get("/health", status_code=status.HTTP_200_OK,tags=['Health'])
async def health():
    '''
    Check if service is running
    '''
    return {"message": "Service running"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
