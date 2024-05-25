# Airbus Aerothon 6.0 - Optimal Route Planning & Risk Mitigation

## Introduction

Enhancing flight navigation mechanisms is a critical priority for Airbus, aiming to improve operational efficiency and safety. We propose the design and implementation of an advanced software solution that identifies optimal flight routes and mitigates risks associated with GPS unavailability, adverse weather conditions, and system failures. This innovative AI-powered mobile app, integrated with blockchain technology for robust data security, offers real-time updates and alternative route suggestions. By leveraging artificial intelligence, machine learning, and data analytics, the solution minimizes human errors, ensures safety in adverse conditions, and detects system anomalies early. Optimized routes and real-time risk assessments not only enhance efficiency and reduce costs but also lower the carbon footprint, improve regulatory compliance, and increase reporting accuracy. Additionally, a chatbot feature provides intuitive assistance to pilots and control centers, further improving operational efficiency and safety.

## Project Components

This Project is divided into 3 parts:

1. **Android**
2. **Machine Learning**
3. **Blockchain**
4. 

### Login and Signup Screens:

<img src="https://github.com/Smarshal21/Airbus_Aerothon/assets/96579549/ecfbc084-f344-40c2-bdc9-0aae522e9e0a" width="240" height="510" /> 
<img src="https://github.com/Smarshal21/Airbus_Aerothon/assets/96579549/291d8077-b063-4be3-955a-0b29bcbe0637" width="240" height="510" />

### Home Screens:
<img src="https://github.com/LCB2021029-Badri/GREYLIFE_CANARA/assets/96579549/9718259b-bcb4-484b-b125-df413c8b1b66" width="240" height="510" /> 


### Data Collection & Status Screens:

<img src="https://github.com/LCB2021029-Badri/GREYLIFE_CANARA/assets/96579549/5e6d9c85-c307-4d49-bdb6-1de1dae2a136" width="240" height="510" /> 

<img src="https://github.com/LCB2021029-Badri/GREYLIFE_CANARA/assets/96579549/0083e643-b098-400a-bc55-a3293bf2454a" width="240" height="510" /> 


### AI ChatBot / Risk Mitigation Screen:
<img src="https://github.com/LCB2021029-Badri/GREYLIFE_CANARA/assets/96579549/99e5001b-9027-448d-967f-6a1f53ff9a96" width="240" height="510" /> 

## Machine Learning
### Overview
This project showcases the deployment of machine learning models using PCA (Principal Component Analysis) and XGBoost in Python. The models are trained and saved using pickle, then integrated into a Flask API. The Flask API is deployed on Railway, enabling users to send data from their mobile devices and receive predictions in real-time.
#### PCA (Principal Component Analysis)
Reduces the dimensionality of data, which can lead to faster training and improved model efficiency.
Helps in identifying important patterns and reducing noise in the data
It Reduces the input size from 11 to 3 and then process the result 
#### XGBoost
Provides high predictive accuracy and often outperforms other machine learning algorithms.
Allows for feature selection and can handle both numerical and categorical data
#### Ensemble Learning
Can lead to improved model performance, especially when the individual models have complementary strengths and weaknesses. Provides more robust predictions and is less sensitive to outliers or noise in the data.

### Workflow

<img src="https://github.com/Smarshal21/GREYLIFE_CANARA/assets/99678760/186e90d2-8e2e-4885-b72d-76308e8cf12b" width="700" height="300" /> 

### Sample Input and Output
<img src="https://github.com/Smarshal21/GREYLIFE_CANARA/assets/99678760/04403898-f017-4204-a711-8576a999cd91" width="1000" height="500" /> 

## BlockChain
### Overview
This project focuses on the deployment of a Polygon Edge Chain on Amazon Web Services (AWS) using the Kaleido platform. The Polygon Edge Chain provides high-performance, low-latency infrastructure for blockchain applications. By successfully running a Polygon Edge Chain, this project aims to facilitate the development of efficient and scalable decentralized applications
### Consortium blockchain architecture
#### Node
Each node stores a copy of the blockchain and participates in the consensus process to validate transactions and add new blocks to the chain. There are two nodes running on polygon blockchain
#### Ledger
The ledger is the decentralized database that stores all of the transactions that occur on the blockchain
#### Smart Contracts
Smart contracts are self-executing contracts.These are used blockchain consortium architecture to automate the process of executing transactions on the blockchain. Kaleido's Smart Contract Management component simplifies Ethereum transaction submission and application development by providing clean RESTful interfaces for interaction with your smart contract methods.
##### Smart Contract WorkFlow
<img width="1025" alt="Screenshot 2023-11-16 at 2 42 25 AM" src="https://github.com/Smarshal21/GREYLIFE_CANARA/assets/99678760/aedf1e91-5731-47a9-9206-b5ec68a8633d">

#### Governance
Consortium blockchain governance is member-defined and adaptable, comprising rules and decision-making mechanisms tailored to specific use cases and goals.
Access to a private blockchain network is restricted to authorized parties only, and the network is not open to the public.
Private blockchains are preferred in enterprise use cases, such as supply chain management, to maintain greater network control.
#### Transaction Details


<img src="https://github.com/Smarshal21/GREYLIFE_CANARA/assets/99678760/795fc8ed-f16a-418a-8b90-aed448b0086d" width="500" height="250" /> 
<img src="https://github.com/Smarshal21/GREYLIFE_CANARA/assets/99678760/63e3c1fa-7def-44df-8042-0644c1d4831b" width="500" height="250" /> 
<img src="https://github.com/Smarshal21/GREYLIFE_CANARA/assets/99678760/7745bf72-2e5f-4b42-8704-5e606e2c2efb" width="550" height="300"/> 

## Features
- Authentication - Email-Password
- Dashboard
- Status Page (Application Status)
- Page for Uploading Documents and Data
- ML model Processed Output
- Secure Storage of data in Private Polygon BlockChain Deployed on Kaleido

## TECH STACK
- Kotlin
- XML
- Firebase
- Python
- Sklearn
- Flask
- Railway
- Solidity
- Kaleido
- Polygon-Edge
- JavaScript
## Meet The Team
- Badri Akkala |[Github](https://github.com/LCB2021029-Badri)
- KSN Samanwith |[Github](https://github.com/Smarshal21)


