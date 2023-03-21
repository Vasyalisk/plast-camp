from fastapi import FastAPI


def include_routes(app: FastAPI):
    import routes.auth
    import routes.users

    app.include_router(routes.auth.router, prefix="/auth")
    app.include_router(routes.users.router, prefix="/users")
