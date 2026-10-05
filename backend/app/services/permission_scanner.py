from fastapi.routing import APIRoute


def scan_permissions(app):
    discovered = set()

    def scan_routes(routes):
        for route in routes:
            # Normal API route
            if isinstance(route, APIRoute):
                permission_name = getattr(
                    route.endpoint,
                    "_permission",
                    None,
                )

                if permission_name:
                    discovered.add(permission_name)

            # FastAPI _IncludedRouter
            original_router = getattr(route, "original_router", None)

            if original_router is not None:
                scan_routes(original_router.routes)

    scan_routes(app.routes)

    return sorted(discovered)