import flask

app = flask.Flask("sad")

@app.get("/")
def root():
    return {"ping": "pong"}
