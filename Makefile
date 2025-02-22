.PHONY: init test deploy

init:
    echo "unimplemented yet" && exit 1
    docker-compose build
    docker-compose run --rm backend flask db upgrade

test:
    echo "unimplemented yet" && exit 1
    docker-compose run --rm backend pytest tests/unit
    docker-compose run --rm backend pytest tests/integration

deploy:
    echo "unimplemented yet" && exit 1
    docker stack deploy -c docker/compose/docker-compose.yml grading