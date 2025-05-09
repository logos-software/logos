from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods


def home(request):
    """View da página inicial."""
    return HttpResponse('<h1>Bem-vindo ao Logoss</h1>')


@require_http_methods(["GET"])
def health_check(request):
    """
    Health check para verificar se a aplicação está funcionando.
    Útil para monitoramento e testes.
    """
    return JsonResponse({
        'status': 'ok',
        'message': 'Aplicação está funcionando corretamente'
    })
