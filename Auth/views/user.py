from django.http import HttpRequest
from django.views.defaults import page_not_found
import logging

logger = logging.getLogger("django")



def custom_404_handler(request: HttpRequest, exception):
    # Get request information

    # Log the path, the user making the request, and META information
    logger.warning(
        f"404 Not Found - Path: {request.path} - User: {request.user}",
    )

    # Log the HTTP method
    logger.warning(f"404 Not Found - Method: {request.method}")

    # Log the path and the request body
    logger.warning(
        f"404 Not Found - Path: {request.path} & Body: {request.body}"
    )

    # Log the request information
    logger.warning(f"404 Not Found - Request Information: {request.body} {request.path} {request.user}")

    # Call the default 404 handler to render the error page
    return page_not_found(request, exception)