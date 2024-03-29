from django.shortcuts import render

class ExternalAccessMiddleware:

  def __init__(self,get_response):
    self.get_response = get_response

  def __call__(self, request):

    external_access_header  = request.headers.get('EXTERNAL_ACCESS')

    # Vérifier si EXTERNAL_ACCESS est défini et vaut 1
    if external_access_header  and external_access_header == '1':

      user_email = request.user.username if request.user.is_authenticated else None

      denied_domains  = ['ccomptes.fr', 'hcfp.fr']

      # Vérifier le domaine de l'e-mail
      if user_email and any(user_email.endswith(domain) or user_email.endswith(f'.{domain}') for domain in denied_domains ):

        return render(request, 'ecc/forbidden.html')

    response = self.get_response(request)

    return response