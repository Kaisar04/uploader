from fastapi import FastAPI, UploadFile, File, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from service import upload_file


app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get("/", response_class=HTMLResponse)
async def get_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@app.post("/upload")
async def upload(
        file: UploadFile = File(...)
):
    for chunk in file.file:
        print(chunk)
    # try:
    #     await parallel_multithreading_upload(file)
    # except Exception:
    #     return {"message": "Something went wrong"}
    # return Response(status_code=200, content="Successfully uploaded")

