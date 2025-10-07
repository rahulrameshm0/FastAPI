import random

from fastapi import FastAPI, HTTPException
import random

app = FastAPI()


quotes = ['I love you the more in that I believe you had liked me for my own sake and for nothing else.',
         'But man is not made for defeat. A man can be destroyed but not defeated.',
         'When you reach the end of your rope, tie a knot in it and hang on.',
         'There is nothing permanent except change.',
         'You cannot shake hands with a clenched fist.']
@app.get('/')
async def random_quotes():
    quote = random.choice(quotes)
    return {"Today Quote": quote}