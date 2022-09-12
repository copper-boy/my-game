run_test_for_service() {
  eval docker exec -ti "$1" pytest
}

for container in my-game-auth_service-1 my-game-logic_service-1 my-game-handler_service-1
do
  run_test_for_service $container
done
