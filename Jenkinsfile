pipeline {
    agent any
    stages {
        stage('Prepare') {
            steps {
            sh 'ls -la'
            }
        }

        stage('Build and Run Django Blog') {
            steps {
                script {
                    try {
                        // Останавливаем и удаляем старый контейнер Django
                        sh 'docker stop django-blogapp-container || true'
                        sh 'docker rm django-blogapp-container || true'

                        // Собираем образ Django
                        docker.build('django-blogapp')

                        // Запускаем контейнер Django
                        sh '''docker run -d \
                            --name django-blogapp-container \
                            -p 8000:8000 \
                            django-blogapp'''

                        // Проверяем доступность Django приложения
                        def retries = 3
                        def success = false
                        def response = ""

                        for (int i = 0; i < retries; i++) {
                            response = sh(
                                script: 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/blog/home/ || echo "000"',
                                returnStdout: true
                            ).trim()

                            if (response == "200") {
                                success = true
                                break
                            }
                            sleep(time: 5, unit: 'SECONDS')
                        }

                        if (!success) {
                            sh 'docker logs django-blogapp-container || true'
                            error "Django Blog application is not available. Last status: ${response}"
                        } else {
                            echo "Django Blog is running and available"
                        }
                    } catch (Exception e) {
                        sh 'docker logs django-blogapp-container || true'
                        throw e
                    }
                }
            }
        }
         sh '''docker exec avtest-container /bin/sh -c '
                    pip install allure-pytest beautifulsoup4 opencv-python selenium && \
                    apt-get update && \
                    apt-get install -y --no-install-recommends allure && \
                    rm -rf /var/lib/apt/lists/*
                    '''

                sh '''docker exec avtest-container /bin/sh -c '
                    apt-get update && \
                    apt-get install -y --no-install-recommends \
                        wget \
                        unzip \
                        google-chrome-stable && \
                    wget -q https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && \
                    unzip chromedriver_linux64.zip && \
                    mv chromedriver /usr/local/bin/ && \
                    chmod +x /usr/local/bin/chromedriver && \
                    rm chromedriver_linux64.zip && \
                    rm -rf /var/lib/apt/lists/*
                    '''

                        // Необязательно: можно добавить небольшую задержку
                        sleep(time: 200, unit: 'SECONDS')
                    } catch (Exception e) {
                        sh 'docker logs avtest-container || true'
                        throw e
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                echo "Cleaning up containers..."
                // Логирование перед остановкой
                sh 'docker logs django-blogapp-container --tail 50 || true'
                sh 'docker logs avtest-container --tail 50 || true'

                // Остановка контейнеров
                sh 'docker stop django-blogapp-container || true'
                sh 'docker rm django-blogapp-container || true'
                sh 'docker stop avtest-container || true'
                sh 'docker rm avtest-container || true'
            }
        }
    }
}