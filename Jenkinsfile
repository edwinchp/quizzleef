pipeline {
    agent any

    environment {
        DB_NAME = credentials('django-db-name')
        DB_USER = credentials('django-db-user')
        DB_PASSWORD = credentials('django-db-password')
        DB_HOST = credentials('django-db-host')
        DB_PORT = credentials('django-db-port')
        DJANGO_ALLOWED_HOSTS = credentials('django-allowed-hosts')
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Migrations') {
            steps {
                sh '''
                    . venv/bin/activate
                    python manage.py migrate
                '''
            }
        }

        stage('Run Server') {
            steps {
                sh '''
                    . venv/bin/activate
                    nohup python manage.py runserver 0.0.0.0:8002 &
                '''
            }
        }
    }
}