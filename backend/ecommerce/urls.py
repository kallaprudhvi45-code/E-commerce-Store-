from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve
from django.http import FileResponse
import os

def serve_frontend(request, path='index.html'):
    """Serve frontend HTML/CSS/JS files."""
    frontend_dir = settings.FRONTEND_DIR
    file_path = os.path.join(frontend_dir, path)
    
    if os.path.isfile(file_path):
        return FileResponse(open(file_path, 'rb'))
    
    # Fallback to index.html
    index_path = os.path.join(frontend_dir, 'index.html')
    if os.path.isfile(index_path):
        return FileResponse(open(index_path, 'rb'))
    
    from django.http import Http404
    raise Http404("Page not found")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve frontend files - this must be last
    urlpatterns += [
        path('', serve_frontend, {'path': 'index.html'}, name='home'),
        path('<path:path>', serve_frontend, name='frontend'),
    ]
