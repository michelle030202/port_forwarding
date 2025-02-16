import paramiko
import threading
import logging

from local_port_forwarding import LocalPortForwarding
from remote_port_forwarding import RemotePortForwarding
logger = logging.getLogger(__name__)

# SSH server details
SSH_HOST = 'pubsub.com'  # example
SSH_PORT = 22
SSH_USER = 'user'
SSH_PASSWORD = 'ssh_password'

# Local Port Forwarding: Forward localhost:8080 to remote_host:80
LOCAL_PORT = 8080
REMOTE_HOST = ''
REMOTE_PORT = 80

# Remote Port Forwarding: Forward remote_host:9000 to localhost:5000
REMOTE_FORWARD_PORT = 9000
LOCAL_FORWARD_PORT = 5000


def create_ssh_client():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
    logger.info(f"Connected to {SSH_HOST}.")
    return client


def main():
    """Main function to set up both local and remote port forwarding."""
    ssh_client = create_ssh_client()

    forward_local_port = LocalPortForwarding(ssh_client, LOCAL_PORT, REMOTE_HOST, REMOTE_PORT)
    forward_remote_port = RemotePortForwarding(ssh_client, REMOTE_HOST, LOCAL_FORWARD_PORT, REMOTE_FORWARD_PORT)

    # Start local port forwarding
    threading.Thread(target=forward_local_port.forward_local_port, daemon=True).start()

    # Start remote port forwarding
    threading.Thread(target=forward_remote_port.forward_remote_port, daemon=True).start()


if __name__ == "__main__":
    main()
