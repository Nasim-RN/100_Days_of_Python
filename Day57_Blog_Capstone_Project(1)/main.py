from flask import Flask, render_template
import requests

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
print(posts)
# post_objects = []
# for n in range(len(posts)):
#     post_obj = (posts[n]["id"], posts[n]["title"], posts[n]["subtitle"],  posts[n]["body"])
#     post_objects.append(post_obj)
# print(post_objects)


app = Flask(__name__)

@app.route('/')
def get_all_post():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
        requested_post = None
        if posts[0]["id"] == index:
            requested_post = posts[0]
        elif posts[1]["id"] == index:
            requested_post = posts[1]
        else:
            requested_post = posts[2]

        return render_template("post.html", post=requested_post)




if __name__ == "__main__":
    app.run(debug=True)
