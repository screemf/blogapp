pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "django-app"  // Имя образа
        DOCKER_TAG = "latest"             // Тег образа
        APP_PORT = "8000"                 // Порт приложения
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com//screemf/blogapp.git'  // Укажите ваш репозиторий
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Собираем Docker-образ из Dockerfile
                    docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_TAG}")
                }
            }
        }

        stage('Run Migrations') {
            steps {
                script {
                    // Запускаем миграции внутри контейнера
                    docker.image("${DOCKER_IMAGE_NAME}:${DOCKER_TAG}").inside {
                        sh 'python manage.py migrate --noinput'
                    }
                }
            }
        }

        stage('Run App') {
            steps {
                script {
                    // Останавливаем старый контейнер (если есть)
                    sh "docker stop django-app || true"
                    sh "docker rm django-app || true"

                    // Запускаем новый контейнер
                    sh """
                        docker run -d \
                            --name django-app \
                            -p ${APP_PORT}:8000 \
                            ${DOCKER_IMAGE_NAME}:${DOCKER_TAG}
                    """
                }
            }
        }
    }

    post {
        always {
            // Логирование (опционально)
            echo "Приложение запущено на порту ${APP_PORT}"
        }
        failure {
            // Уведомление о неудаче
           echo "Приложение не запущено на порту ${APP_PORT}"
        }
    }
}