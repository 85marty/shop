from django.urls import path
from .views import MemberListView, MemberDetailView, MemberUpdateView, login_view, register_view, logout_view, \
    MemberDeleteView

urlpatterns = [
    path('', MemberListView.as_view(), name='member_list'),
    path('<int:pk>/', MemberDetailView.as_view(), name='member_detail'),
    path('edit/<int:pk>', MemberUpdateView.as_view(), name='member_edit'),
    path('delete/<int:pk>', MemberDeleteView.as_view(), name='member_delete'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registration/', register_view, name='register')
]
