var ModalFormCtrl = function ($scope, $modalInstance, instance) {
    $scope.instance = instance;
    $scope.ok = function () {
        $modalInstance.close();
    };
};

app.controller(
    'MainController',
    ['$scope', 'ModelService', function ($scope, ModelService) {
        $scope.$on('updateProjects', function () {
            ModelService.reloadProjects();
        });
    }
]);

app.controller(
    'ProjectListController',
    ['$scope', 'ModelService', function ($scope, ModelService) {
        $scope.projects = ModelService.getProjects();
    }
]);

app.controller(
    'ProjectDetailController',
    [
        '$scope',
        '$controller',
        '$stateParams',
        '$modal',
        'ModelService',
        function ($scope, $controller, $stateParams, $modal, ModelService) {
            function get_project() {
                return ModelService.getProjectById(
                    $stateParams.projectId
                );
            }

            $scope.current_project = get_project();

            $scope.$on('projectUpdated', function () {
                $scope.current_project = get_project();
            });

            $scope.errors = [];
            $scope.can_view_project = false;
            $scope.can_modify_project = false;
            $scope.can_add_data = false;
            $scope.can_manage_users = false;

            if ($scope.current_project.permissions.indexOf('view_project_data')) {
                $scope.can_view_project = true;
            }
            if ($scope.current_project.permissions.indexOf('add_project_data')) {
                $scope.can_add_data = true;
            }
            if ($scope.current_project.permissions.indexOf('modify_project_data')) {
                $scope.can_modify_project = true;
            }
            if ($scope.current_project.permissions.indexOf('manage_project_users')) {
                $scope.can_manage_users = true;
            }

            $scope.init_form = function(instance) {
                var proposed_instance = angular.copy(instance);
                $scope.errors = [];

                // launch form modal
                var modalInstance = $modal.open({
                    templateUrl: 'static/ng-app/partials/project-form.html',
                    controller: ModalFormCtrl,
                    resolve: {
                        instance: function() {
                            return proposed_instance;
                        }
                    }
                });
            };
        }
    ]
);

app.controller(
    'ProjectEditController',
    [
        '$scope',
        '$rootScope',
        '$controller',
        'Project',
        function ($scope, $rootScope, $controller, Project) {
            // Inherits ProjectDetailController $scope
            $controller('ProjectDetailController', {$scope: $scope});

            $scope.create_update = function (instance) {
                $scope.errors = [];
                var response;
                if (instance.id) {
                    response = Project.update(
                        {id: instance.id },
                        $scope.instance
                    );
                } else {
                    response = Project.save(
                        $scope.instance
                    );
                }

                response.$promise.then(function () {
                    // notify to update subject group list
                    $rootScope.$broadcast('updateProjects');

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
    'SubjectGroupController',
    ['$scope', '$controller', '$stateParams', '$modal', 'SubjectGroup', function ($scope, $controller, $stateParams, $modal, SubjectGroup) {
        // Inherits ProjectDetailController $scope
        $controller('ProjectDetailController', {$scope: $scope});

        function get_list() {
            return SubjectGroup.query(
                {
                    'project': $scope.current_project.id
                }
            );
        }
        $scope.subject_groups = get_list();

        $scope.$on('updateSubjectGroups', function () {
            $scope.subject_groups = get_list();
        });

        $scope.init_form = function(instance) {
            var proposed_instance = angular.copy(instance);
            $scope.errors = [];

            // launch form modal
            var modalInstance = $modal.open({
                templateUrl: 'static/ng-app/partials/subject-group-form.html',
                controller: ModalFormCtrl,
                resolve: {
                    instance: function() {
                        return proposed_instance;
                    }
                }
            });
        };
    }
]);

app.controller(
    'SubjectGroupEditController',
    ['$scope', '$rootScope', '$controller', 'SubjectGroup', function ($scope, $rootScope, $controller, SubjectGroup) {
        // Inherits ProjectDetailController $scope
        $controller('ProjectDetailController', {$scope: $scope});

        $scope.create_update = function (instance) {
            $scope.errors = [];
            var response;
            if (instance.id) {
                response = SubjectGroup.update(
                    {id: instance.id },
                    $scope.instance
                );
            } else {
                instance.project = $scope.current_project.id;

                response = SubjectGroup.save(
                    $scope.instance
                );
            }

            response.$promise.then(function () {
                // notify to update subject group list
                $rootScope.$broadcast('updateSubjectGroups');

                // close modal
                $scope.ok();

            }, function (error) {
                $scope.errors = error.data;
            });
        };
    }
]);

app.controller(
    'SubjectController',
    [
        '$scope',
        '$controller',
        '$modal',
        'Subject',
        function ($scope, $controller, $modal, Subject) {
            // Inherits ProjectDetailController $scope
            $controller('ProjectDetailController', {$scope: $scope});

            function get_list() {
                return Subject.query(
                    {
                        'project': $scope.current_project.id
                    }
                );
            }
            $scope.subjects = get_list();

            $scope.$on('updateSubjects', function () {
                $scope.subjects = get_list();
            });

            $scope.init_form = function(instance) {
                var proposed_instance = angular.copy(instance);
                $scope.errors = [];

                // launch form modal
                var modalInstance = $modal.open({
                    templateUrl: 'static/ng-app/partials/subject-form.html',
                    controller: ModalFormCtrl,
                    resolve: {
                        instance: function() {
                            return proposed_instance;
                        }
                    }
                });
            };
        }
    ]
);

app.controller(
    'SubjectEditController',
    [
        '$scope',
        '$rootScope',
        '$controller',
        'Subject',
        'SubjectGroup',
        function ($scope, $rootScope, $controller, Subject, SubjectGroup) {
            // Inherits ProjectDetailController $scope
            $controller('ProjectDetailController', {$scope: $scope});

            $scope.subject_groups = SubjectGroup.query(
                {
                    'project': $scope.current_project.id
                }
            );

            $scope.create_update = function (instance) {
                $scope.errors = [];
                var response;
                if (instance.id) {
                    response = Subject.update(
                        {id: instance.id },
                        $scope.instance
                    );
                } else {
                    instance.project = $scope.current_project.id;

                    response = Subject.save(
                        $scope.instance
                    );
                }

                response.$promise.then(function () {
                    // notify to update subject list
                    $rootScope.$broadcast('updateSubjects');

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
    'SiteController',
    [
        '$scope',
        '$controller',
        '$modal',
        'Site',
        function ($scope, $controller, $modal, Site) {
            // Inherits ProjectDetailController $scope
            $controller('ProjectDetailController', {$scope: $scope});

            function get_list() {
                return Site.query(
                    {
                        'project': $scope.current_project.id
                    }
                );
            }
            $scope.sites = get_list();

            $scope.$on('updateSites', function () {
                $scope.sites = get_list();
            });

            $scope.init_form = function(instance) {
                var proposed_instance = angular.copy(instance);
                $scope.errors = [];

                // launch form modal
                $modal.open({
                    templateUrl: 'static/ng-app/partials/site-form.html',
                    controller: ModalFormCtrl,
                    resolve: {
                        instance: function() {
                            return proposed_instance;
                        }
                    }
                });
            };
        }
    ]
);

app.controller(
    'SiteEditController',
    [
        '$scope',
        '$rootScope',
        '$controller',
        'Site',
        function ($scope, $rootScope, $controller, Site) {
            // Inherits ProjectDetailController $scope
            $controller('ProjectDetailController', {$scope: $scope});

            $scope.create_update = function (instance) {
                $scope.errors = [];
                var response;
                if (instance.id) {
                    response = Site.update(
                        {id: instance.id },
                        $scope.instance
                    );
                } else {
                    instance.project = $scope.current_project.id;

                    response = Site.save(
                        $scope.instance
                    );
                }

                response.$promise.then(function () {
                    // notify to update subject list
                    $rootScope.$broadcast('updateSites');

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
    'CytometerController',
    [
        '$scope',
        '$controller',
        '$modal',
        'Cytometer',
        function ($scope, $controller, $modal, Cytometer) {
            // Inherits ProjectDetailController $scope
            $controller('ProjectDetailController', {$scope: $scope});

            function get_list() {
                return Cytometer.query(
                    {
                        'project': $scope.current_project.id
                    }
                );
            }
            $scope.cytometers = get_list();

            $scope.$on('updateCytometers', function () {
                $scope.cytometers = get_list();
            });

            $scope.init_form = function(instance) {
                var proposed_instance = angular.copy(instance);
                $scope.errors = [];

                // launch form modal
                var modalInstance = $modal.open({
                    templateUrl: 'static/ng-app/partials/cytometer-form.html',
                    controller: ModalFormCtrl,
                    resolve: {
                        instance: function() {
                            return proposed_instance;
                        }
                    }
                });
            };
        }
    ]
);

app.controller(
    'CytometerEditController',
    [
        '$scope',
        '$rootScope',
        '$controller',
        'Cytometer',
        'Site',
        function ($scope, $rootScope, $controller, Cytometer, Site) {
            // Inherits ProjectDetailController $scope
            $controller('ProjectDetailController', {$scope: $scope});

            $scope.sites = Site.query(
                {
                    'project': $scope.current_project.id
                }
            );

            $scope.create_update = function (instance) {
                $scope.errors = [];
                var response;
                if (instance.id) {
                    response = Cytometer.update(
                        {id: instance.id },
                        $scope.instance
                    );
                } else {
                    response = Cytometer.save(
                        $scope.instance
                    );
                }

                response.$promise.then(function () {
                    // notify to update subject list
                    $rootScope.$broadcast('updateCytometers');

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
    'VisitTypeController',
    [
        '$scope',
        '$controller',
        '$modal',
        'VisitType',
        function ($scope, $controller, $modal, VisitType) {
            // Inherits ProjectDetailController $scope
            $controller('ProjectDetailController', {$scope: $scope});

            function get_list() {
                return VisitType.query(
                    {
                        'project': $scope.current_project.id
                    }
                );
            }
            $scope.visit_types = get_list();

            $scope.$on('updateVisitTypes', function () {
                $scope.visit_types = get_list();
            });

            $scope.init_form = function(instance) {
                var proposed_instance = angular.copy(instance);
                $scope.errors = [];

                // launch form modal
                $modal.open({
                    templateUrl: 'static/ng-app/partials/visit-type-form.html',
                    controller: ModalFormCtrl,
                    resolve: {
                        instance: function() {
                            return proposed_instance;
                        }
                    }
                });
            };
        }
    ]
);

app.controller(
    'VisitTypeEditController',
    [
        '$scope',
        '$rootScope',
        '$controller',
        'VisitType',
        function ($scope, $rootScope, $controller, VisitType) {
            // Inherits ProjectDetailController $scope
            $controller('ProjectDetailController', {$scope: $scope});

            $scope.create_update = function (instance) {
                $scope.errors = [];
                var response;
                if (instance.id) {
                    response = VisitType.update(
                        {id: instance.id },
                        $scope.instance
                    );
                } else {
                    instance.project = $scope.current_project.id;

                    response = VisitType.save(
                        $scope.instance
                    );
                }

                response.$promise.then(function () {
                    // notify to update subject list
                    $rootScope.$broadcast('updateVisitTypes');

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
    'StimulationController',
    [
        '$scope',
        '$controller',
        '$modal',
        'Stimulation',
        function ($scope, $controller, $modal, Stimulation) {
            // Inherits ProjectDetailController $scope
            $controller('ProjectDetailController', {$scope: $scope});

            function get_list() {
                return Stimulation.query(
                    {
                        'project': $scope.current_project.id
                    }
                );
            }
            $scope.stimulations = get_list();

            $scope.$on('updateStimulations', function () {
                $scope.stimulations = get_list();
            });

            $scope.init_form = function(instance) {
                var proposed_instance = angular.copy(instance);
                $scope.errors = [];

                // launch form modal
                $modal.open({
                    templateUrl: 'static/ng-app/partials/stimulation-form.html',
                    controller: ModalFormCtrl,
                    resolve: {
                        instance: function() {
                            return proposed_instance;
                        }
                    }
                });
            };
    }
]);

app.controller(
    'StimulationEditController',
    [
        '$scope',
        '$rootScope',
        '$controller',
        'Stimulation',
        function ($scope, $rootScope, $controller, Stimulation) {
            // Inherits ProjectDetailController $scope
            $controller('ProjectDetailController', {$scope: $scope});

            $scope.create_update = function (instance) {
                $scope.errors = [];
                var response;
                if (instance.id) {
                    response = Stimulation.update(
                        {id: instance.id },
                        $scope.instance
                    );
                } else {
                    instance.project = $scope.current_project.id;

                    response = Stimulation.save(
                        $scope.instance
                    );
                }

                response.$promise.then(function () {
                    // notify to update subject list
                    $rootScope.$broadcast('updateStimulations');

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
    'PanelTemplateController',
    ['$scope', '$controller', 'PanelTemplate', function ($scope, $controller, PanelTemplate) {
        // Inherits ProjectDetailController $scope
        $controller('ProjectDetailController', {$scope: $scope});

        $scope.panel_templates = PanelTemplate.query(
            {
                'project': $scope.current_project.id
            }
        );

        $scope.expand_params = [];
        $scope.panel_templates.$promise.then(function () {
            $scope.panel_templates.forEach(function () {
                $scope.expand_params.push(false);
            })
        });

        $scope.toggle_params = function (i) {
            $scope.expand_params[i] = $scope.expand_params[i] != true;
        };

        $scope.expand_all_panels = function () {
            for (var i = 0; i < $scope.panel_templates.length; i++) {
                $scope.expand_params[i] = true;
            }
        };

        $scope.collapse_all_panels = function () {
            for (var i = 0; i < $scope.panel_templates.length; i++) {
                $scope.expand_params[i] = false;
            }
        };
    }
]);

app.controller(
    'SampleController',
    ['$scope', 'ModelService', function ($scope, ModelService) {
        $scope.current_project = ModelService.getCurrentProject();
    }
]);

app.controller(
    'BeadSampleController',
    ['$scope', 'ModelService', function ($scope, ModelService) {
        $scope.current_project = ModelService.getCurrentProject();
    }
]);

app.controller(
    'CompensationController',
    ['$scope', 'ModelService', function ($scope, ModelService) {
        $scope.current_project = ModelService.getCurrentProject();
    }
]);