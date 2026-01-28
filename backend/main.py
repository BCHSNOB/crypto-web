from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from crypto_utils import aes_encrypt, aes_decrypt
from key_manager import derive_key
import io

app = FastAPI(title="Crypto Web API")

@app.post("/encrypt")
async def encrypt_file(
    file: UploadFile = File(...),
    password: str = Form(...)
):
    data = await file.read()
    key = derive_key(password)
    encrypted = aes_encrypt(data, key)

    return StreamingResponse(
        io.BytesIO(encrypted),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={file.filename}.enc"
        }
    )

@app.post("/decrypt")
async def decrypt_file(
    file: UploadFile = File(...),
    password: str = Form(...)
):
    data = await file.read()
    key = derive_key(password)
    decrypted = aes_decrypt(data, key)

    return StreamingResponse(
        io.BytesIO(decrypted),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename=decrypted_{file.filename}"
        }
    )
