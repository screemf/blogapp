pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "django-app"
        DOCKER_TAG = "latest"
        APP_PORT = "8000"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],  // Указываем ветку main вместо master
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/screemf/blogapp.git',
                        credentialsId: '701cac66-35b9-4c38-a20c-3ab0f09edd2e'  // Используйте ваш credentialsId
                    ]]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_TAG}")
                }
            }
        }

        stage('Run App') {
            steps {
                script {
                    sh "docker stop django-app || true"
                    sh "docker rm django-app || true"
                    sh """
                        docker run -d \
                            --name django-app \
                            -p ${APP_PORT}:8000 \
                            ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Логи контейнера:"
            sh "docker logs django-app --tail 50 || true"
        }
        failure {
            emailext body: 'Сборка провалена: ${BUILD_URL}',
                      subject: 'FAILED: ${JOB_NAME}',
                      to: 'dev-team@example.com'
        }
    }
}