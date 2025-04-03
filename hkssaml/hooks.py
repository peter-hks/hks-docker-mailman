from django.conf import settings
from django.contrib.auth.models import User
from mailmanclient import Client
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

def create_user(user_identity):
    """
    This function is called during the SAML authentication process to create
    or update a user in the Django application and in Mailman.

    :param user_identity: A dictionary containing the mapped SAML attributes.
    """
    # Log the user_identity for debugging
    logger.info(f"User identity received: {user_identity}")

    # Extract user attributes from user_identity
    user_email = user_identity.get('email')
    user_username = user_identity.get('username')
    first_name = user_identity.get('first_name', '')
    last_name = user_identity.get('last_name', '')

    # Ensure required attributes are present
    if not user_email:
        logger.error("Email attribute 'email' not found in user_identity")
        raise ValueError("Email attribute 'email' not found")

    if not user_username:
        logger.error("Username attribute 'username' not found in user_identity")
        raise ValueError("Username attribute 'username' not found")

    # Normalize username (e.g., lowercase)
    user_username = user_username.lower().strip()

    # Attempt to retrieve the existing user
    try:
        user = User.objects.get(username=user_username)
        logger.info(f"Existing user '{user_username}' found")

        # Update user details if necessary
        user.email = user_email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        logger.info(f"User '{user_username}' updated successfully")
    except User.DoesNotExist:
        # Create new user
        user = User.objects.create_user(
            username=user_username,
            email=user_email,
            first_name=first_name,
            last_name=last_name
        )
        logger.info(f"User '{user_username}' created successfully")

    # Ensure the user has the appropriate permissions
    # Adjust these flags according to your needs
    user.is_staff = True  # Set to True if the user should have staff privileges
    user.is_superuser = True  # Set to True if the user should have superuser privileges
    user.save()

    # Proceed to create or update the user in Mailman
    client = Client('http://localhost:8001/3.1', 'restadmin', 'restpass')

    try:
        # Check if the Mailman user already exists
        mailman_user = client.get_user(user_email)
        logger.info(f"Mailman user '{user_email}' already exists")
    except:
        # Create Mailman user if it doesn't exist
        mailman_user = client.create_user(user_email, None)
        logger.info(f"Mailman user '{user_email}' created successfully")

    # Add and verify the email address
    mailman_user.add_address(user_email, absorb_existing=True)
    address = client.get_address(user_email)
    if not address.verified:
        address.verify()
        logger.info(f"Email address '{user_email}' verified")

    # Set preferred address
    mailman_user.preferred_address = user_email

def before_login(user_identity):
    """
    This function is called before the user is logged in.
    You can use it to perform any pre-login actions or checks.
    """
    logger.info(f"Before login hook called with user_identity: {user_identity}")
    # Additional pre-login logic can be added here
