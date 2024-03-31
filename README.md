# World of Tanks

## Overview

Welcome to the *World of Tanks* project! This application is a comprehensive database of tanks from various countries, types, and production years. It presents a user-friendly website, powered by Python, that allows users to explore the vast world of armored warfare vehicles throughout history.

## Features

- **Comprehensive Database**: A rich collection of tanks sorted by ascending years, with detailed information on each model.
- **Interactive Country Flags**: Users can sort tanks based on the country by clicking on flags, making it easy to find tanks from specific nations.
- **Python-Powered Backend**: Utilizes Python for backend logic, serving a dynamic HTML front-end.
- **CI/CD Integration**: Continuous Integration (CI) with Jenkins and Continuous Deployment (CD) with ArgoCD for streamlined development and deployment.
- **Database**: Utilizes MongoDB for efficient data storage and retrieval.
- **Monitoring and Alerts**: Implements Prometheus and Grafana for real-time monitoring and alerting to maintain system health and performance.
- **Project Management**: Utilizes a Kanban board on Jira for clear and organized project tracking.


## Getting started

To get a local copy up and running, follow these simple steps(Assuming you're using Windows OS):

### Prerequisites

- Python (version 3.X)
- Docker Desktop
- Kubernetes cluster 

### Installation
1. **Clone the repo**:
```
git clone https://gitlab.com/sela-tracks/1101/oran/world-of-tanks.git
cd world-of-tanks
```

2. **Install Python dependencies**:
```
pip install flask pymongo requests pytest
```

3. **Run Docker Desktop and make sure your cluster is up and runnig**.

4. **Install Helm**:
```
choco install kubernetes-helm
```

5. **Install Jenkins for the CI**:
```
helm repo add jenkinsci https://charts.jenkins.io/
```
```
helm install my-jenkins jenkinsci/jenkins --version 5.1.3
```

6. **Apply these predefined yaml files which using ArgoCD for the CD**:
```
kubectl apply -f mongodb.yaml
```
```
kubectl apply -f application.yaml
```
7. **Install Prometheus(under observation namespace) for monitoring and implment the predifined alerts**:
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```
```
helm repo update
```
```
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack --version v0.72.0 -n observation
```
```
helm upgrade kube-prometheus-stack prometheus-community/kube-prometheus-stack -f alerts.yaml -n observation
```
8. **Install Grafana**:
```
helm repo add grafana https://grafana.github.io/helm-charts
```
```
helm install my-grafana grafana/grafana --version 7.3.7
```

## Testing 

The application includes a suite of tests to verify the full functionality of the website, database, and its features.
To run the tests, ensure you have `pytest` installed and execute:
```
pytest
```

## Usage
Navigate to the hosted URL or, if running locally, to http://localhost:5000 in your browser to explore the tank database. Click on the flag icons to filter tanks by country or use the search functionality to find specific models.

## Support
For any recommendation, request or a question feel free to email me oranhack7@gmail.com.

## Monitoring
To monitor application performance and receive alerts, refer to the Prometheus and Grafana documentation for setup and configuration instructions.

## Acknowledgments
This project utilizes open-source tools such as Python, MongoDB, Jenkins, ArgoCD, Prometheus, and Grafana.

## License
This project is open-source and made by Oran Hackmon for the Sela College Final project of DevOps Enginnering Course.
