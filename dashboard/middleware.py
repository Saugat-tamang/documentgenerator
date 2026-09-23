from django.contrib.auth import logout

class ClientMiddleware:
    def __init__(self, get_response):
        self.get_response                   = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            client_id                       = request.session.get('client_id')
            if client_id:
                request.client_id           = client_id
        return self.get_response(request)