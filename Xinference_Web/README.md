# Vulnerability Name
Unauthorized Arbitrary Operations in Xinference Web Service

## Vendor
Xinference belongs to Hangzhou Future Speed Technology Co., Ltd.

## Introduction to Xinference
Xorbits Inference (Xinference) is a powerful and comprehensive distributed inference framework. It can be used for the inference of various models, such as large language models (LLMs), speech recognition models, and multimodal models. With Xorbits Inference, you can easily deploy your own models or built - in cutting - edge open - source models with one click.

- [GitHub](https://github.com/xorbitsai/inference)
- [Official Documentation](https://inference.readthedocs.io/zh) - cn/latest/index.html

## Version
All current versions

## Risk and Hazard
When Xinference is deployed in the way of "xinference - local --host 0.0.0.0 --port 9997" (this port can be customized) with the default configuration, attackers can access the Web GUI interface without authorization and perform arbitrary operations such as viewing, downloading, deploying, running, and deleting models through interface operations.

## Vulnerability Reproduction
### 1. Deploy Xinference
```bash
pip install "xinference[all]"
```

2.Start Xinference
bash
xinference - local --host 0.0.0.0 --port 9997

3.Access the Xinference interface
A.Pull and deploy models. On the Launch Model interface, the attacker can click a model and complete a simple configuration to pull any model from the Magic Tower community and complete the installation.
![image](https://github.com/user-attachments/assets/d5d8deed-9cf0-445d-80c8-f8fb9be0755d)

B.Delete the model. On the "Running models" interface, attackers can choose to delete the running models.
![image](https://github.com/user-attachments/assets/dda2b80b-798a-48f5-a3f3-45bbfffa76bb)


C.Modify the model configuration. On the "Register Model" interface, attackers can modify the relevant configurations or create new ones.
![image](https://github.com/user-attachments/assets/3d859b33-a477-4eb6-9c81-d1fc1df29be6)

D.View sensitive cluster information. Attackers can view cluster resource information in "Cluster Information".
![image](https://github.com/user-attachments/assets/e76a3850-f28f-4e7f-86ac-c026c702d3da)



4.Run the poc.py script of Python and then enter the relevant IP address and port.
