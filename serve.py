import uvicorn

if __name__ == "__main__":
    uvicorn.run(app="serve_handler:app", workers=3)
