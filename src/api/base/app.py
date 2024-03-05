from fastapi import FastAPI


# FastAPI app definition
api_app = FastAPI(
    title="ACROSS API",
    summary="Astrophysics Cross-Observatory Science Support (ACROSS).",
    description="API providing information on various NASA missions to aid in coordination of large observation efforts.",
    contact={
        "email": "support@gcn.nasa.gov",
    },
    root_path="/api/v0",
)

@api_app.get("/api/v0/hello")
def hello():
    return "API says hello"