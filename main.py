import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Load blog posts from the JSON file
def load_blog_posts():
    if os.path.exists('blog_posts.json'):
        with open('blog_posts.json', 'r') as file:
            return json.load(file)
    else:
        return []

# Save blog posts to the JSON file
def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file, indent=4)

# Fetch a specific post by ID
def fetch_post_by_id(post_id):
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None

@app.route('/')
def index():
    # Load the blog posts from the JSON file
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data from the POST request
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Load existing blog posts
        blog_posts = load_blog_posts()

        # Create a new post with an auto-generated ID
        new_post = {
            'id': len(blog_posts) + 1,  # Ensure each post gets a unique ID
            'author': author,
            'title': title,
            'content': content
        }

        # Append the new post to the list
        blog_posts.append(new_post)

        # Save the updated list back to the JSON file
        save_blog_posts(blog_posts)

        # Flash a success message
        flash('New post added successfully!', 'success')

        # Redirect back to the home page to see the updated list
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Load existing blog posts
    blog_posts = load_blog_posts()

    # Remove the post with the specified ID
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save the updated list back to the JSON file
    save_blog_posts(blog_posts)

    # Flash a success message
    flash('Post deleted successfully!', 'success')

    # Redirect back to the home page
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog post to update
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post with the new form data
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        # Load existing blog posts
        blog_posts = load_blog_posts()

        # Save the updated post list back to the JSON file
        save_blog_posts(blog_posts)

        # Flash a success message
        flash('Post updated successfully!', 'success')

        # Redirect to the home page to see the updated post
        return redirect(url_for('index'))

    # If GET request, render the update form with the current post data
    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)