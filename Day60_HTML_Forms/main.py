from flask import Flask, render_template, request
import requests
import smtplib
import os

blog_url = "https://api.npoint.io/2b1e1701b179fe512483"
blog_resp = requests.get(blog_url)
all_posts = blog_resp.json()



app = Flask(__name__)

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")


@app.route('/')
def home():
    return render_template("index.html", posts=all_posts)


@app.route('/index.html')
def index():
    return render_template("index.html", posts=all_posts)


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route("/contact.html", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        message = data["message"]
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="n.r.niyar@gmail.com",
                msg=f"Subject: New Message!\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
            )
        return render_template("contact.html", msg_sent=True)
    else:
        return render_template("contact.html", msg_sent=False)




@app.route('/post/<int:p_id>')
def get_post(p_id):
    return render_template('post.html', post=all_posts[int(p_id) - 1])


if __name__ == "__main__":
    app.run(debug=True)