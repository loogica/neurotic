import os

from coopy.base import init_persistent_system
from flask import Flask, jsonify, render_template

from neurotic.domain import TestReportRepository

app = Flask(__name__)

repository = init_persistent_system(TestReportRepository,
                                    basedir="build_history")

@app.route("/")
def main():
    return '''
<!doctype html>
<html ng-app>
  <head>
    <link href="/static/bootstrap.min.css" rel="stylesheet">
    <link href="/static/grid.css" rel="stylesheet">
    <script src="http://ajax.googleapis.com/ajax/libs/angularjs/1.0.6/angular.min.js"></script>
    <script src="http://underscorejs.org/underscore-min.js"></script>
    <script src="/static/ace/ace.js" type="text/javascript" charset="utf-8"></script>
    <script src="/static/neurotic.js"></script>
    <style type="text/css" media="screen">
    #editor {
        height:500px;
    }
  </style>
  </head>
  <body ng-controller="NeuroticCtrl">
    <div class="container">
      <h1>Last Build</h1>
      <div class="row">
        <div class="col-6 col-sm-6 col-lg-6">
          <pre id="editor" ng-show="show">{{ refined_error }}</pre>
        </div>
        <div class="col-6 col-sm-6">
          <div class="col-lg-error col-current">
            <h1>Build {{ current_build.id }}</h1>
            <li ng-repeat="test in current_build.reports | filter:failed_filter">
               <a href="#show-{{ test.id }}" ng-click="show_error(test)"
               ng-style="test.size">
                 {{ test.outcome }} - {{ test.location[2]  }}
               </a>
            </li>
          </div>
          <div class="col-other">
            <li ng-repeat="build in reports | filter:except_current">
              <a href="#build-{{ build.id}}" ng-click="show_build(build)">
                Build {{ build.id }}
              </a>
            </li>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
'''

@app.route("/reports", methods=["GET", "OPTIONS"])
def reports():
    return jsonify(dict(reports=repository.reports))

if __name__ == "__main__":
    app.run(debug=True)
