#!/bin/bash

echo "Loading SQL files into Trino..."
for file in sql/*.sql; do
    echo "Running $file"
    docker exec -i sexi-silverbullet trino < "$file"
done
echo "✅ All done!"
