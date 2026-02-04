from app import app

if __name__ == "__main__":
    # Default to port 3001 for Kavia preview. No env vars required.
    app.run(host="0.0.0.0", port=3001, debug=True)
