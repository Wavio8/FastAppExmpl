from fastapi import APIRouter, HTTPException
import httpx

from app.schemas import IrisFeatures, IrisPredictResponse

router = APIRouter(
    prefix="/ml",
    tags=["ml"],
)


@router.post("/iris-predict", response_model=IrisPredictResponse)
async def iris_predict(features: IrisFeatures):
    payload = {
        "instances": [
            {
                "sepal_length": features.sepal_length,
                "sepal_width": features.sepal_width,
                "petal_length": features.petal_length,
                "petal_width": features.petal_width,
            }
        ]
    }

    # через INGRESS по HTTPS
    url = "https://iris.k8s.labs.itmo.loc/predict"

    try:
        async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
            resp = await client.post(url, json=payload)
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Cannot reach iris inference service: {e}",
        )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Inference service returned {resp.status_code}: {resp.text}",
        )

    data = resp.json()
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])

    return IrisPredictResponse(
        predictions=data.get("predictions", []),
        latency_sec=data.get("latency_sec"),
    )
