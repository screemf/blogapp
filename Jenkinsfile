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

        stage('Cleanup Port') {
            steps {
                script {
                    sh """
                        # Остановка контейнеров использующих порт 8000
                        docker ps --format '{{.ID}} {{.Ports}}' | grep ':8000' | awk '{print \$1}' | xargs -r docker stop || true

                        # Освобождение порта 8000
                        echo "Очистка порта 8000..."
                        sudo lsof -i :8000 | awk 'NR!=1 {print \$2}' | xargs -r sudo kill -9 || true
                        sudo netstat -tulnp | grep ':8000' | awk '{print \$7}' | cut -d'/' -f1 | xargs -r sudo kill -9 || true
                    """
                }
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

                        # Проверка состояния порта
                        echo "=== Проверка порта 8000 ==="
                        sudo lsof -i :8000 || echo "Порт 8000 свободен"
                        docker port blog-container

                        # Проверка доступности
                        echo "=== Проверка доступности ==="
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
                sh """
                    docker logs blog-container --tail 200 > blog.log 2>&1 || true
                    docker stop blog-container || true
                    docker rm blog-container || true
                    docker network rm ${NETWORK_NAME} || true
                """
                archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
            }
        }
    }
}