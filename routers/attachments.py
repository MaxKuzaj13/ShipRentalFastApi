from fastapi import APIRouter, UploadFile

router = APIRouter(prefix='/attachments', tags=['attachments'])

@router.post("/files", status_code=201)
async def create_upload_file(file: UploadFile):
    with open(file.filename, 'wb') as handler:
        handler.write(await file.read())
    return {"filename": file.filename, "Content-Type": file.content_type}
