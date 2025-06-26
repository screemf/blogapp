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

                    // Запускаем контейнер
                    sh '''docker run -d \
                        --name django-blogapp-container \
                        -p 8000:8000 \
                        django-blogapp'''

                    // Ждем пока контейнер запустится
                    sleep(time: 5, unit: 'SECONDS')

                    // Проверяем доступность приложения
                    def response = sh(script: 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/blog/home/', returnStdout: true).trim()

                    if (response != "200") {
                        error "Application is not available. HTTP status code: ${response}"
                    } else {
                        echo "Application is available and responding with HTTP 200"
                    }
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