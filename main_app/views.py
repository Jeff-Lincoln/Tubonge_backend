import json
import os
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from getstream import Stream
from getstream.models import UserRequest  # Add this import
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Stream client
api_key = os.getenv('API_GETSTREAM_PUBLIC_KEY')
secret = os.getenv('API_GETSTREAM_SECRET_KEY')

if not api_key or not secret:
    raise ValueError("Missing GetStream API Keys. Check your environment variables.")

client = Stream(api_key=api_key, api_secret=secret)

@csrf_exempt
def create_user(request):
    """Handles user creation and token generation using the Stream API."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        # Parse incoming JSON data
        data = json.loads(request.body)

        # Extract fields from request data
        user_id = data.get("userId")
        name = data.get("name", "Anonymous")
        image = data.get("image", "")
        email = data.get("email")

        # Check if required fields are provided
        if not user_id or not email:
            return JsonResponse({"error": "Missing required fields: userId and email"}, status=400)

        # Create user request object
        user = UserRequest(
            id=user_id,
            role="user",
            name=name,
            image=image,
            custom={"email": email}
        )

        # Log the user creation attempt
        logger.info(f"Attempting to create/update user: {user}")

        # Upsert the user using the correct method
        response = client.upsert_users(user)
        
        logger.info(f"Upsert response: {response}")

        # Set token validity (1 hour = 3600 seconds)
        validity = 60 * 60

        # Generate the user token
        token = client.create_token(user_id=user_id, expiration=validity)

        logger.info(f"User {user_id} created with token {token} and validity {validity} seconds.")

        # Return the token in the response
        return JsonResponse({"token": token})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)