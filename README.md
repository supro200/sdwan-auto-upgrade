Introduction

This article describes a possible approach to perform automated upgrades of edge devices in a Cisco SD-WAN environment.

The goal is to simplify and streamline the upgrade process using automated tools.

It is proposed to use Public Cloud infrastructure to store software images and manage access to them using API.

This article specifically focus on Cisco SDWAN infrastructure, but the same approach can be used to upgrade any devices as long as they have Internet access.

This approach has the following benefits:

    The SP doesn't have to host files on-prem, or manage any infrastructure or complex firewall rules which greatly reduces security risks and management overhead
    Software images can be shared using dynamic restricted access URLs
    Endpoints can access the images using their Internet links which reduces a single link utilization if images were stored on a central on-prem server or vManage
    Images can be hosted in different regions, closer to endpoints, which would benefit customers who have global presence
    Images can automatically uploaded on the devices out of business hours reducing engineers' after hours work

Shared Access Signature

The images should be stored in private storage accounts and only exposed during the upgrade using secure access links.

Most of public cloud providers have this feature, in Azure this is called shared access signature (SAS):

https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview

A shared access signature (SAS) provides secure delegated access to resources in your storage account without compromising the security of your data. With a SAS, you have granular control over how a client can access your data. You can control what resources the client may access, what permissions they have on those resources, and how long the SAS is valid, among other parameters.

These signed URL can be generated using API calls and easily integrated with existing automation pipelines.


Meanwhile, Cisco vManage has API endpoints which allow to upgrade controlled devices, offering similar functionality to the GUI.
Solution components and steps

The diagram shows the components of this solution and the required steps described below in more details:

    The automated tool makes API call to Azure, specifying target file and the time limit when this file should be available.
    The API endpoint returns SAS URL which includes unique signature, for example: http://nttsdwantest.blob.core.windows.net/images/isr4300-universalk9.17.02.02.SPA.bin?se=2020-10-28T03%3A48%3A01Z&sp=rt&sv=2019-12-12&sr=b&sig=BUkMvzGhUwKo0J7ASabY42hvMutODyCNljnFkpjeowE%3D
    The automated tool makes API call to vManage to add software with type=remote and URL=SAS

4. The automated tool makes another API call to vManage to initiate the upgrade process with the parameters of Software Version and target device (Device ID/Serial and System IP)

5. vManage returns Job ID to the automated tool which can poll vManage for the Job status.

6. vManage makes netconf RPC call to the router instructing it to download image via HTTP using the SAS URL, install it, and optionally, activate the new image.

7. The router downloads the image from Azure using it's transport Internet connection

8. The router validates the image and installs it. If requested, the new software is activated and the router is rebooted.

9. vManage polls the router to monitor the upgrade process and updates Job ID.


The software images are stored as Azure Blob objects and uploaded there manually (this process can also be automated if necessary)
Costs

Public cloud infrastructure is not free, so it's important to consider possible costs.

There are two components: Cost of storage the files and transfer costs.


Storage costs:

https://azure.microsoft.com/en-au/pricing/details/storage/blobs/

$0.0275 per GB per month for LRS Standard storage tier in region Australia regions

If the average image size is 700 MB and we store 100 images, the cost would be 0.7*100*0.0275 = $1.9 per month
Transfer costs:

https://azure.microsoft.com/en-au/pricing/details/bandwidth/

$0.165 per GB in Australia regions

If the image size is 700MB and the number of sites is 50, the cost of upgrade would be: 0.7GB * 50 * 0.165 = $5.8

There are other costs like read access, but they are counted per 10,000 and cost about 0.07, so it can be safely excluded from the calculations.


Caveats and limitations

This approach was tested on vManage version 20.1 and Cisco IOS-XE devices version 17.2

A significant limitation is that vManage does not accept image URLs if they don't ends with .bin. Meanwhile, Azure generates SAS URLs in a specific format and it's not possible to influence it.

As a workaround an additional key-value pair is added which seems to be ignored by Azure. This satisfied vManage requirements to the file to end with .bin and Azure returns the correct file.

     azure_blob_sas_token_bin = (generate_sas_token(AZURE_STORAGE_ACCOUNT, azure_blob_container, file_name=file_name) + "&ext=.bin")

Correct Azure SAS URL:

http://<account-name>.blob.core.windows.net/images/c1100-universalk9.17.03.01a.SPA.bin?se=2020-10-28T03%3A42%3A32Z&sp=rt&sv=2019-12-12&sr=b&sig=TCpnfN1AKgzrIqhI9H9tpt6EkUBfMDPgBX3wzobG9jY%3D

Modified:

http://<account-name>.blob.core.windows.net/images/c1100-universalk9.17.03.01a.SPA.bin?se=2020-10-28T03%3A42%3A32Z&sp=rt&sv=2019-12-12&sr=b&sig=TCpnfN1AKgzrIqhI9H9tpt6EkUBfMDPgBX3wzobG9jY%3D&ext=.bin


Also noticed that HTTPS does not always work, but HTTP is fine, this need to be confirmed. In any case, there is no confidential information transferred from Azure to end device, images are already signed, so HTTP protocol could be still used.