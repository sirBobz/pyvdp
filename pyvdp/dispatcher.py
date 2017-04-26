import jsonpickle
import random
import requests
import string

from pyvdp.exceptions import (VisaAccessDeniedError, VisaDuplicateTransactionError, VisaGeneralError,
                              VisaMessageValidationError, VisaNotFoundError, VisaTimeoutError, VisaUnauthenticatedError)

from pyvdp import configuration, authentication, logger


class VisaDispatcher(object):
    """Constructs a request to Visa API to provided resource, method and http verb.

    After request is constructed, it shall be submitted with `send()` method, which returns a `requests.Response`
    object.

    This class is not assumed to be instantiated on its own (consider it abstract). Instead, every VISA API
    implementation must provide its own request class, inheriting from VisaRequest and providing a
    corresponding VISA API resource name as a `resource` argument value.

    :param str resource: **Required**. VISA API resource name.
    :param str api: **Required**. VISA API api name.
    :param str version: **Required**. VISA API version.
    :param str method: **Required**. VISA API endpoint method.
    :param str http_verb: **Required**. VISA API HTTP verb. Possible values: **GET**, **POST**.
    :param str auth_method: **Required**. Authentication method. Possible values:
            **ssl** - for certificate-based authentication (default) or **token** - for x-pay-token authentication    
    :param object data: **Conditional**. Data payload.
    :param str url_params: **Conditional**. Additional parameters for endpoint url, e.g. status identifier for
        :func:`pyvdp.visadirect.fundstransfer.pushfundstransactions.get`.    
    """
    # VDP HTTP codes mapped to exceptions
    # (kudos to http://codereview.stackexchange.com/questions/155350/pyvdp-python-library-for-visa-developer-program)
    ERROR_CODES = {
        202: VisaTimeoutError,
        303: VisaDuplicateTransactionError,
        400: VisaMessageValidationError,
        401: VisaUnauthenticatedError,
        403: VisaAccessDeniedError,
        404: VisaNotFoundError
    }

    def __init__(self,
                 resource,
                 api,
                 version,
                 method,
                 http_verb,
                 auth_method,
                 url_params=None,
                 data=None):

        self._config = configuration.get_config()

        # API path structure: https://domain/resource/api/version/method
        # eg https://sandbox.api.visa.com/cybersource/payments/v1/authorizations
        self._url = self._config['url']
        self._resource = resource
        self._api = api
        self._method = method
        self._version = version
        self._endpoint = "%s/%s/%s/%s/%s" % (self._url, resource, api, version, method)
        self._http_verb = http_verb

        if url_params:
            self._endpoint = self._endpoint + "/" + url_params

        if self._http_verb == 'POST' or self._http_verb == 'PUT':
            self._data = self._obj_to_json(data)
        elif self._http_verb == 'GET':
            if data:
                self._data = data.__dict__
            else:
                self._data = None
        else:
            raise AttributeError("HTTP verb must be 'GET', 'POST' or 'PUT'. '%s' given." % self._http_verb)

        # Headers setup
        self._setup_headers()

        self._auth = authentication.get_auth(auth_method,
                                             url=self._url,
                                             api=self._api,
                                             version=self._version,
                                             method=self._method,
                                             data=self._data)

    @logger.log_event
    def send(self):
        """Submits a data object or query string id to VISA using `self._endpoint` field and corresponding http verb.

        :return: result: Resulting dictionary.
        """

        # Session initialization
        _session = requests.Session()

        # Using requests.Session and requests.PreparedRequest to construct request to VDP
        _request = requests.Request(
            headers=self._headers,
            url=self._endpoint,
            method=self._http_verb,
        )

        if self._http_verb == 'GET':
            _request.params = self._data
        elif self._http_verb == 'POST' or self._http_verb == 'PUT':
            _request.data = self._data
        else:
            raise AttributeError("HTTP verb must be 'GET', 'POST', 'PUT'. '%s' given." % self._http_verb)

        _request.__dict__.update(self._auth['request'])
        _session.__dict__.update(self._auth['session'])
        self._headers.update(self._auth['headers'])

        prepped_req = _request.prepare()

        response = _session.send(prepped_req)

        return self._handle_response(response)

    def _handle_response(self, response):
        """Processes a response from Visa Direct API.

        Depending on HTTP code in response, either returns a result or raises corresponding app-level exception.

        :param requests.Response response: **Required**. Response from VISA.
        :return: dict result: Resulting dictionary.
        :raises: VisaTimeoutError, VisaDuplicateTransactionError, VisaMessageValidationError, VisaUnauthenticatedError,
                VisaAccessDeniedError, VisaNotFoundError, VisaGeneralError
        """

        try:
            if response.headers['content-type'] == 'application/json;charset=UTF-8':
                message = response.json()
            else:
                message = response.text
        except KeyError:
            message = "Unknown VISA error"

        status_code = response.status_code

        result = {
            'request': {
                'url': response.request.url,
                'method': response.request.method,
                'headers': response.request.headers,
                'body': response.request.body,
            },
            'response': {
                'code': status_code,
                'headers': response.headers,
                'message': message
            }
        }

        if status_code == 200:
            return result
        else:
            raise self.ERROR_CODES.get(status_code, VisaGeneralError)(result=result)

    @staticmethod
    def _get_x_client_transaction_id():
        """Generates random 12-digits value used for X-Client-Transaction-ID header.

        :return: Value for X-Client-Transaction-ID header
        """
        return ''.join(random.choice(string.digits) for _ in range(12))

    @staticmethod
    def _obj_to_json(data):
        """Serializes Python object to json

        :param object data: Python object
        :return: JSON string
        """
        return jsonpickle.encode(data, unpicklable=False)

    def _setup_headers(self):
        self._headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Client-Transaction-ID': self._get_x_client_transaction_id()
        }

