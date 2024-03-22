import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP trigger function that takes an HttpRequest object as input and returns an HttpResponse object.
    
    Args:
        req (func.HttpRequest): The HTTP request object containing the request details.
        
    Returns:
        func.HttpResponse: The HTTP response object containing the response data.
    """
    logging.warn("Host=\"{}\"".format(req.headers.get('Host')))
    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        logging.info("name=\"{}\"".format(name))
        return func.HttpResponse(f"Hey, Mr. {name}. This HTTP triggered function executed successfully.", status_code=200)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )