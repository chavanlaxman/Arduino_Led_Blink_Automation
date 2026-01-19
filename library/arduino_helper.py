import serial.tools.list_ports
import subprocess

def detect_arduino_port():
    """
    This function will auto-detect arduino comp port connected to system
    :return: arduino port ex. COMP3
    """
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "USB" in port.description:
            return port.device
    return None

print(detect_arduino_port())

def detect_board(port):
    # Basic heuristic (can be enhanced)
    if "ttyUSB" in port:
        return "arduino:avr:uno"
    return "unknown"


def flash_firmware(port, board, firmware_path):
    command = [
        "arduino-cli",
        "upload",
        "-p", port,
        "--fqbn", board,
        "--input-file", firmware_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr
    }
