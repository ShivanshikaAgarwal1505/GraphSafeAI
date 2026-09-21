from datetime import datetime
import email
import traceback

from shared.database.models.user import (
    User,
)

from shared.security.password import (
    hash_password,
    verify_password,
)

from shared.security.jwt import (
    create_access_token,
)

from services.authentication.infrastructure.user_repository import (
    UserRepository,
)


repository = UserRepository()


class AuthService:

    def register(
        self,
        db,
        name: str,
        email: str,
        password: str,
    ):

        existing_user = (
            repository.get_by_email(
                db,
                email,
            )
        )

        if existing_user:

            raise ValueError(
                "Email already exists."
            )
            
        try:
            hashed = hash_password(password)
            print("HASHED:", hashed)

        except Exception as e:
            import traceback

            print("HASH FAILED")
            traceback.print_exc()
            raise

        user = User(
            name=name,
            email=email,
            password_hash=hashed,
        )

        return repository.create(
            db,
            user,
        )

    def login(
        self,
        db,
        email: str,
        password: str,
    ):

        user = (
            repository.get_by_email(
                db,
                email,
            )
        )

        if user is None:

            raise ValueError(
                "Invalid credentials."
            )

        if not verify_password(
            password,
            user.password_hash,
        ):

            raise ValueError(
                "Invalid credentials."
            )

        user.last_login_at = (
            datetime.utcnow()
        )

        repository.save(
            db,
        )

        token = create_access_token(
            user.id
        )

        return {
            "access_token": token,
            "user": user,
        }

    def get_user(
        self,
        db,
        user_id: int,
    ):

        return repository.get_by_id(
            db,
            user_id,
        )