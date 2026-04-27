import argparse
import os
import paramiko
import subprocess
import json

def get_worker_node_ip():
    # Get worker node IPs using oc get nodes -o wide
    try:
        result = subprocess.check_output([
            'oc', 'get', 'nodes', '-o', 'json'
        ], text=True)
        nodes = json.loads(result)
        for node in nodes['items']:
            if any(t['key'] == 'node-role.kubernetes.io/worker' for t in node['metadata'].get('labels', [])):
                # Use the first worker node
                return node['status']['addresses'][0]['address']
        # fallback: just use the first node
        return nodes['items'][0]['status']['addresses'][0]['address']
    except Exception as e:
        print(f"Error getting worker node IP: {e}")
        return None

def get_config_service_port(namespace):
    # Get config-service NodePort using oc get svc -n <namespace> lrb-2511-mtcil -o json
    try:
        result = subprocess.check_output([
            'oc', 'get', 'svc', '-n', namespace, 'lrb-2511-mtcil', '-o', 'json'
        ], text=True)
        svc = json.loads(result)
        # Find the NodePort for port 31751 (or any port you want)
        for port in svc['spec']['ports']:
            if port['port'] == 31751 or port['name'] == 'ssh' or port['targetPort'] == 31751:
                return port['nodePort']
        # fallback: just use the first NodePort
        return svc['spec']['ports'][0]['nodePort']
    except Exception as e:
        print(f"Error getting config-service port: {e}")
        return None

def update_config_via_ssh(host, port, user, password, commands):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=user, password=password)
    for cmd in commands:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
    ssh.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', required=True, help='Target microservice (e.g., udm, udr)')
    parser.add_argument('--namespace', required=False, default='lrb-2511-mtcil', help='Namespace for config-service')
    args = parser.parse_args()

    SSH_USER = os.getenv('SSH_USER', 'admin')
    SSH_PASS = os.getenv('SSH_PASS', 'password')

    # Dynamically get worker node IP and config-service port
    SSH_HOST = get_worker_node_ip()
    SSH_PORT = get_config_service_port(args.namespace)

    if not SSH_HOST or not SSH_PORT:
        print("Could not determine SSH host or port. Exiting.")
        exit(1)

    commands = [
        # Replace with actual CLI commands
        f'echo "Set log level for {args.target}"'
    ]
    update_config_via_ssh(SSH_HOST, SSH_PORT, SSH_USER, SSH_PASS, commands)
