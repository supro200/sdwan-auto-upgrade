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

isr4331_file_name3 = "isr4300-universalk9.17.03.01a.SPA.bin"
isr4331_version3 = "17.3.1"
isr4331_payload3 = {
    "action": "install",
    "input": {
        "vEdgeVPN": "0",
        "vSmartVPN": 0,
        "data": [{"family": "isr4300", "version": isr4331_version3}],
        "versionType": "remote",
        "reboot": True,
        "sync": True,
    },
    "devices": [{"deviceIP": "3.1.1.133", "deviceId": "ISR4331/K9-FDO230904G3"}],
    "deviceType": "vedge",
}

# ---------- test ISR 1111 file -------------
isr1111_file_name1 = "c1100-universalk9.17.02.02.SPA.bin"
isr1111_version1 = "17.2.2"
isr1111_payload1 = {
    "action": "install",
    "input": {
        "vEdgeVPN": "0",
        "vSmartVPN": 0,
        "data": [{"family": "c1100", "version": isr1111_version1}],
        "versionType": "remote",
        "reboot": False,
        "sync": True,
    },
    "devices": [{"deviceIP": "3.1.1.248", "deviceId": "C1111-8PLTELA-FGL231612VJ"}],
    "deviceType": "vedge",
}

isr1111_file_name2 = "c1100-universalk9.17.03.01a.SPA.bin"
isr1111_version2 = "17.3.1a"
isr1111_payload2 = {
    "action": "install",
    "input": {
        "vEdgeVPN": "0",
        "vSmartVPN": 0,
        "data": [{"family": "c1100", "version": isr1111_version2}],
        "versionType": "remote",
        "reboot": True,
        "sync": True,
    },
    "devices": [{"deviceIP": "3.1.1.248", "deviceId": "C1111-8PLTELA-FGL231612VJ"}],
    "deviceType": "vedge",
}
