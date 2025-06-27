pipeline {
    agent any

    environment {
        TEST_IMAGE = "my-app"
        TEST_TAG = "${env.BUILD_NUMBER}"
        TEST_TARGET_URL = "http://127.0.0.1:8000/blog/home"
        WAIT_TIME = "10" // в секундах
    }

    stages {
        stage('Prepare Test Environment') {
            steps {
                script {
                    echo "Ожидаем ${WAIT_TIME} секунд перед проверкой доступности приложения..."
                    sleep(time: WAIT_TIME.toInteger(), unit: 'SECONDS')

                    // Проверка доступности приложения
                    sh """
                        if ! curl --output /dev/null --silent --head --fail "${TEST_TARGET_URL}"; then
                            echo "ERROR: Тестируемое приложение не доступно по адресу ${TEST_TARGET_URL}"
                            exit 1
                        fi
                        echo "Приложение доступно по адресу ${TEST_TARGET_URL}"
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    try {
                        // Запускаем тестовый контейнер
                        sh """
                            docker run --rm \
                                -e TEST_TARGET_URL=${TEST_TARGET_URL} \
                                ${TEST_IMAGE}:${TEST_TAG} \
                                sh -c "pip install beautifulsoup4 opencv-python && pytest -n 3 --alluredir=./allure-results"
                        """
                    } catch (Exception e) {
                        echo "Ошибка при выполнении тестов: ${e.getMessage()}"
                        throw e
                    }
                }
            }
        }

        stage('Generate Report') {
            steps {
                script {
                    // Копируем результаты тестов из контейнера
                    sh """
                        docker create --name test-container ${TEST_IMAGE}:${TEST_TAG}
                        docker cp test-container:/app/allure-results ./allure-results || true
                        docker rm -f test-container
                    """

                    // Генерируем отчет Allure
                    allureCommandline = tool name: 'allure-commandline', type: 'io.qameta.allure.jenkins.tools.AllureCommandlineInstaller'
                    sh """
                        ${allureCommandline}/bin/allure generate allure-results -o allure-report --clean
                    """
                }
            }
        }
    }

    post {
        always {
            // Публикуем отчет Allure
            allure includeProperties: false,
                   jdk: '',
                   results: [[path: 'allure-results']]

            // Очистка
            script {
                sh 'docker rm -f test-container || true'
            }
        }
    }
}