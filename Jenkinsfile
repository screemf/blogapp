pipeline {
    agent any
    environment {
        // Настройки Docker Hub
        DOCKER_REGISTRY = 'docker.io'
        DOCKERHUB_CREDS = credentials('dockerhub-creds') // ID ваших credentials в Jenkins

        // Ваши образы из Docker Hub
        BLOG_IMAGE = "${DOCKER_REGISTRY}/screemf/django-blogapp"
        TEST_IMAGE = "${DOCKER_REGISTRY}/screemf/my-app"

        // Сеть и порты
        NETWORK_NAME = 'blog-network'
        BLOG_PORT = '8001' // Порт для блога на хосте
        TEST_PORT = '8002' // Порт для тестов (если нужен)
    }
    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    // Создаем сеть
                    sh "docker network create ${NETWORK_NAME} || true"

                    // Логинимся в Docker Hub
                    sh """
                        echo ${DOCKERHUB_CREDS_PSW} | docker login \
                            -u ${DOCKERHUB_CREDS_USR} \
                            --password-stdin ${DOCKER_REGISTRY}
                    """
                }
            }
        }

        stage('Run Blog App') {
            steps {
                script {
                    // Останавливаем старый контейнер если есть
                    sh "docker stop blog-container || true"
                    sh "docker rm blog-container || true"

                    // Запускаем блог
                    sh """
                        docker run -d \
                            --name blog-container \
                            --network ${NETWORK_NAME} \
                            -p ${BLOG_PORT}:8000 \
                            ${BLOG_IMAGE}:latest
                    """

                    // Ждем инициализации (адаптируйте время под ваш проект)
                    sh 'sleep 20 && curl -f http://localhost:${BLOG_PORT}/healthcheck || true'
                }
            }
        }

        stage('Run Autotests') {
            steps {
                script {
                    // Запускаем тесты с подключением к блогу через сеть
                    sh """
                        docker run --rm \
                            --name test-container \
                            --network ${NETWORK_NAME} \
                            -e TEST_URL=http://blog-container:8000 \
                            ${TEST_IMAGE}:latest
                    """
                }
            }
        }
    }
    post {
        always {
            // Сохраняем логи
            sh "docker logs blog-container --tail 100 > blog.log 2>&1 || true"
            archiveArtifacts artifacts: 'blog.log', allowEmptyArchive: true

            // Очистка
            sh "docker stop blog-container || true"
            sh "docker rm blog-container || true"
            sh "docker network rm ${NETWORK_NAME} || true"
            sh 'docker logout'
        }
    }
}