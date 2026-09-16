pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Code checkout completed'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t seclock-app:1.0 .'
            }
        }
    }
}
