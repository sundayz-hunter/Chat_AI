import asyncio
import json

import markdown2
import ollama
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth import get_user_model

from chat.models import Chat, ChatMessage

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """Handles real-time chat communication using WebSockets.

    This consumer manages the WebSocket connection, receives user messages,
    streams AI responses, and saves the conversation to the database.
    """

    async def connect(self):
        """Handles the initial WebSocket connection.

        Adds the consumer to the chat room group and accepts the connection.
        """
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Handles the WebSocket disconnection.

        Removes the consumer from the chat room group.
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handles receiving messages from the WebSocket.

        Receives user messages, streams AI responses, and saves the conversation.
        """
        data = json.loads(text_data)
        user_message = data["message"]

        # Send user message to frontend
        await self.send(text_data=json.dumps({"message": user_message, "sender": "user"}))

        # Get chat
        chat = await self.get_chat(self.chat_id)
        if not chat:
            return

        # Stream AI response
        ai_response = ""
        raw_markdown_response = ""
        stream = ollama.chat(
            model=settings.AI_MODEL,
            messages=[{"role": "user", "content": user_message}],
            stream=True
        )

        for chunk in stream:
            raw_markdown_response += chunk["message"]["content"]
            formatted_html = markdown2.markdown(raw_markdown_response)

            # Send each chunk immediately
            await self.send(text_data=json.dumps({"message": formatted_html, "sender": "ai"}))
            await asyncio.sleep(0.05)  # Small delay to allow frontend to process

        # Save full AI response
        await self.save_message(chat, self.scope["user"], user_message, formatted_html)

        # **Explicitly Close WebSocket After AI Response is Sent**
        await self.send(text_data=json.dumps({"close": True}))  # Notify frontend to close
        await self.close()  # Close WebSocket connection

    @sync_to_async
    def get_chat(self, chat_id):
        """Retrieves a chat object from the database.

        Attempts to fetch the chat object based on the provided chat_id.
        """
        try:
            return Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return None

    @sync_to_async
    def save_message(self, chat, user, user_message, formatted_html):
        """Saves a chat message and AI response to the database.

        Creates a new ChatMessage object with the provided information.
        """
        ChatMessage.objects.create(
            chat=chat, user=user, message=user_message, response=formatted_html
        )
