# import a module from another directory
import sys

sys.path.append("/Users/yuyakawakami/Research/EOF_ensemble")


import calculate_projections as cp
import numpy as np
from flask import Flask, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    return "Hello World"


@app.route("/random", methods=["GET"])
def random():
    # generate 100 random points inside a 50x50 square as floats
    x = np.random.uniform(-25, 25, 100)
    y = np.random.uniform(-25, 25, 100)

    # make a list of lists

    res_data = {
        "points": [
            {"coords": list(pair), "text": "random points"} for pair in zip(x, y)
        ]
    }
    return make_response(jsonify(res_data), 200)


@app.route("/spatial", methods=["GET"])
def main():
    # generate 100 random points inside a 50x50 square as floats
    df = cp.calculate_projection(
        "/Users/yuyakawakami/Research/EOF_ensemble/eof_data/rcpall_ts_undetrended_spatial_0.csv",
        False,
    )

    res_data = {
        "points": [
            # {"coords": [row["Dimension 1"], row["Dimension 2"]], "text": index}
            {
                "coords": [float(row["Dimension 1"]), float(row["Dimension 2"])],
                "text": index,
            }
            for index, row in df.iterrows()
        ]
    }
    return make_response(jsonify(res_data), 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
