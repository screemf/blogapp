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
                checkout scm
                // Проверка структуры проекта
                sh '''
                    echo "Структура проекта:"
                    ls -la
                    echo "Дерево каталогов:"
                    find . -maxdepth 2 -type d | sed -e "s|[^-][^/]*/|  |g"
                '''
            }
        }

        stage('Fix Requirements') {
            steps {
                script {
                    // Автоматическое исправление requirements.txt
                    sh '''
                        sed -i 's/cffi==1.15./cffi==1.15.0/' requirements.txt
                        echo "Проверка исправленного requirements.txt:"
                        cat requirements.txt | grep cffi
                    '''
                }
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
                            -v ${WORKSPACE}/blogapp:/app \
                            ${BLOG_IMAGE}:latest
                        sleep 30
                        echo "Проверка работы блога:"
                        docker logs blog-container --tail 20
                        curl --retry 5 --retry-delay 5 --retry-connrefused -f http://localhost:${BLOG_PORT} || echo "Проверка блога не удалась"
                    """
                }
            }
        }

        stage('Run Autotests') {
            steps {
                script {
                    sh """
                        docker run --rm \
                            --name test-container \
                            --network ${NETWORK_NAME} \
                            -e TEST_URL=http://blog-container:8000 \
                            -v ${WORKSPACE}:/app \
                            -w /app \
                            ${TEST_IMAGE}:latest \
                            sh -c 'pip install --upgrade pip && \
                                  pip install -r requirements.txt && \
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
                    archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true

                    sh "docker stop blog-container || true"
                    sh "docker rm blog-container || true"
                    sh "docker network rm ${NETWORK_NAME} || true"
                }
            }
        }
    }
}