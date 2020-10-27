import os
from datetime import datetime, timedelta
from azure.storage.blob import BlobSasPermissions, generate_blob_sas

AZURE_PRIMARY_KEY = os.environ["AZURE_PRIMARY_KEY"]


def generate_sas_token(storage_account_name, container_name, file_name):
    sas = generate_blob_sas(
        account_name=storage_account_name,
        account_key=AZURE_PRIMARY_KEY,
        container_name=container_name,
        blob_name=file_name,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=2),
    )

    sas_url = (
        "http://" + storage_account_name + ".blob.core.windows.net/" + container_name + "/" + file_name + "?" + sas
    )
    return sas_url
