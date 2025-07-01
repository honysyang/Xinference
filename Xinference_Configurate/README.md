# Vulnerability Name
Xinference has an unauthorized access vulnerability 

## Manufacturer
Xinference belongs to Hangzhou Future Speed Technology Co., Ltd.

## Introduction to Xinference
Xorbits Inference (Xinference) is an open-source platform designed to simplify the operation and integration of various AI models. With Xinference, you can use any open-source LLMs (Large Language Models), embedding models, and multimodal models to perform inference in cloud or local environments, and create powerful AI applications.

- [GitHub](https://github.com/xorbitsai/inference)
- [Official Documentation](https://inference.readthedocs.io/zh-cn/latest/index.html)

## Version
All versions of the Xinference open-source framework (when access authentication is not set)

## Vulnerability Description
Xinference does not set up authentication and access control functions by default. When Xinference starts a local service and sets the host to 0.0.0.0, attackers can remotely invoke Xinference's API interfaces and access the Web page, performing malicious operations including but not limited to stealing sensitive model assets, abusing model computing resources, maliciously deleting models, and causing denial-of-service attacks.

Xinference without authentication and access control functions and exposed to the public Internet is vulnerable to this issue.

## Vulnerability Code Analysis
### 1. Local Deployment and Enablement of Xinference
```bash
pip install "xinference[all]"
```
2.Command to Run Xinference Locally Under Default Configuration
inference-local --host 0.0.0.0 --port 9997

3.For Xinference Exposed to Public Network
Any user can access the Xinference web interface and FastAPI services.
Web access route: /ui/#/launch_model/llm
![image](https://github.com/user-attachments/assets/8a1e0475-d571-49d4-9692-31fc109a3386)




The routing address for accessing FastAPI: /docs

![image](https://github.com/user-attachments/assets/27a34753-8af4-4ebd-99a4-3052be9abd21)


It should be noted that under the default configuration of Xinference, any user can access the web page functions and FastAPI interfaces to pull, view, delete, tamper with models, and perform other operations.

## Source Code Analysis
The version of the Xinference source code downloaded in this example is 0.28.
![image](https://github.com/user-attachments/assets/acce7184-e980-42a0-8bbf-c8874f9567bd)


Entering the xinference/api/restful_api.py source code file, one can observe the relevant routes and interfaces of FastAPI.

![image](https://github.com/user-attachments/assets/3d79cc75-ddbb-48d7-b0a2-355d77859dde)

By analyzing the source code, it can be seen that: except for routes such as /v1/models/prompts, /v1/models/vllm-supported, and /v1/cluster/info, other routes all have identity dependencies for permission verification.

![image](https://github.com/user-attachments/assets/d92b2eee-f539-4766-8858-b186112eb644)


Analyzing the identity dependencies of route permission verification again, the source code is as follows.
Here is the interpretation of the source code: To execute the /v1/models/{model_uid} route, it is necessary to pass through dependencies. In dependencies:
If the value of self.is_authenticated() is True (i.e., when system authentication is enabled), a permission check dependency is added to the API route, requiring that users accessing the route must have the models:stop permission.
If system authentication is not enabled, no permission check is performed.

![image](https://github.com/user-attachments/assets/5b463a54-3524-40bf-aa47-16913bc616fb)

Continuing to trace the self.is_authenticated() method, the code is as follows:
It is found that the value of self.is_authenticated() is related to self._auth_service.config. If self._auth_service.config is empty, it returns False.
Through self._auth_service, the AuthService(auth_config_file) method can be traced.
![image](https://github.com/user-attachments/assets/46a613ca-e6ad-4b76-8254-7e55ceab7b9c)


The AuthService method is located in xinference/api/oauth2, and the relevant source code is as follows:
![image](https://github.com/user-attachments/assets/da3296c1-8607-48cf-9ec1-0ad0256d1e70)


Through the above source code analysis, we can further draw the following conclusions:
The value of _auth_service.config is the value of self._config in the AuthService class, and the value of self._config is returned by self.init_auth_config().
The value returned by self.init_auth_config() is determined by auth_config_file.
Key point: If auth_config_file is empty, the value returned by self.init_auth_config() is also empty.

What is the value of auth_config_file in the RESTful API route? Further inspection shows that it is empty by default.

![image](https://github.com/user-attachments/assets/fa6e5f8a-fe7a-469f-a402-091b782feeaf)


Therefore, the following conclusions can be drawn:

By default, the auth_config_file in Xinference is empty, resulting in the default absence of permission settings.

Under the default configuration of Xinference, attackers can access any FastAPI route without authorization, enabling operations such as model invocation and model deletion.


## Vulnerability Reproduction
1.Local Deployment and Enablement of Xinference
pip install "xinference[all]"

2.Command to Run Xinference Locally Under Default Configuration
inference-local --host 0.0.0.0 --port 9997

Current IP: 10.1.2.100

![image](https://github.com/user-attachments/assets/45f0ef87-bdea-4803-bc87-e8aad45effbf)


3.Visit http://10.1.2.100:13002/docs#, or use API interface calling tools to implement the following steps.
![image](https://github.com/user-attachments/assets/2e399f5d-eff4-4ad7-beea-1602b3ace3de)

4.View the current model list

![image](https://github.com/user-attachments/assets/fb9e4cbe-1588-4620-a582-ea7a8b9a045a)
![image](https://github.com/user-attachments/assets/c8d787a4-f942-4a7c-a7a7-f6939b8b8530)


5.Access model-related descriptions
![image](https://github.com/user-attachments/assets/910fbb97-2d57-4f45-9b4d-0d04828834c8)

![image](https://github.com/user-attachments/assets/3d6c9494-4eed-4d93-b4fa-3f81cf320f03)

6.Delete the specified model

![image](https://github.com/user-attachments/assets/fb818367-f19c-442a-a043-f9744bbb3337)
![image](https://github.com/user-attachments/assets/4b2bbb15-8394-4a7b-ba60-8fffa60bddee)


Further verification of the model interface confirms that the model has indeed been deleted.

## Asset Collection
Through the "Xinference" command, it was found that there are no fewer than 3,795 assets exposed to the public network, and most of them are accessible.
![image](https://github.com/user-attachments/assets/205c7dc4-04f7-4431-ac2b-8efcbee195f6)


## Vulnerability Fix Suggestions

1.It is necessary to avoid exposing Xinference to the public network.
2.Modify the value of the default configuration auth_config_file to prevent it from being empty; or set other permission control methods.
