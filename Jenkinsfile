pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "django-app"
        DOCKER_TAG = "latest"
        APP_PORT = "8000"
        APP_URL = "http://localhost:${APP_PORT}/blog/home"  // Добавляем целевой эндпоинт
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/screemf/blogapp.git',
                        credentialsId: '701cac66-35b9-4c38-a20c-3ab0f09edd2e'
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

        // Новый этап: проверка доступности /blog/home
        stage('Check Endpoint') {
            steps {
                script {
                    timeout(time: 2, unit: 'MINUTES') {
                        waitUntil {
                            try {
                                // Проверяем доступность эндпоинта через curl
                                sh """
                                    curl -f -s -o /dev/null -w '%{http_code}' ${APP_URL} | grep -q 200
                                """
                                echo "Эндпоинт ${APP_URL} доступен!"
                                return true
                            } catch (Exception e) {
                                echo "Эндпоинт ${APP_URL} ещё не готов. Повторная попытка..."
                                return false
                            }
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Финальный статус:"
            sh "docker logs django-app --tail 50 || true"
        }
        failure {
            emailext body: """
                Сборка провалена: ${BUILD_URL}
                Логи контейнера:
                ${sh(script: "docker logs django-app --tail 100 2>&1 || true", returnStdout: true)}
            """,
            subject: "FAILED: ${JOB_NAME}",
            to: 'dev-team@example.com'
        }
    }
}