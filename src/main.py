from fastapi import FastAPI, Request
from routes.recognise_user import router as recognise_user
from routes.add_user import router as add_user
from exception.exceptions import BaseException
from fastapi.responses import JSONResponse

app = FastAPI(title="Facial Recognition System")

@app.exception_handler(BaseException)
async def base_handler(req: Request, err: BaseException):
    return JSONResponse(
        status_code=err.status_code,
        content=err.detail
    )

@app.exception_handler(Exception)
async def general_handler(req: Request, err: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error_code": 500,
            "message": str(err)
        }
    )

app.include_router(recognise_user, prefix="/api")
app.include_router(add_user, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)