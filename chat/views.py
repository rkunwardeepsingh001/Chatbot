from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from google.api_core.exceptions import ResourceExhausted
from .ai_service import get_ai_response


@api_view(['POST'])
def chat_view(request):
    user_message = request.data.get("message")

    if not user_message:
        return Response({"error": "Message is required"}, status=400)

    try:
        response = get_ai_response(user_message)
    except ResourceExhausted:
        return Response(
            {"error": "Gemini API quota exceeded. Please check your Google Cloud quota or try again later."},
            status=429,
        )
    except Exception:
        return Response(
            {"error": "Chat service is temporarily unavailable. Please try again later."},
            status=500,
        )

    return Response({
        "user": user_message,
        "bot": response
    })