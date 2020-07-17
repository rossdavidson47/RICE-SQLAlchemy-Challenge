# 1. import Flask
from flask import Flask

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Hello, world! Welcome to my API")
    return "Hello, world! Welcome to my API. This is Ross."

# 4. Define what to do when a user hits the about route
@app.route("/about")
def about():
    print("This is Ross, I am not at home.")
    return "This is Ross, I am not at home. I am in Colorado"

# 5. Define what to do when a user hits the contact route
@app.route("/contact")
def contact():
    print("Please don't call me.")
    return "I am checking my email cgabubga."

# Finally, add code at the bottom of the file that allows you to run the server from the command line with: python app.py.
if __name__ == "__main__":
    app.run(debug=True)

