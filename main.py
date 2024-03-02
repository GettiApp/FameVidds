from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy database to store user data
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists and password is correct
        if username in users and users[username]['password'] == password:
            return redirect(url_for('feed', username=username))
        else:
            return "Invalid username or password. Please try again."
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username is already taken
        if username in users:
            return "Username already taken. Please choose another one."
        else:
            # Add user to database
            users[username] = {'password': password, 'feed': []}
            return redirect(url_for('feed', username=username))
    return render_template('signup.html')

@app.route('/<username>/feed')
def feed(username):
    if username in users:
        user_feed = users[username]['feed']
        return render_template('feed.html', username=username, feed=user_feed)
    else:
        return "User not found."

@app.route('/<username>/create_video', methods=['GET', 'POST'])
def create_video(username):
    if request.method == 'POST':
        video_title = request.form['title']
        video_content = request.form['content']
        
        # Add video to user's feed
        users[username]['feed'].append({'title': video_title, 'content': video_content})
        return redirect(url_for('feed', username=username))
    return render_template('create_video.html')

if __name__ == '__main__':
    app.run(debug=True)
