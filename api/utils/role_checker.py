from fastapi import HTTPException, status


class RoleChecker:

    @staticmethod
    def is_superuser(role: str) -> None:
        if role != "super_user":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="u dont have rights for this action"
            )
        