from pyvdp.dispatcher import VisaDispatcher


class VisaMerchantMeasurementDispatcher(VisaDispatcher):
    """Implements HTTP requests to Visa MerchantMeasurement APIs.

    https://developer.visa.com/products/merchant_measurement

    :param data: **Required**. Instance of data model.
    :param str resource: **Required**. Resource name.
    :param str api: **Required**. API name.
    :param str version: **Required**. API version.
    :param str method: **Required**. Method name.
    :param str auth_method: **Required**. Authentication method. Possible values are: **ssl**, **token**.
    :param str http_verb: **Required**. HTTP Verb.
    """
    def __init__(self, resource, api, version, method, http_verb, auth_method, data):
        super(VisaMerchantMeasurementDispatcher, self).__init__(resource=resource,
                                                                api=api,
                                                                version=version,
                                                                method=method,
                                                                http_verb=http_verb,
                                                                auth_method=auth_method,
                                                                data=data)

