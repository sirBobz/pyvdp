from pyvdp.dispatcher import VisaDispatcher


class VisaGlobalAtmLocatorDispatcher(VisaDispatcher):
    """Implements HTTP requests to Visa Global ATM Locator APIs.

    :param data: **Required**. Instance of data model.
    :param str resource: **Required**. Resource name.
    :param str api: **Required**. API name.
    :param str method: **Required**. Method name.
    :param str auth_method: **Required**. Authentication method. Possible values are: **ssl**, **token**
    :param str http_verb: **Required**. HTTP Verb.
    """
    def __init__(self, resource, api, method, http_verb, auth_method, data):
        super(VisaGlobalAtmLocatorDispatcher, self).__init__(resource=resource,
                                                             api=api,
                                                             method=method,
                                                             http_verb=http_verb,
                                                             auth_method=auth_method,
                                                             data=data)

