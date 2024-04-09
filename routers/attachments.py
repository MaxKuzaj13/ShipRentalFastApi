import os
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter(prefix='/attachments', tags=['attachments'])

# Folder path where files will be saved
UPLOAD_FOLDER = "uploads"

# Ensure the folder exists or create it if it doesn't
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@router.post("/files", status_code=201)
async def create_upload_file(file: UploadFile = File(...)):
    """
    Handle POST requests to upload and save files on the server.

    Parameters:
    - file: Represents the uploaded file. It is of type UploadFile from FastAPI's File module.

    Returns:
    - Dict: Information about the saved file, including filename and content type.
    """
    # Construct the file path by concatenating the folder path with the file name
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        # Attempt to write the file to disk
        with open(file_path, 'wb') as handler:
            handler.write(await file.read())
        # Return information about the saved file
        return {"filename": file.filename, "Content-Type": file.content_type}
    except Exception as e:
        # Raise an HTTP 500 server error with details of the error if saving fails
        raise HTTPException(status_code=500, detail=str(e))

