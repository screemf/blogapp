pipeline {
    agent any
    environment {
        DOCKER_REGISTRY = 'docker.io'
        BLOG_IMAGE = "screemf/django_project"  # Образ с Django-приложением
        TEST_IMAGE = "screemf/my-app"         # Образ с тестами
        NETWORK_NAME = 'blog-network'
        BLOG_PORT = '8005'
        BLOG_URL = "http://blog-container:8000/blog/home"  # Полный URL для проверки
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Fix Requirements') {
            steps {
                script {
                    sh '''
                        # Исправляем requirements.txt
                        sed -i 's/cffi==1.15./cffi==1.15.0/' requirements.txt
                        echo "Проверка исправленного requirements.txt:"
                        grep cffi requirements.txt
                    '''
                }
            }
        }

        stage('Prepare Environment') {
            steps {
                script {
                    sh """
                        docker stop blog-container test-container || true
                        docker rm blog-container test-container || true
                        docker network rm ${NETWORK_NAME} || true
                        docker network create ${NETWORK_NAME}
                    """
                }
            }
        }

        stage('Run Blog App') {
            steps {
                script {
                    sh """
                        docker pull ${BLOG_IMAGE}:latest
                        docker run -d \
                            --name blog-container \
                            --network ${NETWORK_NAME} \
                            -p ${BLOG_PORT}:8000 \
                            -v ${WORKSPACE}/blogapp:/app \
                            ${BLOG_IMAGE}:latest

                        echo "Ожидание запуска блога..."
                        sleep 30

                        # Проверка логов блога
                        echo "Логи блога:"
                        docker logs blog-container --tail 20

                        # Проверка доступности
                        echo "Проверка доступности блога по URL: ${BLOG_URL}"
                        docker exec blog-container curl -sSf ${BLOG_URL} || echo "Блог не доступен"

                        # Альтернативная проверка с хоста
                        curl --retry 5 --retry-delay 5 --retry-connrefused \
                             -f "http://localhost:${BLOG_PORT}/blog/home" || echo "Внешняя проверка не удалась"
                    """
                }
            }
        }

        stage('Run Autotests') {
            steps {
                script {
                    sh """
                        echo "Запуск тестов из образа ${TEST_IMAGE}"
                        docker run --rm \
                            --name test-container \
                            --network ${NETWORK_NAME} \
                            -e TEST_URL=${BLOG_URL} \
                            -v ${WORKSPACE}:/app \
                            -w /app \
                            ${TEST_IMAGE}:latest \
                            sh -c 'pip install --upgrade pip && \
                                  pip install -r requirements.txt && \
                                  ls -la && \
                                  pytest Auth_test.py Users_test.py registr_test.py Post_detail_test.py Post_test.py WS_test.py \
                                  --alluredir=./allure-results'
                    """
                }
            }
        }

        stage('Allure Report') {
            steps {
                script {
                    sh 'mkdir -p allure-report'
                    sh """
                        docker run --rm \
                            -v ${WORKSPACE}/allure-results:/allure-results \
                            -v ${WORKSPACE}/allure-report:/allure-report \
                            allureapi/allure:2.13.8 \
                            allure generate /allure-results -o /allure-report --clean
                    """
                    publishHTML(target: [
                        reportDir: 'allure-report',
                        reportFiles: 'index.html',
                        reportName: 'Allure Report'
                    ])
                }
            }
        }
    }

    post {
        always {
            script {
                node {
                    sh "docker logs blog-container --tail 200 > blog.log 2>&1 || true"
                    sh "docker logs test-container --tail 200 > tests.log 2>&1 || true"
                    archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true

                    sh "docker stop blog-container test-container || true"
                    sh "docker rm blog-container test-container || true"
                    sh "docker network rm ${NETWORK_NAME} || true"
                }
            }
        }
    }
}