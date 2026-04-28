from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

class SimpleCorsMiddleware:

    def __init__(self, get_response):
        logger.debug("Initializing SimpleCorsMiddleware")
        self.get_response = get_response

    def __call__(self, request):
        logger.debug("Processing request with method: %s", request.method)
        if request.method == 'OPTIONS':
            response = HttpResponse()
            logger.debug("Handling options request")
        else:
            logger.error("Received non-OPTIONS request in SimpleCorsMiddleware: %s", request.method)
            response = self.get_response(request)

        origin = request.headers.get('Origin')
        logger.debug("Request origin: %s", origin)
        if origin in ('http://localhost:5173', 'http://127.0.0.1:5173'):
            response['Access-Control-Allow-Origin'] = origin
            logger.debug("Set Access-Control-Allow-Origin to: %s", origin)
        else:
            response['Access-Control-Allow-Origin'] = '*'
            logger.debug("Set Access-Control-Allow-Origin to: %s", '*')
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
