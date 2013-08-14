var app = angular.module('neurotic', []);

app.controller('NeuroticCtrl', ['$scope', '$http',
    function($scope, $http) {
  $scope.reports = [];
  $scope.show = false;
  $scope.current_build = null;

  editor = ace.edit("editor");
  editor.setTheme("ace/theme/solarized_light");
  editor.getSession().setMode("ace/mode/python");
  editor.setFontSize(10);

  $scope.show_build = function(build) {
      $scope.current_build = build;
      var errors = _.filter($scope.current_build.reports,
                            $scope.failed_filter);
      if (errors) {
        $scope.current_item = errors[0];
        $scope.show_error($scope.current_item);
      }
  };

  $scope.failed_filter = function(obj) {
      return obj.outcome == "failed";
  };

  $scope.except_current = function(obj) {
      return obj.id != $scope.current_build.id;
  };

  $scope.init = function() {
    $http.get("/reports").success(function(data) {
        $scope.reports = _.map(data.reports, function(el) {
            el.start = moment(el.start);
            return el;
        });
        $scope.current_build = $scope.reports[$scope.reports.length - 1];
        var errors = _.filter($scope.current_build.reports,
                              $scope.failed_filter);
        if (errors) {
          $scope.current_item = errors[0];
          $scope.show_error($scope.current_item);
        }
    });
  };
  $scope.init();

  $scope.show_error = function(item) {
    var line_count = 0;
    var error_line = null;

    if (!item) {
        return;
    }

    if ($scope.current_item)
        $scope.current_item.size = {'font-size': '14px'};

    if (!item.longrepr) {
        return;
    }

    $scope.refined_error = _.reduce(item.longrepr.reprtraceback.reprentries[0].lines,
      function(a, b) {
        line_count++;
        if (b.substring(0,1) == '>') {
          error_line = line_count;
        }
        return a + '\n' + b;
    });
    editor.getSession().setValue($scope.refined_error);
    $scope.show = true;
    editor.setHighlightActiveLine(true);
    editor.scrollToLine(error_line, true, true, function () {});

    item.size = {'font-size': '20px'};
    $scope.current_item = item;
  };
}]);
