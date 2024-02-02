# import a module from another directory
import re
import sys

sys.path.append("/Users/yuyakawakami/Research/EOF_ensemble")

import calculate_eof as ce
import calculate_projections as cp
import numpy as np
import pandas as pd
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    """
    Return Hello World
    """
    return "Hello World"


@app.route("/random", methods=["GET"])
def random():
    """
    Return random points
    """
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
def spatial():
    """
    testing for now
    """
    # generate 100 random points inside a 50x50 square as floats
    df = cp.calculate_projection(
        "/Users/yuyakawakami/Research/EOF_ensemble/eof_data/rcpall_ts_undetrended_spatial_0.csv",
        False,
    )

    pattern = r"_rcp(\d{2})_r(\d{3})i"

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

    for point in res_data["points"]:
        match = re.search(pattern, point["text"])
        if match:
            rcp_substring = match.group(1)
            ensembleid_substring = match.group(2)
            point["text"] = f"RCP{rcp_substring}:E{ensembleid_substring}"
        else:
            print("Pattern not found.")

    return make_response(jsonify(res_data), 200)


@app.route("/spatial/<rcp_id>/<ensemble_id>")
def temporal(rcp_id, ensemble_id):
    """
    testing for now
    """

    df = pd.read_csv(
        "/Users/yuyakawakami/Research/EOF_ensemble/eof_data/rcpall_ts_undetrended_spatial_0.csv",
    )
    print(rcp_id, ensemble_id)
    print(f"rcp{rcp_id}_r{ensemble_id:03}")

    arr = {
        "data": df.filter(like=f"rcp{rcp_id}_r{int(ensemble_id):03}")
        .values.flatten()
        .tolist()
    }

    return make_response(jsonify(arr, 200))


@app.route("/spatial_grid")
def spatial_grid():
    _, _, lat, lon = ce.read_data(
        "/Users/yuyakawakami/Research/Data/MPI-GE/ncs/ts_Lmon_MPI-ESM_rcp26_r001i2005p3_200601-209912.nc",
        "ts",
        remove_mean=False,
        linear_detrend=False,
    )
    ret = {"lat": lat.tolist(), "lon": lon.tolist()}
    return make_response(jsonify(ret), 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
