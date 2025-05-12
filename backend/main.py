from core.server import app

if __name__ == "__main__":
    import uvicorn  # type: ignore

    uvicorn.run(
        "core.server:app", http="httptools", proxy_headers=True, server_header=False
    )
