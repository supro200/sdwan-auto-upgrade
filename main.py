# https://pypi.org/project/azure-storage-blob/
# Install manually - pip install azure-storage-blob
import os
from sshtunnel import SSHTunnelForwarder  # ssh tunnel to jump host
from vmanage_api_lib import rest_api_lib
from azure_api_lib import generate_sas_token
from constants import JUMPHOST, VMANAGE, AZURE_STORAGE_ACCOUNT
from test_software import *

SSH_USERNAME = os.environ["SSH_USERNAME"]
SSH_PASSWORD = os.environ["SSH_PASSWORD"]

azure_blob_container = "images"

# ----------- software to test - see test_software.py for definitions -----------------
file_name = isr1111_file_name2
software_version = isr1111_version2
software_install_payload = isr1111_payload2
platform_family = "c1100"

# -------------------------- Build ssh tunnel via jumphost --------------------------

ssh_tunnel = SSHTunnelForwarder(
    JUMPHOST, ssh_username=SSH_USERNAME, ssh_password=SSH_PASSWORD, remote_bind_address=(VMANAGE, 443)
)
ssh_tunnel.daemon_forward_servers = True
ssh_tunnel.start()

print(
    f"SSH tunnel established to target host: {VMANAGE} via {JUMPHOST} "
    f"\nAllocated local port: {ssh_tunnel.local_bind_port}"
)

vmanage_host = "127.0.0.1"  # set vmanage host to local tunnel endpoint
vmanage_connect_port = ssh_tunnel.local_bind_port

# -------------------------- Initialise vManage connection --------------------------
sdwan_controller = rest_api_lib(
    vmanage_ip="127.0.0.1", vmanage_port=vmanage_connect_port, username=SSH_USERNAME, password=SSH_PASSWORD
)

sdwan_controller.print_software(remote_only=True)

# -------------------------- Generate SAS ---------------------------

azure_blob_sas_token_bin = (
    generate_sas_token(AZURE_STORAGE_ACCOUNT, azure_blob_container, file_name=file_name) + "&ext=.bin"
)
print(f"\nGenerated Azure SAS token: {azure_blob_sas_token_bin}")

print(f"-------------------------- Generating remote URL ---------------------------")

add_software_payload = {
    "platformFamily": platform_family,
    "controllerVersionName": "20.1",
    "versionName": software_version,
    "versionURL": azure_blob_sas_token_bin,
}
print(f"\nSending POST request with payload: {add_software_payload}")
response = sdwan_controller.post_request("device/action/software", add_software_payload)
print(f"\nGot response: {response.status_code}, {response.reason}")
if response.status_code != 200:
    ssh_tunnel.stop()
    print(f">>>> Could not generate remote URL. Exiting....")
    exit(1)

sdwan_controller.print_software(remote_only=True, print_all=False)

print(f"-------------------------- Installing software to device ---------------------------")
print(f"\nSending POST request with payload: {software_install_payload}")
response = sdwan_controller.post_request("device/action/install", software_install_payload)
print(f"\nGot response: {response.status_code}, {response.reason}")

ssh_tunnel.stop()
