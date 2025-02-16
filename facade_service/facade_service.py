from flask import Flask, request, jsonify
import grpc
import uuid
import requests
from proto import logging_pb2
from proto import logging_pb2_grpc


app = Flask(__name__)


channel = grpc.insecure_channel("localhost:50051")
stub = logging_pb2_grpc.LoggingServiceStub(channel)

def get_messages_service_response():
    try:
        # Request to messages_service
        response = requests.get("http://localhost:8082/get_message")
        return response.text  # Returns a text answer
    except requests.RequestException as e:
        return f"Error while calling messages-service: {e}"
    

@app.route("/send_message", methods = ["POST"])
def handle_post():
    msg = request.json.get("message")
    if not msg:
        return jsonify(error="No message provided"), 400
    
    msg_id = str(uuid.uuid4())

    try:
        response = stub.LogMessage(logging_pb2.LogRequest(id=msg_id, message=msg))
        return jsonify(id=msg_id, status=response.status)
    except grpc.RpcError as e:
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