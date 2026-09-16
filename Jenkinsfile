pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/mathewjohn90/digital-inheritance-vault.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        /opt/sonar-scanner/bin/sonar-scanner \
                        -Dsonar.projectKey=Digital-Inheritance-Vault
                        -Dsonar.projectName=Digital-Inheritance-Vault \
                        -Dsonar.sources=.
                    '''
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t seclock-app:1.0 .'
            }
        }
    }
}



