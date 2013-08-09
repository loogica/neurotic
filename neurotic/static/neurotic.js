

function NeuroticCtrl($scope, $http) {
  $scope.reports = [];
  $scope.show = false;
  editor = ace.edit("editor");
  editor.setTheme("ace/theme/solarized_light");
  editor.getSession().setMode("ace/mode/python");
  editor.setFontSize(10);

  $scope.init = function() {
    $http.get("/reports").success(function(data) {
        $scope.reports = data.reports;
    });
  };
  $scope.init();

  $scope.last_build = function() {
    return $scope.reports[$scope.reports.length - 1];
  };

  $scope.failed_filter = function(obj) {
      return obj.outcome == "failed";
  };

  $scope.show_error = function(item) {
    var line_count = 0;
    var error_line = null;
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
  };


}
