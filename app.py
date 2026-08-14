import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()

app = create_app(os.getenv("FLASK_ENV", "development"))

if __name__ == "__main__":
    # Changed 0.0.0.1 to 127.0.0.1
    app.run(host="127.0.0.1", port=5000, debug=app.config.get("DEBUG", False))