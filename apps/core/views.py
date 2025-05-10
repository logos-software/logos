from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "username": user.get_username(),
            }
        )
        return context


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
