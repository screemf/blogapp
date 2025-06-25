pipeline {
    agent any
    environment {
        DOCKER_REGISTRY = 'docker.io'
        BLOG_IMAGE = "screemf/django_project"  // Используем существующий репозиторий
        TEST_IMAGE = "screemf/my-app"          // Используем существующий репозиторий
        NETWORK_NAME = 'blog-network'
        BLOG_PORT = '8000'
        TEST_PORT = '8001'
    }
    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    sh "docker network create ${NETWORK_NAME} || true"
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
                        docker stop blog-container || true
                        docker rm blog-container || true
                        docker pull ${BLOG_IMAGE}:latest
                        docker run -d \
                            --name blog-container \
                            --network ${NETWORK_NAME} \
                            -p ${BLOG_PORT}:8000 \
                            ${BLOG_IMAGE}:latest
                        sleep 20
                        curl -f http://localhost:${BLOG_PORT} || true
                    """
                }
            }
        }

        stage('Run Autotests') {
            steps {
                script {
                    sh """
                        docker stop test-container || true
                        docker rm test-container || true
                        docker pull ${TEST_IMAGE}:latest
                        docker run --rm \
                            --name test-container \
                            --network ${NETWORK_NAME} \
                            -p ${TEST_PORT}:8000 \
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