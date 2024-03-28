from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/device/{deviceInfo}")
async def hello(deviceInfo : str):
    return {f"DeviceOS_Version": f"{deviceInfo}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")