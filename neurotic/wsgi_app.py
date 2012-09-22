import os

from coopy.base import init_persistent_system
from flask import Flask, jsonify, render_template

from neurotic.domain import TestReportRepository

app = Flask(__name__)

repository = init_persistent_system(TestReportRepository,
                                    basedir="build_history")

@app.route("/")
def main():
    return jsonify(dict(reports=repository.reports))

if __name__ == "__main__":
    app.run(debug=True)
