import httpx


async def call_ml_model(data: dict):
    # Exercise model endpoint
    url = "https://exercise-plan-production.up.railway.app/predict"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        response.raise_for_status()
        return response.json()
