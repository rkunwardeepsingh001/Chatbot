import os
from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from google.api_core.exceptions import ResourceExhausted
from rest_framework.test import APIClient

os.environ.setdefault("GOOGLE_API_KEY", "test-google-api-key")

from .ai_service import get_ai_response
from .middleware import SimpleCorsMiddleware
from .models import ChatMessage


class ChatViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("chat.views.get_ai_response", return_value="Hello from the bot")
    def test_chat_endpoint_returns_ai_response(self, mock_get_ai_response):
        response = self.client.post(
            "/api/chat/",
            {"message": "Hello"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                "user": "Hello",
                "bot": "Hello from the bot",
            },
        )
        mock_get_ai_response.assert_called_once_with("Hello")

    def test_chat_endpoint_requires_message(self):
        response = self.client.post("/api/chat/", {}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"error": "Message is required"})

    @patch("chat.views.get_ai_response", side_effect=ResourceExhausted("quota exceeded"))
    def test_chat_endpoint_returns_429_when_api_quota_is_exhausted(self, mock_get_ai_response):
        response = self.client.post(
            "/api/chat/",
            {"message": "Hello"},
            format="json",
        )

        self.assertEqual(response.status_code, 429)
        self.assertIn("Gemini API Limit exceeded", response.data["error"])
        mock_get_ai_response.assert_called_once_with("Hello")

    @patch("chat.views.get_ai_response", side_effect=Exception("service down"))
    def test_chat_endpoint_returns_500_when_ai_service_fails(self, mock_get_ai_response):
        response = self.client.post(
            "/api/chat/",
            {"message": "Hello"},
            format="json",
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.data,
            {
                "error": "Chat service is temporarily unavailable. Please try again later.",
            },
        )
        mock_get_ai_response.assert_called_once_with("Hello")


class AIServiceTests(TestCase):
    @patch("chat.ai_service.genai")
    def test_get_ai_response_returns_text_from_gemini(self, mock_genai):
        mock_response = Mock(text="Generated answer")
        mock_chat = Mock()
        mock_chat.send_message.return_value = mock_response
        mock_model = Mock()
        mock_model.start_chat.return_value = mock_chat
        mock_genai.GenerativeModel.return_value = mock_model

        response = get_ai_response("What is CI/CD?")

        self.assertEqual(response, "Generated answer")
        mock_genai.configure.assert_called_once_with(api_key="test-google-api-key")
        mock_genai.GenerativeModel.assert_called_once_with("gemini-flash-latest")
        mock_model.start_chat.assert_called_once_with()
        mock_chat.send_message.assert_called_once_with("What is CI/CD?")

    @patch("chat.ai_service.genai")
    def test_get_ai_response_returns_fallback_when_service_fails(self, mock_genai):
        mock_genai.GenerativeModel.side_effect = Exception("network error")

        response = get_ai_response("Hello")

        self.assertEqual(
            response,
            "The AI service is currently unavailable. Please try again later.",
        )

    @patch("chat.ai_service.genai")
    def test_get_ai_response_returns_quota_message_when_limit_is_exceeded(self, mock_genai):
        mock_genai.GenerativeModel.side_effect = ResourceExhausted("quota exceeded")

        response = get_ai_response("Hello")

        self.assertEqual(
            response,
            "The Gemini API limit exceeded. Please try again later.",
        )


class ChatMessageModelTests(TestCase):
    def test_chat_message_can_be_saved(self):
        message = ChatMessage.objects.create(
            user_message="Hello",
            bot_response="Hi there",
        )

        self.assertEqual(message.user_message, "Hello")
        self.assertEqual(message.bot_response, "Hi there")
        self.assertIsNotNone(message.created_at)


class SimpleCorsMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_allows_localhost_frontend_origin(self):
        middleware = SimpleCorsMiddleware(lambda request: HttpResponse())
        request = self.factory.get("/", HTTP_ORIGIN="http://localhost:5173")

        response = middleware(request)

        self.assertEqual(response["Access-Control-Allow-Origin"], "http://localhost:5173")
        self.assertEqual(response["Access-Control-Allow-Methods"], "GET, POST, OPTIONS, HEAD")
        self.assertEqual(response["Access-Control-Allow-Headers"], "Content-Type")

    def test_options_request_returns_cors_response_without_calling_view(self):
        get_response = Mock()
        middleware = SimpleCorsMiddleware(get_response)
        request = self.factory.options("/", HTTP_ORIGIN="https://example.com")

        response = middleware(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Access-Control-Allow-Origin"], "*")
        get_response.assert_not_called()
