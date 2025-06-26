pipeline {
    agent any
    stages {
        stage('Prepare') {
            steps {
                // Очищаем рабочую директорию
                deleteDir()
            }
        }

        stage('Clone avtest') {
            steps {
                // Клонируем репозиторий avtest
                git url: 'https://github.com/screemf/avtest.git', branch: 'main'
            }
        }

        stage('Build and Run Django Blog') {
            steps {
                script {
                    // Останавливаем и удаляем старый контейнер
                    sh 'docker stop django-blogapp-container || true'
                    sh 'docker rm django-blogapp-container || true'

                    // Собираем образ
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
                        error "Django Blog application is not available. HTTP status code: ${response}"
                    } else {
                        echo "Django Blog application is available and responding with HTTP 200"
                    }
                }
            }
        }

        stage('Build and Run avtest') {
            steps {
                script {
                    dir('avtest') {
                        // Останавливаем и удаляем старый контейнер avtest
                        sh 'docker stop avtest-container || true'
                        sh 'docker rm avtest-container || true'

                        // Собираем образ avtest
                        docker.build('avtest-app')

                        // Запускаем контейнер avtest без проверки доступности
                        sh '''docker run -d \
                            --name avtest-container \
                            -p 8080:8080 \
                            avtest-app'''

                        echo "avtest application container started (no availability check performed)"
                    }
                }
            }
        }
    }
    post {
        always {
            // Очистка после выполнения
            script {
                sh 'docker stop django-blogapp-container || true'
                sh 'docker rm django-blogapp-container || true'
                sh 'docker stop avtest-container || true'
                sh 'docker rm avtest-container || true'
            }
        }
    }
}