from django.urls import path
from .views import *


urlpatterns = [
    path('news/last', LastNewsView.as_view(), name='last-news'),
    path('news/create', NewsCreateView.as_view(), name='news-create'),
    path('news/<int:id>/update', NewsUpdateView.as_view(), name='news-update'),
    path('request/create', CreateRequestView.as_view(), name='create-request'),
    path('request/active', RequesrListView.as_view(), name='active-request'),
    path('request/<int:id>/setstatus', RequestSetStatusView.as_view(), name='request-set-status')
]
