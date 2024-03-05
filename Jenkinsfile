pipeline {
    agent {
        kubernetes {
            label 'ez-joy-friends'
            idleMinutes 5
            yamlFile 'build-pod.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }

 environment {
        GITLAB_CREDS = 'oran-gitlab-cred'
        DOCKER_IMAGE = 'oranhack7/world_of_tanks_project'
        MONGODB_URI = 'mongodb://mongo:27017/world_of_tanks'
        PROJECT_ID = '55413952'
        GITLAB_URL = 'https://gitlab.com'

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
                // Adjusted step to use Docker Pipeline syntax
                script {
                    def customDocker = docker.build("${env.DOCKER_IMAGE}")
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

    stage('Create Merge Request') {
            when {
                not {
                    branch 'main'
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
