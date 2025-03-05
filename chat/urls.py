from django.urls import path

from chat.views import ChatListView, ChatCreateView, ChatUpdateView, ChatDeleteView, ChatView

app_name = 'chat'

urlpatterns = [
    path("", ChatListView.as_view(), name="chat_list"),
    path("create/", ChatCreateView.as_view(), name="chat_create"),
    path("<int:pk>/update/", ChatUpdateView.as_view(), name="chat_update"),
    path("<int:pk>/delete/", ChatDeleteView.as_view(), name="chat_delete"),
    path("<int:chat_id>/", ChatView.as_view(), name="chat"),
]
