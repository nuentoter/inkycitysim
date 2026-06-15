from fastapi import FastAPI, WebSocket
import asyncio
import random
import json

app = FastAPI()

time_tick = 0

npcs = {
    "Harold Pike": {"x": 5, "y": 5, "A": 0.55, "B": 0.35, "C": 0.10},
    "Daniel Cross": {"x": 2, "y": 7, "A": 0.60, "B": 0.30, "C": 0.10},
}

case = {
    "Identity split behavior": 0.45,
    "Single operator error": 0.40,
    "External substitution": 0.15
}

feed = []


def step_simulation():
    global time_tick
    time_tick += 1

    feed.clear()

    for name, npc in npcs.items():

        if random.random() < 0.4:
            npc["x"] += random.choice([-1, 0, 1])
            npc["y"] += random.choice([-1, 0, 1])

        npc["x"] = max(0, min(9, npc["x"]))
        npc["y"] = max(0, min(9, npc["y"]))

        drift = random.random() * 0.05
        npc["A"] = max(0.1, npc["A"] + random.choice([-drift, drift]))
        npc["B"] = max(0.1, npc["B"] + random.choice([-drift, drift]))

        total = npc["A"] + npc["B"] + npc["C"]
        npc["A"] /= total
        npc["B"] /= total
        npc["C"] /= total

        if random.random() < 0.3:
            feed.append(f"{name} observed at ({npc['x']},{npc['y']})")

        case["Identity split behavior"] += npc["B"] * 0.01

    normalize_case()


def normalize_case():
    total = sum(case.values())
    for k in case:
        case[k] /= total


def get_state():
    return {
        "time": time_tick,
        "npcs": npcs,
        "case": case,
        "feed": feed
    }


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    while True:
        step_simulation()
        await ws.send_text(json.dumps(get_state()))
        await asyncio.sleep(0.8)
