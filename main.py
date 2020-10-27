# https://pypi.org/project/azure-storage-blob/
# Install manually - pip install azure-storage-blob
import json
import os
from sshtunnel import SSHTunnelForwarder  # ssh tunnel to jump host
from vmanage_api_lib import rest_api_lib
from azure_api_lib import generate_sas_token
from constants import JUMPHOST, VMANAGE, AZURE_STORAGE_ACCOUNT

SSH_USERNAME = os.environ["SSH_USERNAME"]
SSH_PASSWORD = os.environ["SSH_PASSWORD"]

azure_blob_container = "images"

# ---------- test ASR 1001-X file --------------
asr_1001x_file_name1 = "asr1001x-universalk9.17.03.01a.SPA.bin"
asr_1001x_version1 = "17.3.1"
asr_1001x_payload1 = {
    "action": "install",
    "input": {
        "vEdgeVPN": "0",
        "vSmartVPN": 0,
        "data": [{"family": "asr1001x", "version": asr_1001x_version1}],
        "versionType": "remote",
        "reboot": False,
        "sync": True,
    },
    "devices": [{"deviceIP": "3.1.1.250", "deviceId": "ASR1001-X-JAE2310048V"}],
    "deviceType": "vedge",
}

# ---------- test ISR 4331 file -------------
isr4331_file_name1 = "isr4300-universalk9.17.03.01a.SPA.bin"
isr4331_version1 = "17.3.1"
isr4331_payload1 = {
    "action": "install",
    "input": {
        "vEdgeVPN": "0",
        "vSmartVPN": 0,
        "data": [{"family": "isr4300", "version": isr4331_version1}],
        "versionType": "remote",
        "reboot": False,
        "sync": True,
    },
    "devices": [{"deviceIP": "3.1.1.133", "deviceId": "ISR4331/K9-FDO230904G3"}],
    "deviceType": "vedge",
}

isr4331_file_name2 = "isr4300-universalk9.17.02.02.SPA.bin"
isr4331_version2 = "17.2.2"
isr4331_payload2 = {
    "action": "install",
    "input": {
        "vEdgeVPN": "0",
        "vSmartVPN": 0,
        "data": [{"family": "isr4300", "version": isr4331_version2}],
        "versionType": "remote",
        "reboot": False,
        "sync": True,
    },
    "devices": [{"deviceIP": "3.1.1.133", "deviceId": "ISR4331/K9-FDO230904G3"}],
    "deviceType": "vedge",
}

# ----------- software to test -----------------
file_name = asr_1001x_file_name1
software_version = asr_1001x_version1
software_install_payload = asr_1001x_payload1

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
        generate_sas_token(AZURE_STORAGE_ACCOUNT, azure_blob_container, file_name=file_name) + "&ext=.bin")
print(f"\nGenerated Azure SAS token: {azure_blob_sas_token_bin}")

print(f"-------------------------- Generate remote URL ---------------------------")
test_payload = {"controllerVersionName": "20.1", "versionName": software_version, "versionURL": azure_blob_sas_token_bin}
print(f"\nSending POST request with payload: {test_payload}")
response = sdwan_controller.post_request("device/action/software", test_payload)
print(f"\nGot response: {response.status_code}, {response.reason}")
if response.status_code != 200:
    ssh_tunnel.stop()
    print(f">>>> Could not generate remote URL. Exiting....")
    exit(1)

sdwan_controller.print_software(remote_only=True, print_all=False)

print(f"-------------------------- Installing software to device ---------------------------")
print(f"\nSending POST request with payload: {software_install_payload}")
response = sdwan_controller.post_request("device/action/install", software_install_payload)
print(f"\nGot response: {response.reason}")

ssh_tunnel.stop()
