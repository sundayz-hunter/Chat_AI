import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from chat.models import Chat
from chat.forms import ChatForm


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = "chat/chat_list.html"
    context_object_name = "chats"
    form_class = ChatForm

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context


class ChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    form_class = ChatForm
    template_name = "chat/chat_create.html"
    success_url = reverse_lazy("chat:chat_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        if self.request.htmx:
            response = render(self.request, "chat/partials_chat_row.html", {'chat': self.object})
            response['HX-Trigger'] = json.dumps({
                'chatCreated': {
                    'url': reverse('chat:chat', args=[self.object.id])
                }
            })
            return response
        return super().form_valid(form)


class ChatUpdateView(LoginRequiredMixin, UpdateView):
    model = Chat
    form_class = ChatForm
    template_name = "chat/chat_edit.html"
    success_url = reverse_lazy("chat:chat_list")

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)

    def form_valid(self, form):
        chat = form.save()
        if self.request.htmx:
            response = render(self.request, "chat/partials_chat_row.html", {"chat": chat})
            response['HX-Trigger'] = json.dumps({
                'chatUpdated': {
                    'url': reverse('chat:chat', args=[chat.id])
                }
            })
            return response
        return super().form_valid(form)


class ChatDeleteView(LoginRequiredMixin, DeleteView):
    model = Chat
    template_name = "chat/chat_confirm_delete.html"
    success_url = reverse_lazy("chat:chat_list")

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        chat = self.get_object()
        response = super().delete(request, *args, **kwargs)
        if self.request.htmx:
            response = HttpResponse("")
            response["HX-Trigger"] = json.dumps({
                "chatDeleted": {
                    "id": chat.id,
                    "name": chat.name
                }
            })
            return response
        return response


class ChatView(LoginRequiredMixin, View):
    template_name = "chat/chat.html"

    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id, user=request.user)
        messages = chat.chatmessage_set.all().order_by("timestamp")
        chats = Chat.objects.filter(user=request.user).order_by("-created_at")
        return render(request, self.template_name,{"chat": chat, "messages_chat": messages, "chats": chats})
