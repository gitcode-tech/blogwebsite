from flask import Flask, render_template, request, redirect, url_for

from database import (
    initialize_database,
    get_all_posts,
    get_post,
    create_post,
    update_post,
    delete_post
)


app = Flask(__name__)

initialize_database()


@app.route("/")
def index():
    posts = get_all_posts()

    return render_template(
        "index.html",
        posts=posts
    )


@app.route("/post/<int:post_id>")
def post(post_id):
    selected_post = get_post(post_id)

    if selected_post is None:
        return "Post not found", 404

    return render_template(
        "post.html",
        post=selected_post
    )


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        category = request.form.get("category")

        if not title or not content:
            return "Title and content are required", 400

        create_post(title, content, category)

        return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit(post_id):
    selected_post = get_post(post_id)

    if selected_post is None:
        return "Post not found", 404

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        category = request.form.get("category")

        update_post(
            post_id,
            title,
            content,
            category
        )

        return redirect(url_for("post", post_id=post_id))

    return render_template(
        "edit.html",
        post=selected_post
    )


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete(post_id):
    delete_post(post_id)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
