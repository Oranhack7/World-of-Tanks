# World of Tanks

## Overview

Welcome to the *World of Tanks* project! This application is a comprehensive database of tanks from various countries, types, and production years. It presents a user-friendly HTML website, powered by Python, that allows users to explore the vast world of armored warfare vehicles throughout history.

## Features

- **Comprehensive Database**: A rich collection of tanks sorted by ascending years, with detailed information on each model.
- **Interactive Country Flags**: Users can sort tanks based on the country by clicking on flags, making it easy to find tanks from specific nations.
- **Python-Powered Backend**: Utilizes Python for backend logic, serving a dynamic HTML front-end.
- **CI/CD Integration**: Continuous Integration (CI) with Jenkins and Continuous Deployment (CD) with ArgoCD for streamlined development and deployment.
- **Database**: Utilizes MongoDB for efficient data storage and retrieval.
- **Monitoring and Alerts**: Implements Prometheus and Grafana for real-time monitoring and alerting to maintain system health and performance.
- **Project Management**: Utilizes a Kanban board on Jira for clear and organized project tracking.


## Getting started

To get a local copy up and running, follow these simple steps:

### Prerequisites

- Python (version 3.x)
- Flask
- PyMongo
- An active MongoDB instance
- Kubernetes cluster for deployment using the Helm chart

### Installation
- Clone the repo:
```
git close https://gitlab.com/sela-tracks/1101/oran/world-of-tanks.git
cd world-of-tanks
```

1. Install Python dependencies:
   ```
   pip install flask pymongo requests pytest
   ```

2. Set up your MongoDB database:
- Follow MongoDB's documentation to install and set up your database.
- `MONGODB_URI`: URI for connecting to your MongoDB instance.

3. Configure your CI/CD pipelines:
- Jenkins and ArgoCD setup guides can be found in their respective documentation.

4. Run the application:
- Navigate to the application directory and run the Flask application:
```
python app.py
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
For any recommendation, request or question feel free to email me oranhack7@gmail.com.

## Monitoring
To monitor application performance and receive alerts, refer to the Prometheus and Grafana documentation for setup and configuration instructions.

## Acknowledgments
This project utilizes open-source tools such as Python, MongoDB, Jenkins, ArgoCD, Prometheus, and Grafana.

## License
This project is open-source and made by Oran Hackmon for the Sela College Final project of DevOps Enginnering Course.
