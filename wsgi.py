from app import create_app

if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True,host="127.0.0.1", port=8002)