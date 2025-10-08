from fastapi import FastAPI, HTTPException

weather_data = {
    "Delhi": {"temperature": 30, "condition": "Sunny"},
    "Chennai": {"temperature": 55, "condition": "Sunny"},
    "Mumbai": {"temperature": 40, "condition": "Sunny"},
    "Kerala": {"temperature": 30, "condition": "Cold"},
    "Bangalore": {"temperature": 25, "condition": "smowy"},
}

app = FastAPI()

@app.get('/weather/{city}')
async def weather_datas(city:str):
    if city in weather_data:
        weather = weather_data[city]
        return {"City": city, "Weather": weather['temperature'], 'Condition': weather['condition']}
    raise HTTPException(status_code=404, detail=f"{city} is not found")
