
#!/bin/bash

docker exec --tty $(docker compose ps -q api) /bin/bash -c "cd src && MP_ENVIRONMENT=development alembic upgrade head"