from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from getstream import Stream
from .models import User as UserModel  # Assuming you have a User model

# Initialize Stream client with API keys from environment variables
api_key = os.getenv('API_GETSTREAM_PUBLIC_KEY')
secret = os.getenv('API_GETSTREAM_SECRET_KEY')

if not api_key or not secret:
    raise ValueError("Missing GetStream API Keys. Check your environment variables.")

client = Stream(api_key, secret)


@csrf_exempt
def generate_user_token(request):
    """Handles the creation of a user token using the Stream API and saves the user in the database."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        # Parse incoming JSON data
        data = json.loads(request.body)
        email = data.get("email")  # Expecting email as user ID
        name = data.get("name", "Anonymous")  # Default to "Anonymous" if name is not provided
        image = data.get("image", "")  # Default to empty string if image is not provided

        # Ensure that the email is provided
        if not email:
            return JsonResponse({"error": "Missing required field: email"}, status=400)

        # Create a unique user ID from email
        user_id = email  # Using email as user ID

        # Create the user object for the Stream API
        new_user = {
            "id": user_id,
            "role": "user",
            "name": name,
            "image": image,
            "custom": {
                "email": email,
            },
        }

        # Upsert the user in the Stream API
        client.upsert_users([new_user])

        # Set token validity (1 hour = 3600 seconds)
        validity = 60 * 60

        # Generate the user token
        token = client.create_token(user_id, {"expires_in": validity})

        # Save or update user in the PostgreSQL database
        user, created = UserModel.objects.update_or_create(
            email=email,
            defaults={
                'name': name,
                'image': image,
                'role': 'user',
            },
        )

        # Log the token creation process
        print(f"User {email} created with token {token} and validity {validity}")

        # Return token in JSON response
        return JsonResponse({"token": token})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


# # views.py

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# import os
# from getstream import Stream
# from .models import User as UserModel  # Assuming you have a User model

# # Initialize Stream client with API keys from environment variables
# api_key = os.getenv('API_GETSTREAM_PUBLIC_KEY')
# secret = os.getenv('API_GETSTREAM_SECRET_KEY')

# if not api_key or not secret:
#     raise ValueError("Missing GetStream API Keys. Check your environment variables.")

# client = Stream(api_key, secret)


# @csrf_exempt
# def generate_user_token(request):
#     """Handles the creation of a user token using the Stream API and saves the user in the database."""
#     if request.method != "POST":
#         return JsonResponse({"error": "Invalid request method"}, status=400)

#     try:
#         # Parse incoming JSON data
#         data = json.loads(request.body)
#         user_id = data.get("userId")
#         name = data.get("name", "Anonymous")  # Default to "Anonymous" if name is not provided
#         image = data.get("image", "")  # Default to empty string if image is not provided
#         email = data.get("email", "")  # Default to empty string if email is not provided

#         # Ensure that the user ID is provided
#         if not user_id:
#             return JsonResponse({"error": "Missing required field: userId"}, status=400)

#         # Create the user object for the Stream API
#         new_user = {
#             "id": user_id,
#             "role": "user",
#             "name": name,
#             "image": image,
#             "custom": {
#                 "email": email,
#             },
#         }

#         # Upsert the user in the Stream API
#         client.upsert_users([new_user])

#         # Set token validity (1 hour = 3600 seconds)
#         validity = 60 * 60

#         # Generate the user token
#         token = client.create_token(user_id, {"expires_in": validity})

#         # Save or update user in the PostgreSQL database
#         user, created = UserModel.objects.update_or_create(
#             user_id=user_id,
#             defaults={
#                 'name': name,
#                 'image': image,
#                 'email': email,
#                 'role': 'user',
#             },
#         )

#         # Log the token creation process
#         print(f"User {user_id} created with token {token} and validity {validity}")

#         # Return token in JSON response
#         return JsonResponse({"token": token})

#     except json.JSONDecodeError:
#         return JsonResponse({"error": "Invalid JSON data"}, status=400)
#     except Exception as e:
#         return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
