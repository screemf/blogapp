pipeline {
    agent any
    environment {
        DOCKER_REGISTRY = 'docker.io'
        BLOG_IMAGE = "screemf/django_project"
        TEST_IMAGE = "screemf/my-app"
        NETWORK_NAME = 'blog-network'
        // Динамическое определение свободного порта
        BLOG_PORT = sh(script: "comm -23 <(seq 8000 8100 | sort) <(ss -tan | awk '{print $4}' | cut -d':' -f2 | sort -u) | head -n 1", returnStdout: true).trim()
    }
    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    // Очистка предыдущих контейнеров
                    sh '''
                        docker stop blog-container test-container || true
                        docker rm blog-container test-container || true
                        docker network rm ${NETWORK_NAME} || true
                        docker network create ${NETWORK_NAME}
                        echo "Выбран порт для блога: ${BLOG_PORT}"
                    '''
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login $DOCKER_REGISTRY \
                            -u "$DOCKER_USER" \
                            --password-stdin
                    '''
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
                        echo "Блог доступен на порту: ${BLOG_PORT}"
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
                        docker pull ${TEST_IMAGE}:latest
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
            sh "docker logs blog-container --tail 100 > blog.log 2>&1 || true"
            sh "docker logs test-container --tail 100 > tests.log 2>&1 || true"
            archiveArtifacts artifacts: '*.log', allowEmptyArchive: true

            sh "docker stop blog-container test-container || true"
            sh "docker rm blog-container test-container || true"
            sh "docker network rm ${NETWORK_NAME} || true"
            sh 'docker logout'
        }
    }
}