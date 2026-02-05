from sqlmodel import select
from typing import TypeVar, Generic
from uuid import UUID

T = TypeVar('T')

class UserFilter(Generic[T]):
    """
    Utility class for applying user-based filters to database queries
    to ensure proper data isolation
    """

    @staticmethod
    def apply_user_filter(query, model_class, user_id: UUID):
        """
        Apply a user filter to a query to ensure only data belonging to the user is returned

        Args:
            query: The SQLModel select query
            model_class: The model class to filter on
            user_id: The UUID of the user whose data should be returned

        Returns:
            Modified query with user filter applied
        """
        # Check if the model has a user_id field
        if hasattr(model_class, 'user_id'):
            query = query.where(model_class.user_id == user_id)
        else:
            # For models that don't have a direct user_id,
            # we might need to join with related tables
            raise AttributeError(f"{model_class.__name__} does not have a user_id attribute")

        return query

    @staticmethod
    def get_user_specific_query(model_class, user_id: UUID):
        """
        Create a base query for a model filtered by user

        Args:
            model_class: The model class to query
            user_id: The UUID of the user whose data should be returned

        Returns:
            Select query filtered by user_id
        """
        query = select(model_class)
        return UserFilter.apply_user_filter(query, model_class, user_id)

# Specific filter functions for common use cases
def get_tasks_for_user(user_id: UUID):
    """
    Get a query for all tasks belonging to a specific user
    """
    from ..models.task import Task
    return UserFilter.get_user_specific_query(Task, user_id)

def get_todos_for_user(user_id: UUID):
    """
    Get a query for all todos belonging to a specific user
    """
    from ..models.todo import Todo
    return UserFilter.get_user_specific_query(Todo, user_id)

# Additional helper functions
def verify_user_owns_resource(session, model_class, resource_id: UUID, user_id: UUID) -> bool:
    """
    Verify that a specific resource belongs to the user

    Args:
        session: Database session
        model_class: The model class of the resource
        resource_id: ID of the resource to check
        user_id: ID of the user to verify ownership for

    Returns:
        True if the resource belongs to the user, False otherwise
    """
    query = select(model_class).where(
        model_class.id == resource_id,
        model_class.user_id == user_id
    )

    resource = session.exec(query).first()
    return resource is not None