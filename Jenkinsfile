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


        stage('Build Docker image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:latest", "--no-cache .")
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yaml up --build test_service'
                    sh 'docker-compose -f docker-compose.yaml run test pytest'
                    sh 'docker-compose -f docker-compose.yaml down'
                }
            }
        }

        stage('Push Docker image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'oran-docker-creds') {
                        dockerImage.push("${env.BRANCH_NAME}-${env.BUILD_NUMBER}")
                        dockerImage.push("latest")
                    }
                }
            }
        }

    }
    post {
        always {
            cleanWs()
        }
    }
}
