pipeline {
    agent any

    environment {
        // Define Docker image tag
        DOCKER_IMAGE = 'oranhack7/world_of_tanks_project:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                // Explicitly check out from GitLab repository on dev branch
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: 'origin/dev']],
                    userRemoteConfigs: [[
                        url: 'https://gitlab.com/sela-tracks/1101/oran/world-of-tanks.git',
                        credentialsId: 'oran-gitlab-creds'
                    ]]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build Docker image
                script {
                    docker.build(env.DOCKER_IMAGE)
                }
            }
        }

        stage('Run Tests') {
            steps {
                // Run tests using the Docker image
                script {
                    docker.image(env.DOCKER_IMAGE).inside {
                        sh 'python -m unittest discover -s tests'
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Login to Docker Hub
                    docker.withRegistry('https://registry.hub.docker.com', 'oran-docker-creds') {
                        // Push the Docker image
                        docker.push(env.DOCKER_IMAGE)
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up Docker images to avoid filling up the Jenkins agent
            script {
                docker.rmi(env.DOCKER_IMAGE)
            }
        }
    }
}
