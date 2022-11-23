from flask import Flask, redirect, url_for
from blueprints import user_bp, home_bp
import config
from extension import db


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(user_bp)


@app.route("/")
def to_home():
    return redirect(url_for("home.workspace"))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
