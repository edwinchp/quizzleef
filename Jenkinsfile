pipeline {
    agent any

    environment {
        DB_NAME = credentials('django-db-name')
        DB_USER = credentials('django-db-user')
        DB_PASSWORD = credentials('django-db-password')
        DB_HOST = credentials('django-db-host')
        DB_PORT = credentials('django-db-port')
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Migrations') {
            steps {
                sh 'python manage.py migrate'
            }
        }

        stage('Run Server') {
            steps {
                sh 'python manage.py runserver 0.0.0.0:8000'
            }
        }
    }
}