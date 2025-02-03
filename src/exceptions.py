from fastapi import HTTPException, status

INVALID_LOGIN_DATA_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password"
)

USER_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

CREDENTIALS_INVALID_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={'WWW-Authenticate': 'Bearer'}
)

TOKEN_EXPIRE_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token expired",
    headers={'WWW-Authenticate': 'Bearer'}
)

TOKEN_BLACKLISTED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token blacklisted",
    headers={'WWW-Authenticate': 'Bearer'}
)

ROLE_PERMISSION_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have the rights to perform this action"
)

UPDATE_USER_FAILED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No changes have been made"
)
