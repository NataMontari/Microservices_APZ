#!/bin/bash

# Надсилаємо GET запит
echo "GET request:"
curl -X GET http://localhost:8080/get_messages

# Надсилаємо POST запит
# echo -e "\nSending POST request..."
# curl -X POST http://localhost:8080/send_message -H "Content-Type: application/json" -d '{"message": "Test message"}'