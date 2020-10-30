import logging

import requests
import json
import sys


class rest_api_lib:
    def __init__(self, vmanage_ip, vmanage_port, username, password):
        self.vmanage_ip = vmanage_ip
        self.vmanage_port = vmanage_port
        self.session = {}
        self.login(username, password)

    def login(self, username, password):
        """Login to vmanage"""
        base_url_str = "https://" + str(self.vmanage_ip) + ":" + str(self.vmanage_port)

        login_action = "/j_security_check"

        # Format data for loginForm
        login_data = {"j_username": username, "j_password": password}

        # Url for posting login data
        login_url = base_url_str + login_action

        sess = requests.session()
        # If the vmanage has a certificate signed by a trusted authority change verify to True
        login_response = sess.post(url=login_url, data=login_data, verify=False)

        if b"<html>" in login_response.content:
            print("Login Failed")
            sys.exit(1)

        self.session[self.vmanage_ip] = sess

    def get_token(self):
        get_token_api = "/dataservice/client/token"

        url = "https://" + str(self.vmanage_ip) + ":" + str(self.vmanage_port) + get_token_api

        response = self.session[self.vmanage_ip].get(url, verify=False)

        if response.status_code == 200:
            return response.text
        else:
            return None

    def get_request(self, mount_point):
        """GET request"""
        url = "https://" + str(self.vmanage_ip) + ":" + str(self.vmanage_port) + "/dataservice/" + mount_point

        return self.session[self.vmanage_ip].get(url, verify=False)

    def post_request(self, mount_point, payload):
        """POST request"""
        url = "https://" + str(self.vmanage_ip) + ":" + str(self.vmanage_port) + "/dataservice/" + mount_point

        token = {"X-XSRF-TOKEN": self.get_token()}
        headers = {"Content-Type": "application/json"}
        headers_with_token = {**headers, **token}

        logging.info(f"\n{url}:  url, \nPayload: {payload}, \nHeaders: {headers_with_token}")

        return self.session[self.vmanage_ip].post(
            url=url, data=json.dumps(payload), headers=headers_with_token, verify=False
        )

    def print_software(self, remote_only=True, print_all=False):

        response = json.loads(self.get_request("device/action/software").content)
        print("------------- Software available on vManage -------------------")
        print(
            f"versionType  versionName  versionURL                               platformFamily           availableFiles"
        )
        for item in response["data"]:
            if remote_only and item["versionType"] == "remote":
                print(
                    f"{item['versionType']}     {item['versionName']}    {item['versionURL']} {item['platformFamily']} {item['availableFiles']}"
                )
            elif not remote_only:
                print(
                    f"{item['versionType']}     {item['versionName']}    {item['versionURL']} {item['platformFamily']} {item['availableFiles']}"
                )
        if print_all:
            print(json.dumps(response["data"], indent=4, sort_keys=True))

