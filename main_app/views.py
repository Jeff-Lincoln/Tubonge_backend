# main_app/views.py
from __future__ import annotations
import json
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, Tuple

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from getstream import Stream
from getstream.models import UserRequest
from dotenv import load_dotenv

from .models import StreamUser

# Configure logging with a detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S'
)
logger = logging.getLogger(__name__)

class StreamClient:
    """Singleton class to manage Stream API client instance."""
    _instance = None
    
    def __new__(cls) -> StreamClient:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize Stream client with API credentials."""
        load_dotenv()
        api_key = os.getenv('API_GETSTREAM_PUBLIC_KEY')
        api_secret = os.getenv('API_GETSTREAM_SECRET_KEY')
        
        if not api_key or not api_secret:
            raise ValueError("Missing GetStream API Keys. Check your environment variables.")
        
        self.client = Stream(api_key=api_key, api_secret=api_secret)
        self.api_key = api_key  # Store for logging purposes

class UserManager:
    """Manager class for user operations."""
    
    def __init__(self):
        self.stream = StreamClient()
    
    def create_user_request(self, user_data: Dict[str, Any]) -> UserRequest:
        """Create a UserRequest object for Stream API."""
        current_time = datetime.utcnow().isoformat()
        return UserRequest(
            id=user_data['userId'],
            role="user",
            name=user_data.get('name', user_data['email']),  # Default to email if name not provided
            image=user_data.get('image', ''),
            custom={
                "email": user_data['email'],
                "created_at": current_time,
                "last_active": current_time
            }
        )
    
    def upsert_stream_user(self, user_request: UserRequest) -> None:
        """Upsert user to Stream API with logging."""
        try:
            start_time = time.time()
            # Pass user_request directly, not wrapped in a list
            response = self.stream.client.upsert_users(user_request)
            duration = time.time() - start_time
            
            logger.info(
                f'HTTP Request: POST https://chat.stream-io-api.com/api/v2/users'
                f'?api_key={self.stream.api_key} "HTTP/1.1 201 Created"'
            )
            logger.info(f"User {user_request.id} successfully created/updated")
            logger.debug(f"Stream API call took {duration:.2f} seconds")
            
            return response
        except Exception as e:
            logger.error(f"Stream API error: {str(e)}")
            raise
    
    def generate_token(self, user_id: str, validity_seconds: int = 3600) -> str:
        """Generate a Stream user token with specified validity."""
        token = self.stream.client.create_token(user_id=user_id, expiration=validity_seconds)
        logger.info(f"Generated token for user {user_id}")
        return token

    def process_user(self, data: Dict[str, Any]) -> Tuple[UserRequest, str]:
        """Process user data and return user request and token."""
        user_request = self.create_user_request(data)
        self.upsert_stream_user(user_request)
        token = self.generate_token(data['userId'])
        return user_request, token

def validate_request_data(data: Dict[str, Any]) -> None:
    """Validate required fields in request data."""
    required_fields = ['userId', 'email']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

@csrf_exempt
@require_http_methods(["POST"])
def create_user(request) -> JsonResponse:
    """Handle user creation and token generation endpoint."""
    logger.info("Received request to create user")
    
    try:
        # Parse request data
        data = json.loads(request.body)
        logger.info(f"Request data: {json.dumps(data, indent=2)}")
        
        # Validate request data
        validate_request_data(data)
        
        # Process user
        user_manager = UserManager()
        user_request, token = user_manager.process_user(data)
        
        # Prepare response
        response_data = {
            "token": token,
            "user": {
                "id": user_request.id,
                "name": user_request.name,
                "email": user_request.custom["email"],
                "image": user_request.image,
                "created_at": user_request.custom["created_at"],
                "token_expires_in": 3600
            }
        }
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)
# from __future__ import annotations

# import json
# import logging
# import os
# import time
# from datetime import datetime
# from typing import Any, Dict, Tuple

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# from django.core.exceptions import ValidationError
# from getstream import Stream
# from getstream.models import UserRequest
# from dotenv import load_dotenv

# from .models import StreamUser

# # Configure logging with more detailed format
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     datefmt='%d/%b/%Y %H:%M:%S'
# )
# logger = logging.getLogger(__name__)

# class StreamClient:
#     """Singleton class to manage Stream API client instance."""
#     _instance = None
    
#     def __new__(cls) -> StreamClient:
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             cls._instance._initialize()
#         return cls._instance
    
#     def _initialize(self) -> None:
#         """Initialize Stream client with API credentials."""
#         load_dotenv()
#         api_key = os.getenv('API_GETSTREAM_PUBLIC_KEY')
#         api_secret = os.getenv('API_GETSTREAM_SECRET_KEY')
        
#         if not api_key or not api_secret:
#             raise ValueError("Missing GetStream API Keys. Check your environment variables.")
        
#         self.client = Stream(api_key=api_key, api_secret=api_secret)
#         self.api_key = api_key  # Store for logging purposes

# class UserManager:
#     """Manager class for user operations."""
    
#     def __init__(self):
#         self.stream = StreamClient()
    
#     def create_user_request(self, user_data: Dict[str, Any]) -> UserRequest:
#         """Create a UserRequest object for Stream API."""
#         current_time = datetime.utcnow().isoformat()
#         return UserRequest(
#             id=user_data['userId'],
#             role="user",
#             name=user_data.get('name', user_data['email']),  # Default to email if name not provided
#             image=user_data.get('image', ''),
#             custom={
#                 "email": user_data['email'],
#                 "created_at": current_time,
#                 "last_active": current_time
#             }
#         )
    
#     def upsert_stream_user(self, user_request: UserRequest) -> None:
#         """Upsert user to Stream API with logging."""
#         try:
#             start_time = time.time()
#             response = self.stream.client.upsert_users(user_request)
#             duration = time.time() - start_time
            
#             logger.info(
#                 f'HTTP Request: POST https://chat.stream-io-api.com/api/v2/users'
#                 f'?api_key={self.stream.api_key} "HTTP/1.1 201 Created"'
#             )
#             logger.info(f"User {user_request.id} successfully created/updated")
#             logger.debug(f"Stream API call took {duration:.2f} seconds")
            
#             return response
#         except Exception as e:
#             logger.error(f"Stream API error: {str(e)}")
#             raise
    
#     def generate_token(self, user_id: str, validity_seconds: int = 3600) -> str:
#         """Generate a Stream user token with specified validity."""
#         token = self.stream.client.create_token(user_id=user_id, expiration=validity_seconds)
#         logger.info(f"Generated token for user {user_id}")
#         return token

#     def process_user(self, data: Dict[str, Any]) -> Tuple[UserRequest, str]:
#         """Process user data and return user request and token."""
#         user_request = self.create_user_request(data)
#         self.upsert_stream_user(user_request)
#         token = self.generate_token(data['userId'])
#         return user_request, token

# def validate_request_data(data: Dict[str, Any]) -> None:
#     """Validate required fields in request data."""
#     required_fields = ['userId', 'email']
#     missing_fields = [field for field in required_fields if not data.get(field)]
    
#     if missing_fields:
#         raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

# @csrf_exempt
# @require_http_methods(["POST"])
# def create_user(request) -> JsonResponse:
#     """Handle user creation and token generation endpoint."""
#     logger.info("Received request to create user")
    
#     try:
#         # Parse request data
#         data = json.loads(request.body)
#         logger.info(f"Request data: {json.dumps(data, indent=2)}")
        
#         # Validate request data
#         validate_request_data(data)
        
#         # Process user
#         user_manager = UserManager()
#         user_request, token = user_manager.process_user(data)
        
#         # Prepare response
#         response_data = {
#             "token": token,
#             "user": {
#                 "id": user_request.id,
#                 "name": user_request.name,
#                 "email": user_request.custom["email"],
#                 "image": user_request.image,
#                 "created_at": user_request.custom["created_at"],
#                 "token_expires_in": 3600
#             }
#         }
        
#         return JsonResponse(response_data)
        
#     except json.JSONDecodeError:
#         return JsonResponse({"error": "Invalid JSON data"}, status=400)
#     except ValueError as e:
#         return JsonResponse({"error": str(e)}, status=400)
#     except Exception as e:
#         logger.error(f"Unexpected error: {str(e)}", exc_info=True)
#         return JsonResponse({"error": "An unexpected error occurred"}, status=500)


# # import json
# # import os
# # import logging
# # from datetime import datetime
# # from django.http import JsonResponse
# # from django.views.decorators.csrf import csrf_exempt
# # from django.views.decorators.http import require_http_methods
# # from getstream import Stream
# # from getstream.models import UserRequest
# # from dotenv import load_dotenv

# # # Load environment variables and configure logging
# # load_dotenv()
# # logging.basicConfig(
# #     level=logging.INFO,
# #     format='%(asctime)s - %(levelname)s - %(message)s'
# # )
# # logger = logging.getLogger(__name__)

# # # Initialize Stream client
# # def get_stream_client():
# #     """Initialize and return Stream client with API credentials."""
# #     api_key = os.getenv('API_GETSTREAM_PUBLIC_KEY')
# #     secret = os.getenv('API_GETSTREAM_SECRET_KEY')
    
# #     if not api_key or not secret:
# #         logger.error("Missing GetStream API Keys")
# #         raise ValueError("Missing GetStream API Keys. Check your environment variables.")
    
# #     return Stream(api_key=api_key, api_secret=secret)

# # client = get_stream_client()

# # @csrf_exempt
# # @require_http_methods(["POST"])
# # def create_user(request):
# #     """Handle user creation and token generation using the Stream API."""
# #     logger.info("Received request to create user")
    
# #     try:
# #         # Parse and validate request data
# #         try:
# #             data = json.loads(request.body)
# #             logger.info(f"Request data: {json.dumps(data, indent=2)}")
# #         except json.JSONDecodeError:
# #             logger.error("Invalid JSON data received")
# #             return JsonResponse({"error": "Invalid JSON data"}, status=400)

# #         # Extract and validate required fields
# #         user_id = data.get("userId")
# #         email = data.get("email")
# #         name = data.get("name", "Anonymous")
# #         image = data.get("image", "")

# #         if not user_id or not email:
# #             logger.error(f"Missing required fields: userId={user_id}, email={email}")
# #             return JsonResponse(
# #                 {"error": "Missing required fields: userId and email"}, 
# #                 status=400
# #             )

# #         # Create user request object
# #         current_time = datetime.utcnow().isoformat()
# #         user = UserRequest(
# #             id=user_id,
# #             role="user",
# #             name=name,
# #             image=image,
# #             custom={
# #                 "email": email,
# #                 "created_at": current_time,
# #                 "last_active": current_time
# #             }
# #         )

# #         # Upsert user to Stream
# #         try:
# #             client.upsert_users(user)
# #             logger.info(f"User {user_id} successfully created/updated")
# #         except Exception as e:
# #             logger.error(f"Stream API error: {str(e)}")
# #             return JsonResponse(
# #                 {"error": "Failed to create user in Stream"}, 
# #                 status=503
# #             )

# #         # Generate token with 1-hour validity
# #         validity = 60 * 60  # 1 hour in seconds
# #         token = client.create_token(user_id=user_id, expiration=validity)
# #         logger.info(f"Generated token for user {user_id}")

# #         # Return success response
# #         return JsonResponse({
# #             "token": token,
# #             "user": {
# #                 "id": user_id,
# #                 "name": name,
# #                 "email": email,
# #                 "image": image,
# #                 "created_at": current_time,
# #                 "token_expires_in": validity
# #             }
# #         })

# #     except Exception as e:
# #         logger.error(f"Unexpected error: {str(e)}", exc_info=True)
# #         return JsonResponse(
# #             {"error": "An unexpected error occurred"},
# #             status=500
# #         )


# # # import json
# # # import os
# # # import logging
# # # from datetime import datetime
# # # from django.http import JsonResponse
# # # from django.views.decorators.csrf import csrf_exempt
# # # from django.views.decorators.http import require_http_methods
# # # from getstream import Stream
# # # from getstream.models import UserRequest
# # # from dotenv import load_dotenv

# # # # Load environment variables
# # # load_dotenv()

# # # # Set up logging
# # # logging.basicConfig(
# # #     level=logging.INFO,
# # #     format='%(asctime)s - %(levelname)s - %(message)s'
# # # )
# # # logger = logging.getLogger(__name__)

# # # # Initialize Stream client
# # # api_key = os.getenv('API_GETSTREAM_PUBLIC_KEY')
# # # secret = os.getenv('API_GETSTREAM_SECRET_KEY')

# # # if not api_key or not secret:
# # #     logger.error("Missing GetStream API Keys")
# # #     raise ValueError("Missing GetStream API Keys. Check your environment variables.")

# # # client = Stream(api_key=api_key, api_secret=secret)

# # # @csrf_exempt
# # # @require_http_methods(["POST"])
# # # def create_user(request):
# # #     """Handle user creation and token generation using the Stream API."""
# # #     logger.info("Received request to create user")
    
# # #     try:
# # #         # Parse incoming JSON data
# # #         try:
# # #             data = json.loads(request.body)
# # #             logger.info(f"Request data: {json.dumps(data, indent=2)}")
# # #         except json.JSONDecodeError:
# # #             logger.error("Invalid JSON data received")
# # #             return JsonResponse({"error": "Invalid JSON data"}, status=400)

# # #         # Extract fields from request data
# # #         user_id = data.get("userId")
# # #         email = data.get("email")
# # #         name = data.get("name", "Anonymous")
# # #         image = data.get("image", "")

# # #         # Validate required fields
# # #         if not user_id or not email:
# # #             logger.error(f"Missing required fields: userId={user_id}, email={email}")
# # #             return JsonResponse(
# # #                 {"error": "Missing required fields: userId and email"}, 
# # #                 status=400
# # #             )

# # #         # Create user request object
# # #         user = UserRequest(
# # #             id=user_id,
# # #             role="user",
# # #             name=name,
# # #             image=image,
# # #             custom={
# # #                 "email": email,
# # #                 "created_at": datetime.utcnow().isoformat(),
# # #                 "last_active": datetime.utcnow().isoformat()
# # #             }
# # #         )

# # #         logger.info(f"Attempting to create/update user: {user_id}")

# # #         # Upsert the user using the Stream client
# # #         try:
# # #             response = client.upsert_users(user)
# # #             logger.info(f"Upsert response successful for user: {user_id}")
# # #         except Exception as e:
# # #             logger.error(f"Stream API error: {str(e)}")
# # #             return JsonResponse(
# # #                 {"error": "Failed to create user in Stream"}, 
# # #                 status=503
# # #             )

# # #         # Generate user token (1 hour validity)
# # #         validity = 60 * 60
# # #         token = client.create_token(user_id=user_id, expiration=validity)

# # #         logger.info(f"User {user_id} created with token {token} and validity {validity} seconds")

# # #         # Return success response
# # #         return JsonResponse({
# # #             "token": token,
# # #             "user": {
# # #                 "id": user_id,
# # #                 "name": name,
# # #                 "email": email,
# # #                 "image": image,
# # #                 "created_at": user.custom["created_at"],
# # #                 "token_expires_in": validity
# # #             }
# # #         })

# # #     except Exception as e:
# # #         logger.error(f"Unexpected error: {str(e)}", exc_info=True)
# # #         return JsonResponse(
# # #             {"error": "An unexpected error occurred"}, 
# # #             status=500
# # #         )

# # # # import json
# # # # import os
# # # # import logging
# # # # from django.http import JsonResponse
# # # # from django.views.decorators.csrf import csrf_exempt
# # # # from getstream import Stream
# # # # from getstream.models import UserRequest  # Add this import
# # # # from dotenv import load_dotenv

# # # # # Load environment variables
# # # # load_dotenv()

# # # # # Set up logging
# # # # logger = logging.getLogger(__name__)

# # # # # Initialize Stream client
# # # # api_key = os.getenv('API_GETSTREAM_PUBLIC_KEY')
# # # # secret = os.getenv('API_GETSTREAM_SECRET_KEY')

# # # # if not api_key or not secret:
# # # #     raise ValueError("Missing GetStream API Keys. Check your environment variables.")

# # # # client = Stream(api_key=api_key, api_secret=secret)

# # # # @csrf_exempt
# # # # def create_user(request):
# # # #     """Handles user creation and token generation using the Stream API."""
# # # #     if request.method != "POST":
# # # #         return JsonResponse({"error": "Invalid request method"}, status=400)

# # # #     try:
# # # #         # Parse incoming JSON data
# # # #         data = json.loads(request.body)

# # # #         # Extract fields from request data
# # # #         user_id = data.get("userId")
# # # #         name = data.get("name", "Anonymous")
# # # #         image = data.get("image", "")
# # # #         email = data.get("email")

# # # #         # Check if required fields are provided
# # # #         if not user_id or not email:
# # # #             return JsonResponse({"error": "Missing required fields: userId and email"}, status=400)

# # # #         # Create user request object
# # # #         user = UserRequest(
# # # #             id=user_id,
# # # #             role="user",
# # # #             name=name,
# # # #             image=image,
# # # #             custom={"email": email}
# # # #         )

# # # #         # Log the user creation attempt
# # # #         logger.info(f"Attempting to create/update user: {user}")

# # # #         # Upsert the user using the correct method
# # # #         response = client.upsert_users(user)
        
# # # #         logger.info(f"Upsert response: {response}")

# # # #         # Set token validity (1 hour = 3600 seconds)
# # # #         validity = 60 * 60

# # # #         # Generate the user token
# # # #         token = client.create_token(user_id=user_id, expiration=validity)

# # # #         logger.info(f"User {user_id} created with token {token} and validity {validity} seconds.")

# # # #         # Return the token in the response
# # # #         return JsonResponse({"token": token})

# # # #     except json.JSONDecodeError:
# # # #         return JsonResponse({"error": "Invalid JSON data"}, status=400)
# # # #     except Exception as e:
# # # #         logger.error(f"An error occurred: {str(e)}")
# # # #         return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)