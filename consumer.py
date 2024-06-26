from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import requests
import uvicorn


class WeatherRequest(BaseModel):
    q: str
    appid: str
    units: str


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float


app = FastAPI()


API_KEY = '8e3a6f58c981d328d0d7342e58b8d5bb'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


@app.get("/")
def read_root():
    return {'message': 'API to get a city weather'}


@app.get("/weather")
def get_weather(city: str = Query(..., example="Pereira")):
    params = WeatherRequest(q=city, appid=API_KEY, units='metric')
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")
    else:
        data = response.json()
        return WeatherResponse(
            city=city,
            temperature=data['main']['temp'],
            description=data['weather'][0]['description'],
            humidity=data['main']['humidity'],
            wind_speed=data['wind']['speed']
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8801)
