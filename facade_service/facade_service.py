from flask import Flask, request, jsonify
import grpc
import uuid
import requests
import logging
from proto import logging_pb2
from proto import logging_pb2_grpc
from tenacity import retry, stop_after_attempt, wait_exponential

app = Flask(__name__)


channel = grpc.insecure_channel("localhost:8081")
stub = logging_pb2_grpc.LoggingServiceStub(channel)

def get_messages_service_response():
    try:
        # Request to messages_service
        response = requests.get("http://localhost:8082/get_message")
        return response.text  # Returns a text answer
    except requests.RequestException as e:
        return f"Error while calling messages-service: {e}"
    
    
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def log_message_with_retry(message_uuid: str, message: str):
    try:
        print(f"Attempting to send message: {message}")
        
        request = logging_pb2.LogRequest(id=message_uuid, message=message)
        response = stub.LogMessage(request)  # call gRPC
        
        if response.status == "Message logged successfully":
            print(f" Message successfully logged: {response.status}")
            return {"status": "success", "message": response.status}
        elif response.status == "Duplicate message ignored":
            print(f"Duplicate send: {response.status}")
            return {"status": "duplicate", "message": response.status}
        else:
            print(f"Attempt failed: {response.status}")
            return {"status": "failed", "message": response.status}

    except grpc.RpcError as e:
        print(f"[gRPC error: {e.code().name} - {e.details()}")
        raise  # repeat the call

@app.route("/send_message", methods=["POST"])
def handle_post():
    msg = request.json.get("message")
    if not msg:
        return jsonify(error="No message provided"), 400
    
    msg_id = str(uuid.uuid4())  # Генеруємо унікальний UUID
    logging.info(f"Received message: {msg}")

    try:
        response = log_message_with_retry(msg_id, msg)  # Calling function with retry
        return jsonify(id=msg_id, **response)  # Returning the response
    except grpc.RpcError as e:
        logging.error(f"Failed to send message: {e}")
        return jsonify(error=f"Logging service error: {e}"), 500

    
@app.route("/get_messages", methods = ["GET"])
def handle_get():
    try:
        response = stub.GetMessages(logging_pb2.Empty())
        logging_messages = list(response.messages)

        messages_service_response = get_messages_service_response()

        combined_response = {"logged_messages": logging_messages, "message_from_service": messages_service_response} 

        return jsonify(combined_response)
    except grpc.RpcError as e:
        return jsonify(error=f"Service error: {e}"), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify(error=f"Unexpected error: {e}"), 500


if __name__ == "__main__":
    app.run(port = 8080)