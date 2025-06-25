pipeline {
    agent any
    environment {
        DOCKER_REGISTRY = 'docker.io'
        BLOG_IMAGE = "screemf/django_project"
        NETWORK_NAME = 'blog-network'
        BLOG_PORT = '8000'
        LOGIN_URL = "http://127.0.0.1:${BLOG_PORT}/user/login/"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Environment') {
            steps {
                script {
                    sh """
                        # Очистка предыдущих контейнеров
                        docker stop blog-container || true
                        docker rm blog-container || true
                        docker network rm ${NETWORK_NAME} || true

                        # Создание сети
                        docker network create ${NETWORK_NAME}
                    """
                }
            }
        }

        stage('Run Blog') {
            steps {
                script {
                    sh """
                        # Запуск контейнера с блогом
                        docker pull ${BLOG_IMAGE}:latest
                        docker run -d \
                            --name blog-container \
                            --network ${NETWORK_NAME} \
                            -p ${BLOG_PORT}:8000 \
                            ${BLOG_IMAGE}:latest

                        # Ожидание инициализации
                        echo "Ожидание запуска блога (30 секунд)..."
                        sleep 30

                        # Проверка состояния
                        echo "=== Состояние контейнера ==="
                        docker ps -a --filter "name=blog-container"

                        # Проверка логов
                        echo "=== Последние логи ==="
                        docker logs --tail 20 blog-container || echo "Логи недоступны"

                        # Проверка доступности
                        echo "=== Проверка доступности ==="
                        echo "URL: ${LOGIN_URL}"

                        HTTP_STATUS=\$(curl -s -o /dev/null -w "%{http_code}" ${LOGIN_URL} || echo "500")

                        if [ "\$HTTP_STATUS" -eq "200" ]; then
                            echo "Успех: Блог доступен (HTTP 200)"
                        else
                            echo "Ошибка: Блог не доступен (HTTP статус: \$HTTP_STATUS)"
                            docker logs blog-container > blog_failure.log
                            exit 1
                        fi
                    """
                }
            }
        }
    }

    post {
        always {
            script {
                // Сохранение логов и очистка
                sh """
                    docker logs blog-container --tail 200 > blog.log 2>&1 || true
                    docker stop blog-container || true
                    docker rm blog-container || true
                    docker network rm ${NETWORK_NAME} || true
                """
                archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
            }
        }

        success {
            echo "Блог успешно запущен и доступен по адресу: ${LOGIN_URL}"
        }

        failure {
            echo "Ошибка при запуске блога. Проверьте логи для диагностики."
        }
    }
}