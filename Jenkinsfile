pipeline {
    agent any

    environment {
        // Настройки для blogapp (Django)
        DJANGO_IMAGE = "django-blogapp"
        DJANGO_CONTAINER = "django-blogapp-container"
        DJANGO_PORT = "8000"
        DJANGO_URL = "http://${DJANGO_CONTAINER}:${DJANGO_PORT}"  // Для доступа из сети контейнеров

        // Настройки для avtest (автотесты)
        AVTEST_IMAGE = "django-avtest"
        AVTEST_CONTAINER = "django-avtest-container"
    }

    stages {
        // 1. Забираем оба репозитория
        stage('Checkout') {
            steps {
                dir('blogapp') {
                    git url: 'https://github.com/screemf/blogapp.git', branch: 'main'
                }
                dir('avtest') {
                    git url: 'https://github.com/screemf/avtest.git', branch: 'main'
                }
            }
        }

        // 2. Собираем оба Docker-образа
        stage('Build Images') {
            steps {
                script {
                    // Собираем Django-приложение
                    docker.build("${DJANGO_IMAGE}", "./blogapp")

                    // Собираем образ с автотестами
                    docker.build("${AVTEST_IMAGE}", "./avtest")
                }
            }
        }

        // 3. Запускаем Django-приложение в отдельной сети
        stage('Run Django') {
            steps {
                script {
                    sh "docker network create django-network || true"
                    sh """
                        docker run -d \
                            --name ${DJANGO_CONTAINER} \
                            --network django-network \
                            -p ${DJANGO_PORT}:8000 \
                            ${DJANGO_IMAGE}
                    """
                    // Ждем, пока Django запустится
                    sleep(time: 15, unit: 'SECONDS')
                }
            }
        }

        // 4. Запускаем автотесты (они подключаются к Django через сеть)
        stage('Run Autotests') {
            steps {
                script {
                    try {
                        sh """
                            docker run --rm \
                                --name ${AVTEST_CONTAINER} \
                                --network django-network \
                                -e BASE_URL=${DJANGO_URL} \
                                ${AVTEST_IMAGE}
                        """
                    } finally {
                        // Сохраняем отчеты тестов (если Allure/JUnit)
                        archiveArtifacts artifacts: '**/allure-results/**', allowEmptyArchive: true
                    }
                }
            }
        }
    }

    post {
        always {
            // Логи и очистка
            sh "docker logs ${DJANGO_CONTAINER} --tail 100 || true"
            sh "docker stop ${DJANGO_CONTAINER} ${AVTEST_CONTAINER} || true"
            sh "docker rm ${DJANGO_CONTAINER} ${AVTEST_CONTAINER} || true"
            sh "docker network rm django-network || true"
        }
        failure {
            emailext body: """
                Тесты провалились: ${BUILD_URL}
                Логи Django:
                ${sh(script: "docker logs ${DJANGO_CONTAINER} --tail 100 2>&1", returnStdout: true)}
            """,
            subject: "FAILED: ${JOB_NAME}",
            to: 'your-team@example.com'
        }
    }
}