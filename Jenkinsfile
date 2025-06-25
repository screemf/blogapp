pipeline {
    agent any
    stages {
        stage('Build and Run') {
            steps {
                script {
                    // Останавливаем и удаляем старый контейнер
                    sh 'docker stop django-blogapp-container || true'
                    sh 'docker rm django-blogapp-container || true'

                    // Собираем образ (если нужно)
                    docker.build('django-blogapp')

                    // Запускаем контейнер (исправленный вариант)
                    sh '''docker run -d \
                        --name django-blogapp-container \
                        -p 8001:8000 \
                        django-blogapp'''
                }
            }
        }
    }
    post {
        always {
            // Очистка после выполнения
            sh 'docker stop django-blogapp-container || true'
            sh 'docker rm django-blogapp-container || true'
        }
    }
}