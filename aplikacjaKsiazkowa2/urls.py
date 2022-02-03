# -*- coding: utf-8 -*-

# Examples:
# Function views
#    1. Add an import:  from my_app import views
#    2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#    1. Add an import:  from other_app.views import Home
#    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#    1. Import the include() function: from django.urls import include, path
#    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))


from django.urls import path
from . import views

from .views import ListBookView, IndexView, BookCreateView, BookDeleteView

app_name = 'aplikacjaKsiazkowa2'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add_book', BookCreateView.as_view(), name='add_book'),
    # path('edit_book/<str:pk>', views.BookUpdateView.as_view(), name='edit_book'),
    path('delete/<str:pk>', BookDeleteView.as_view(), name='delete_book'),
    path('lista', ListBookView.as_view(), name='lista'),
]
