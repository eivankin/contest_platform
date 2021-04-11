from .forms import RegisterForm


def login_form_middleware(get_response):
    """
    I'm too lazy to pass login form in each template render,
    so I made this middleware.
    """

    def middleware(request):
        request.login_form = RegisterForm()
        return get_response(request)

    return middleware
