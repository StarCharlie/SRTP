from flask import Flask
from blueprints import user_bp, home_bp, graph_bp
import config
from extension import db
from flask_cors import *


app = Flask(__name__)
app.config['DEBUG'] = True
# 绑定配置文件
app.config.from_object(config)
CORS(app, supports_credentials=True)
db.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(user_bp)
app.register_blueprint(graph_bp)


@app.route("/")
def to_home():
    return "hello"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
