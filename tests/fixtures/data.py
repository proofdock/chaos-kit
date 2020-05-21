def provide_experiment():
    return {
        "version": "1.0.0",
        "title": "Restart a random node",
        "description": "This test will restart a random node",
        "tags": [
            "azure"
        ],
        "configuration": {
            "azure_subscription_id": "a27e1234-c260-4ac3-8f37-82cded6fb495"
        },
        "secrets": {
            "azure": {
                "client_id": "11115617-a3ef-bbbb-aaaa-2cb92cb91111",
                "client_secret": "secret_secret",
                "tenant_id": "54da8059-1111-1111-bbbb-55b705df1111"
            }
        },
        "steady-state-hypothesis": {
            "title": "Check if web cluster is responding",
            "probes": [
                {
                    "type": "probe",
                    "name": "service-must-respond",
                    "tolerance": 200,
                    "provider": {
                        "type": "http",
                        "url": "https://www.proofdock.io/"
                    }
                }
            ]
        },
        "method": [
            {
                "type": "action",
                "name": "Restart a random node",
                "provider": {
                    "type": "python",
                    "module": "chaosazure.machine.actions",
                    "func": "restart_machines",
                    "secrets": [
                        "azure"
                    ],
                    "config": [
                        "azure_subscription_id"
                    ]
                }
            }
        ],
        "rollbacks": []
    }


def provide_settings():
    return {
        "run_context": {
            "no_upload": False
        }
    }


def provide_journal():
    return {
        "chaoslib-version": "1.9.0",
        "platform": "Linux-4.4.0-18362-Microsoft-x86_64-with-Ubuntu-18.04-bionic",
        "node": "DESKTOP-10FVIE5",
        "experiment": {
            "version": "1.0.0",
            "title": "Restart a random node in web cluster",
            "description": "This test will restart a random node in the web cluster",
            "tags": [
                "azure"
            ],
            "steady-state-hypothesis": {
                "title": "Check if web cluster is responding",
                "probes": [
                    {
                        "type": "probe",
                        "name": "service-must-respond",
                        "tolerance": 200,
                        "provider": {
                            "type": "http",
                            "url": "https://www.proofdock.io/"
                        }
                    }
                ]
            },
            "method": [
                {
                    "type": "action",
                    "name": "Restart a random node in the web cluster",
                    "provider": {
                        "type": "python",
                        "module": "chaosazure.machine.actions",
                        "func": "restart_machines",
                        "secrets": [
                            "azure"
                        ],
                        "config": [
                            "azure"
                        ]
                    }
                }
            ],
            "rollbacks": [],
            "dry": False
        },
        "start": "2020-05-14T19:24:47.983575",
        "status": "completed",
        "deviated": False,
        "steady_states": {
            "before": {
                "steady_state_met": True,
                "probes": [
                    {
                        "activity": {
                            "type": "probe",
                            "name": "service-must-respond",
                            "tolerance": 200,
                            "provider": {
                                "type": "http",
                                "url": "https://www.proofdock.io/"
                            }
                        },
                        "output": {},
                        "status": "succeeded",
                        "start": "2020-05-14T19:24:53.474329",
                        "end": "2020-05-14T19:24:54.860932",
                        "duration": 1.386603,
                        "tolerance_met": True
                    }
                ]
            },
            "after": {
                "steady_state_met": True,
                "probes": [
                    {
                        "activity": {
                            "type": "probe",
                            "name": "service-must-respond",
                            "tolerance": 200,
                            "provider": {
                                "type": "http",
                                "url": "https://www.proofdock.io/"
                            }
                        },
                        "output": {},
                        "status": "succeeded",
                        "start": "2020-05-14T19:25:04.559844",
                        "end": "2020-05-14T19:25:05.346321",
                        "duration": 0.786477,
                        "tolerance_met": True
                    }
                ]
            }
        },
        "run": [
            {
                "activity": {
                    "type": "action",
                    "name": "Restart a random node in the web cluster",
                    "provider": {
                        "type": "python",
                        "module": "chaosazure.machine.actions",
                        "func": "restart_machines",
                        "secrets": [
                            "azure"
                        ],
                        "config": [
                            "azure"
                        ]
                    }
                },
                "output": {
                    "resources": [
                        {
                            "id": "/subscriptions/sub/resourceGroups/rg_web_host/providers/Microsoft.Compute/virtualMachines/test-machine",
                            "sku": None,
                            "name": "test-machine",
                            "type": "microsoft.compute/virtualmachines",
                            "kind": "",
                            "plan": None,
                            "tags": None,
                            "location": "eastus",
                            "resourceGroup": "rg_web_host",
                            "subscriptionId": "sub",
                            "managedBy": "",
                            "identity": None,
                            "zones": None,
                            "tenantId": "ttt",
                            "performed_at": 1589484297
                        }
                    ]
                },
                "status": "succeeded",
                "start": "2020-05-14T19:24:54.881233",
                "end": "2020-05-14T19:24:57.456343",
                "duration": 2.57511
            }
        ],
        "rollbacks": [],
        "end": "2020-05-14T19:25:05.366208",
        "duration": 17.421628952026367
    }
