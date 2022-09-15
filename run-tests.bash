run_test_for_service() {
  eval docker exec -ti "$1" pytest
}

# shellcheck disable=SC2043
for container in my-game-auth_service-1
do
  run_test_for_service $container
done
