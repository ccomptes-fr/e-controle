from django.http import HttpResponseForbidden


class ExternalAccessMiddleware:

  def __init__(self,get_response):
    self.get_response = get_response

  def __call__(self, request):

    external_access_header  = request.headers.get('EXTERNAL_ACCESS')

    # Vérifier si EXTERNAL_ACCESS est défini et vaut 1
    if external_access_header  and external_access_header == '1':

      return HttpResponseForbidden("L'accès à l'application est restreint aux utilisateurs externes.")

    response = self.get_response(request)

    return response