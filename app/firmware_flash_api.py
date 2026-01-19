from fastapi import FastAPI, UploadFile

from library.arduino_helper import detect_arduino_port, detect_board, flash_firmware

app = FastAPI()

@app.post("/flash")
def flash_device(firmware: UploadFile):
    port = detect_arduino_port()
    if not port:
        return {"status": "error", "message": "No Arduino detected"}

    board = detect_board(port)

    firmware_path = f"/tmp/{firmware.filename}"
    with open(firmware_path, "wb") as f:
        f.write(firmware.file.read())

    result = flash_firmware(port, board, firmware_path)

    return {
        "port": port,
        "board": board,
        "result": result
    }
