from fastapi import FastAPI


def include_routes(app: FastAPI):
    import routes.auth
    import routes.camps
    import routes.shared
    import routes.users

    app.include_router(routes.auth.router, prefix="/auth")
    app.include_router(routes.users.router, prefix="/users")
    app.include_router(routes.camps.router, prefix="/camps")
    app.include_router(routes.shared.router, prefix="/shared")
