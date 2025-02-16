import threading
import socket
import logging

logger = logging.getLogger(__name__)


class LocalPortForwarding:
    def __init__(self, ssh_client, local_port, remote_host, remote_port):
        self.ssh_client = ssh_client
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port

    def forward_handler(self, client_sock, transport, remote_host, remote_port):
        """Handles connections for local port forwarding."""
        try:
            channel = transport.open_channel("direct-tcpip", (remote_host, remote_port), client_sock.getpeername())
            if channel is None:
                logger.error("Failed to open SSH channel for forwarding.")
                return

            logger.info(f"Forwarding connection: {client_sock.getpeername()} -> {remote_host}:{remote_port}")

            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                channel.send(data)
                client_sock.send(channel.recv(1024))

        except Exception as e:
            logger.error(f"Error in local forwarding: {e}")

        finally:
            client_sock.close()
            if channel:
                channel.close()
            logger.info(f"Closed connection: {remote_host}:{remote_port}")

    def forward_local_port(self):
        """Sets up local port forwarding."""
        transport = self.ssh_client.get_transport()
        if not transport:
            logger.error("Failed to get SSH transport.")
            return

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", self.local_port))
        server.listen(5)

        logger.info(f"Local port forwarding started: localhost:{self.local_port} -> {self.remote_host}:{self.remote_port}")

        while True:
            client_sock, _ = server.accept()
            threading.Thread(target=self.forward_handler,
                             args=(client_sock, transport, self.remote_host, self.remote_port),
                             daemon=True).start()
