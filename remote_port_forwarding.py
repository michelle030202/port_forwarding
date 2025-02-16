import threading
import socket
import logging

logger = logging.getLogger(__name__)


class RemotePortForwarding:
    def __init__(self, ssh_client, remote_host, remote_port, local_port):
        """Initialize remote port forwarding."""
        self.ssh_client = ssh_client
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.local_port = local_port

    def remote_handler(self, chan, local_host, local_port):
        """Handles connections for remote port forwarding."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((local_host, local_port))
            logger.info(f"Remote forwarding: {chan.getpeername()} -> {local_host}:{local_port}")

            while True:
                data = chan.recv(1024)
                if not data:
                    break
                sock.send(data)
                chan.send(sock.recv(1024))

        except Exception as e:
            logger.error(f"Error in remote forwarding: {e}")

        finally:
            sock.close()
            chan.close()
            logger.info(f"Closed remote forwarding channel: {local_host}:{local_port}")

    def forward_remote_port(self):
        """Sets up remote port forwarding."""
        transport = self.ssh_client.get_transport()
        if not transport:
            logger.error("Failed to get SSH transport.")
            return

        transport.request_port_forward("0.0.0.0", self.remote_port)
        logger.info(
            f"Remote port forwarding started: {self.remote_host}:{self.remote_port} -> localhost:{self.local_port}")

        while True:
            chan = transport.accept(10)
            if chan is None:
                continue
            threading.Thread(target=self.remote_handler, args=(chan, "localhost", self.local_port),
                             daemon=True).start()
