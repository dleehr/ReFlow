app.controller(
    'SampleDeleteController',
    [
        '$scope',
        '$rootScope',
        '$controller',
        'Sample',
        function ($scope, $rootScope, $controller, Sample) {
            // Inherits ProjectDetailController $scope
            $controller('ProjectDetailController', {$scope: $scope});

            $scope.destroy = function (instance) {
                $scope.errors = [];
                var response;
                response = Sample.delete({id: instance.id });

                response.$promise.then(function () {
                    // notification to update samples
                    $rootScope.$broadcast('updateSamples');

                    // close modal
                    $scope.ok();

                }, function (error) {
                    $scope.errors = error.data;
                });
            };
        }
    ]
);

app.controller(
    'BeadSampleDeleteController',
    [
        '$scope',
        '$rootScope',
        '$controller',
        'BeadSample',
        function ($scope, $rootScope, $controller, BeadSample) {
            // Inherits ProjectDetailController $scope
            $controller('ProjectDetailController', {$scope: $scope});

            $scope.destroy = function (instance) {
                $scope.errors = [];
                var response;
                response = BeadSample.delete({id: instance.id });

                response.$promise.then(function () {
                    // notification to update samples
                    $rootScope.$broadcast('updateBeadSamples');

                    // close modal
                    $scope.ok();

                }, function (error) {
                    $scope.errors = error.data;
                });
            };
        }
    ]
);