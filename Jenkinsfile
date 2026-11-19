pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-registration'
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv .venv'
                sh '. .venv/bin/activate && pip install --upgrade pip'
                sh '. .venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Unit Tests') {
            steps {
                sh '. .venv/bin/activate && pytest -v'
            }
        }

        stage('Security Scan') {
            steps {
                sh '. .venv/bin/activate && pip install bandit pip-audit'
                sh '. .venv/bin/activate && bandit -r app.py'
                sh '. .venv/bin/activate && pip-audit -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
                sh 'docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker compose -f ${COMPOSE_FILE} up -d --build'
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    for i in $(seq 1 30); do
                      if curl -fsS http://localhost:5000/health; then exit 0; fi
                      sleep 5
                    done
                    echo "Application health check failed"
                    exit 1
                '''
            }
        }
    }

    post {
        always {
            sh 'docker compose -f docker-compose.yml ps || true'
            archiveArtifacts artifacts: 'pytest.ini', allowEmptyArchive: true
        }
        success {
            echo 'Flask registration application deployed successfully.'
        }
        failure {
            echo 'Pipeline failed. Review the stage logs.'
        }
    }
}
