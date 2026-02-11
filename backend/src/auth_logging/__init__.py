"""
Authentication event logging module
"""

import logging
from datetime import datetime
from typing import Dict, Any
import json

# Create logger for authentication events
auth_logger = logging.getLogger('auth_events')
auth_logger.setLevel(logging.INFO)

# Create file handler for auth events
auth_handler = logging.FileHandler('auth_events.log')
auth_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
auth_handler.setFormatter(formatter)

# Add handler to logger
auth_logger.addHandler(auth_handler)

def log_auth_event(event_type: str, user_id: str = None, email: str = None, ip_address: str = None, success: bool = True, details: Dict[str, Any] = None):
    """
    Log an authentication event

    Args:
        event_type: Type of authentication event (login, logout, register, failed_login, etc.)
        user_id: User ID (if available)
        email: User email
        ip_address: IP address of the request
        success: Whether the event was successful
        details: Additional details about the event
    """
    event_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': event_type,
        'user_id': user_id,
        'email': email,
        'ip_address': ip_address,
        'success': success,
        'details': details or {}
    }

    message = json.dumps(event_data)

    if success:
        auth_logger.info(message)
    else:
        auth_logger.warning(message)

__all__ = ['auth_logger', 'log_auth_event']