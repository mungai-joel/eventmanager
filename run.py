from app import app


if __name__ == '__main__':
    app.secret_key = "secretkey4321"
    app.run(debug=True)