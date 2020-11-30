from api.app import create_app

app = create_app("api.settings")

if __name__ == "__main__":
    app.run(port=9000)
