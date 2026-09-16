pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Code checkout completed'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install -r requirements.txt'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t seclock-app:1.0 .'
            }
        }
    }
}
