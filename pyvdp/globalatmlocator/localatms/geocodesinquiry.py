from pyvdp.globalatmlocator.dispatcher import VisaGlobalAtmLocatorDispatcher


def send(data):
    """Submits a Geocode Inquiry request.
    
    :param GeocodesInquiryModel data: **Required**. 
        Instance of :func:`~pyvdp.globalatmlocator.localatms.GeocodesInquiryModel`.
    :return: Response from VDP
     
    **Usage:**
    
    ..  code-block:: python
    
        

        header_kwargs = {
            "applicationId": "GEOCODE",
            "correlationId": "909420141104053819418",
            "requestMessageId": "ICE01-001",
            "userBid": "10000108",
            "userId": "CDISIUserID"        
        }
        
        location_kwargs = {
            "placeName": "San Raphael"
        }
        
        filters = [
            {
                "filterName": "CHIP_ENABLED",
                "filterValue": 1
            },
            {
                "filterName": "ACCESS_HOURS",
                "filterValue": "B"
            }
        ]
        
        range_kwargs = {
            "count": "99",
            "start": "0"
        }
        
        sort_kwargs = {
            "direction": "asc",
            "primary": "distance"        
        }
        
        options_kwargs = {
            "fetchATMOwnerData": "Y",
            "findFilters": filters,
            "range": GeocodesInquiryModel.RequestData.Options.Range(**range_kwargs),
            "sort": GeocodesInquiryModel.RequestData.Options.Sort(**sort_kwargs),
            "useFirstAmbiguous": True
        }

        request_kwargs = {
            "culture": "en-US",
            "distance": "20",
            "distanceUnit": "mi",
            "location": GeocodesInquiryModel.RequestData.Location(**location_kwargs),
            "metaDataOptions": 0,
            "options": GeocodesInquiryModel.RequestData.Options(**options_kwargs)            
        }
        
        data_kwargs = {
            "requestData": GeocodesInquiryModel.RequestData(**request_kwargs),
            "wsRequestHeaderV2": GeocodesInquiryModel.WsRequestHeaderV2(**header_kwargs)
        }
        
        data = GeocodesInquiryModel(**data_kwargs)
        result = geocodesinquiry.send(data=data)
        print(result)
    """
    c = VisaGlobalAtmLocatorDispatcher(method='localatms/geocodesinquiry', data=data)
    return c.send()
