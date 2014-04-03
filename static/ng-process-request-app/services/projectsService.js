/**
 * Created by swhite on 2/25/14.
 */

var URLS = {
    'PROJECTS':                   '/api/repository/projects/',
    'SPECIMENS':                  '/api/repository/specimens/',
    'SUBJECT_GROUPS':             '/api/repository/subject_groups/',
    'SITES':                      '/api/repository/sites/',
    'SUBJECTS':                   '/api/repository/subjects/',
    'PROJECT_PANELS':             '/api/repository/project_panels/',
    'SITE_PANELS':                '/api/repository/site_panels/',
    'CYTOMETERS':                 '/api/repository/cytometers/',
    'COMPENSATIONS':              '/api/repository/compensations/',
    'CREATE_COMPENSATION':        '/api/repository/compensations/add/',
    'STIMULATIONS':               '/api/repository/stimulations/',
    'SAMPLES':                    '/api/repository/samples/',
    'CREATE_SAMPLES':             '/api/repository/samples/add/',
    'SAMPLE_METADATA':            '/api/repository/samplemetadata/',
    'SAMPLE_COLLECTIONS':         '/api/repository/sample_collections/',
    'SAMPLE_COLLECTION_MEMBERS':  '/api/repository/sample_collection_members/',
    'VISIT_TYPES':                '/api/repository/visit_types/',

    // Process related API URLs
    'WORKERS':                    '/api/repository/workers/',
    'SUBPROCESS_CATEGORIES':      '/api/repository/subprocess_categories/',
    'SUBPROCESS_IMPLEMENTATIONS': '/api/repository/subprocess_implementations/',
    'SUBPROCESS_INPUTS':          '/api/repository/subprocess_inputs/',
    'VERIFY_WORKER':              '/api/repository/verify_worker/',
    'PROCESS_REQUESTS':           '/api/repository/process_requests/',
    'PROCESS_REQUEST_INPUTS':     '/api/repository/process_request_inputs',
    'VIABLE_PROCESS_REQUESTS':    '/api/repository/viable_process_requests/',
};

var service = angular.module('reflowService', ['ngResource']);

service
    .factory('Project', ['$resource', function ($resource) {
        return $resource(URLS.PROJECTS);
    }])
    .factory('Site', ['$resource', function ($resource) {
        return $resource(URLS.SITES);
    }])
    .factory('Specimen', ['$resource', function ($resource) {
        return $resource(URLS.SPECIMENS);
    }])
    .factory('SubjectGroup', ['$resource', function ($resource) {
        return $resource(URLS.SUBJECT_GROUPS);
    }])
    .factory('Subject', ['$resource', function ($resource) {
        return $resource(URLS.SUBJECTS);
    }])
    .factory('VisitType', ['$resource', function ($resource) {
        return $resource(URLS.VISIT_TYPES);
    }])
    .factory('Stimulation', ['$resource', function ($resource) {
        return $resource(URLS.STIMULATIONS);
    }])
    .factory('Cytometer', ['$resource', function ($resource) {
        return $resource(URLS.CYTOMETERS);
    }])
    .factory('ProjectPanel', ['$resource', function ($resource) {
        return $resource(URLS.PROJECT_PANELS);
    }])
    .factory('SitePanel', ['$resource', function ($resource) {
        return $resource(URLS.SITE_PANELS);
    }])
    .factory('Compensation', ['$resource', function ($resource) {
        return $resource(URLS.COMPENSATIONS);
    }])
    .factory('Sample', ['$resource', function ($resource) {
        return $resource(URLS.SAMPLES);
    }])
    .factory('SampleCollection', ['$resource', function ($resource) {
        return $resource(URLS.SAMPLE_COLLECTIONS);
    }])
    .factory('SampleCollectionMember', ['$resource', function ($resource) {
        return $resource(
            URLS.SAMPLE_COLLECTION_MEMBERS,
            {},
            {
                save: {
                    method: 'POST',
                    isArray: true
                }
            }
        );
    }])
    .factory('SubprocessCategory', ['$resource', function ($resource) {
        return $resource(URLS.SUBPROCESS_CATEGORIES);
    }])
    .factory('SubprocessImplementation', ['$resource', function ($resource) {
        return $resource(URLS.SUBPROCESS_IMPLEMENTATIONS);
    }])
    .factory('SubprocessInput', ['$resource', function ($resource) {
        return $resource(URLS.SUBPROCESS_INPUTS);
    }])
    .factory('ProcessRequest', ['$resource', function ($resource) {
        return $resource(URLS.PROCESS_REQUESTS);
    }])
    .factory('ProcessRequestInput', ['$resource', function ($resource) {
        return $resource(
            URLS.PROCESS_REQUEST_INPUTS,
            {},
            {
                save: {
                    method: 'POST',
                    isArray: true
                }
            }
        );
    }])
    .service('Pretreatment', [ function () {
        this.query = function () {
            return [{name:'In vitro'}, {name:'Ex vivo'}];
        };
    }])
    .service('Storage', [ function () {
        this.query = function () {
            return [{name:'Fresh'}, {name:'Cryopreserved'}];
        };
    }]);