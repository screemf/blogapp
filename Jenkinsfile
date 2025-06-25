pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                    docker.build("django-blogapp")
                }
            }
        }
        stage('Run Django') {
            steps {
                script {
                    // Останавливаем и удаляем старый контейнер, если существует
                    sh 'docker stop django-blogapp-container || true'
                    sh 'docker rm django-blogapp-container || true'

                    // Запускаем новый контейнер
                    sh '''
                        docker run -d \
                            --name django-blogapp-container \
                            --network django-network \
                            -p 8000:8000 \  # Используем другой порт
                            django-blogapp
                    '''
                }
            }
        }
    }
    post {
        always {
            sh 'docker stop django-blogapp-container || true'
            sh 'docker rm django-blogapp-container || true'
            sh 'docker network rm django-network || true'
        }
    }
}