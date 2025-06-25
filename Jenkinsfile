pipeline {
    agent any
    environment {
        DOCKER_REGISTRY = 'docker.io'
        BLOG_IMAGE = "screemf/django-blogapp"
        TEST_IMAGE = "screemf/my-app"
        NETWORK_NAME = 'blog-network'
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
                            -p 8000:8000 \
                            ${BLOG_IMAGE}:latest
                        sleep 20
                        curl -f http://localhost:8000 || true
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
            archiveArtifacts artifacts: 'blog.log', allowEmptyArchive: true

            sh "docker stop blog-container || true"
            sh "docker rm blog-container || true"
            sh "docker network rm ${NETWORK_NAME} || true"
            sh 'docker logout'
        }
    }
}