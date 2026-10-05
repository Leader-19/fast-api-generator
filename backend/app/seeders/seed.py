from sqlalchemy import select

from app.config.settings import settings
from app.database.connection import SessionLocal
from app.main import app
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User
from app.services.permission_scanner import (
    scan_permissions,
)
from app.services.security_service import (
    hash_password,
)


ROLES = {
    "ADMIN": "System Administrator",
    "ANALYST": "Data Analyst",
    "VIEWER": "Read-only User",
}


# =========================================================
# ROLES
# =========================================================

def seed_roles(db):
    roles = {}

    for role_name, description in ROLES.items():

        role = db.scalar(
            select(Role).where(
                Role.name == role_name
            )
        )

        if role is None:
            role = Role(
                name=role_name,
                description=description,
            )

            db.add(role)
            db.flush()

            print(
                f"[CREATED] Role: {role_name}"
            )

        else:
            print(
                f"[EXISTS] Role: {role_name}"
            )

        roles[role_name] = role

    return roles


# =========================================================
# PERMISSIONS
# =========================================================

def seed_permissions(db):

    discovered_permissions = scan_permissions(
        app
    )

    print("\nDiscovered permissions:")

    for permission_name in discovered_permissions:

        permission = db.scalar(
            select(Permission).where(
                Permission.name
                == permission_name
            )
        )

        if permission is None:

            permission = Permission(
                name=permission_name,
                description=(
                    f"Permission: "
                    f"{permission_name}"
                ),
            )

            db.add(permission)

            print(
                "[CREATED] Permission: "
                f"{permission_name}"
            )

        else:

            print(
                "[EXISTS] Permission: "
                f"{permission_name}"
            )

    db.flush()


# =========================================================
# ADMIN PERMISSIONS
# =========================================================

def assign_all_permissions_to_admin(
    db,
    admin_role,
):

    permissions = db.scalars(
        select(Permission)
    ).all()

    admin_role.permissions = permissions

    db.flush()

    print(
        "[ADMIN] All permissions assigned "
        f"({len(permissions)})"
    )


# =========================================================
# ADMIN USER
# =========================================================

def seed_admin(
    db,
    roles,
):

    admin = db.scalar(
        select(User).where(
            User.email
            == settings.admin_email
        )
    )

    if admin is None:

        admin = User(
            name=settings.admin_name,
            email=settings.admin_email,
            password_hash=hash_password(
                settings.admin_password
            ),
            is_active=True,
        )

        admin.roles.append(
            roles["ADMIN"]
        )

        db.add(admin)
        db.flush()

        print(
            "[CREATED] Admin user: "
            f"{settings.admin_email}"
        )

    else:

        print(
            "[EXISTS] Admin user: "
            f"{settings.admin_email}"
        )

        if roles["ADMIN"] not in admin.roles:
            admin.roles.append(
                roles["ADMIN"]
            )

    assign_all_permissions_to_admin(
        db,
        roles["ADMIN"],
    )


# =========================================================
# SEED
# =========================================================

def seed():

    db = SessionLocal()

    try:

        print(
            "================================"
        )
        print(
            "Roaming Reconciliation Seeder"
        )
        print(
            "================================"
        )

        roles = seed_roles(db)

        seed_permissions(db)

        seed_admin(
            db,
            roles,
        )

        db.commit()

        print(
            "\n================================"
        )
        print(
            "Seeder completed successfully"
        )
        print(
            "================================"
        )

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


if __name__ == "__main__":
    seed()