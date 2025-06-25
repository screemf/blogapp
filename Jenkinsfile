pipeline {
    agent any
    environment {
        DOCKER_REGISTRY = 'docker.io'
        BLOG_IMAGE = "screemf/django_project"
        TEST_IMAGE = "screemf/my-app"
        NETWORK_NAME = 'blog-network'
        BLOG_PORT = '8005'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm  // Получаем исходный код из репозитория
            }
        }

        stage('Prepare Environment') {
            steps {
                script {
                    sh """
                        docker stop blog-container || true
                        docker rm blog-container || true
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
                            ${BLOG_IMAGE}:latest
                        sleep 15
                        curl -f http://localhost:${BLOG_PORT} || true
                    """
                }
            }
        }

        stage('Run Autotests') {
            steps {
                script {
                    sh """
                        # Копируем тесты в контейнер
                        docker run --rm \
                            --name test-container \
                            --network ${NETWORK_NAME} \
                            -e TEST_URL=http://blog-container:8000 \
                            -v ${WORKSPACE}:/app \
                            ${TEST_IMAGE}:latest \
                            sh -c 'cd /app && \
                                  pip install -r requirements.txt && \
                                  pytest Auth_test.py Users_test.py registr_test.py Post_detail_test.py Post_test.py WS_test.py --alluredir=./allure-results'
                    """
                }
            }
        }

        stage('Allure Report') {
            steps {
                script {
                    // Убедимся, что директория существует
                    sh 'mkdir -p allure-report'

                    // Генерируем отчет Allure
                    sh """
                        docker run --rm \
                            -v ${WORKSPACE}/allure-results:/allure-results \
                            -v ${WORKSPACE}/allure-report:/allure-report \
                            allureapi/allure:2.13.8 \
                            allure generate /allure-results -o /allure-report
                    """

                    // Публикуем отчет
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'allure-report',
                        reportFiles: 'index.html',
                        reportName: 'Allure Report',
                        reportTitles: ''
                    ])
                }
            }
        }
    }

    post {
        always {
            script {
                node {
                    sh "docker logs blog-container --tail 100 > blog.log 2>&1 || true"
                    archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
                    sh "docker stop blog-container || true"
                    sh "docker rm blog-container || true"
                    sh "docker network rm ${NETWORK_NAME} || true"

                    // Сохраняем результаты тестов
                    archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
                }
            }
        }
    }
}