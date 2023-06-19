# plast-camp

**1. Setting up environment variables:**
   - for local development create new `.env` file as `cp .env.local .env`
   - or set your own environment variables


**2. Setting up Docker:**
   - for local development create new `.override.yml` file as `cp docker-compose.override.example.yml docker-compose.override.yml`
   - example file configures and adds local database and Redis services
   - example file sets application to use 8000 port for serving
   - alternatively, specify custom `.override.yml` file
   - build and run image(s) `docker compose up --build`


**3. Database management:**
   - application uses Aerich as a DB management tool for Tortoise ORM
   - in order to set up DB (create Aerich tables) run command `make init-db`
   - to run all migrations from `backend/migrations/models` run `make upgrade`
   - to downgrade one-by-one run `make downgrade`
   - to generate new ones automatically, e.g. when models are changed, run `make migrate`
   - all commands accept Aerich-specific params under the `CMD_ARGS` kwarg
   - for the detailed info see official [Aerich docs](https://github.com/tortoise/aerich)


**4. Managing Python dependencies:**
   - in order to remove / add new Python library, edit `requirements/requirements.in` file
   - then run `make pip-compile` - this will pin package versions according to requirements specs
   - application uses pip tools instead of Poetry due to faster deps resolution of the former


**5. Testing:**
   - run `make test`
   - `make test` accepts additional pytest variables via CMD_ARGS parameter, e. g. `make test CMD_ARGS="-v tests/my_test.py"`


**6. Useful commands:**
   - `make bash` - opens bash console in the running container
   - `make lint` - sorts requirements (alphabetically) and Python imports (according to Black specs)
   - `make chown` - changes ownership of the files to current user (sometimes useful / needed on Linux systems)


**7. Possible Linux ownership issues:**
   - to prevent ownership changes in Linux systems example `.override.yml` file adds user ID
   - alternatively, ownership can be changed via command `make chown`