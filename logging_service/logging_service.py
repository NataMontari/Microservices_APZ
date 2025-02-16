import grpc
from concurrent import futures
import logging
from proto import logging_pb2
from proto import logging_pb2_grpc
class LoggingService(logging_pb2_grpc.LoggingServiceServicer):
    def __init__(self):
        self.messages = {}
    
    def LogMessage(self, request, context):
        self.messages[request.id] = request.message
        return logging_pb2.LogResponse(status = "Message logged successfully")
    
    def GetMessages(self, request, context):
        return logging_pb2.MessagesResponse(messages = list(self.messages.values()))
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    logging_pb2_grpc.add_LoggingServiceServicer_to_server(LoggingService(), server)
    server.add_insecure_port('[::]:50051')

    logging.info("Starting gRPC server on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()