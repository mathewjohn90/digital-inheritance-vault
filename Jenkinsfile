```groovy
pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        AWS_ACCOUNT_ID = '076510357908'

        ECR_REPOSITORY = 'digital-inheritance-vault'
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        ECR_IMAGE = "${ECR_REGISTRY}/${ECR_REPOSITORY}"

        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE = "${ECR_IMAGE}:${IMAGE_TAG}"

        SONAR_PROJECT_KEY = 'Digital-Inheritance-Vault'
        SONAR_PROJECT_NAME = 'Digital-Inheritance-Vault'
    }

    stages {

        stage('Checkout SCM') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/mathewjohn90/digital-inheritance-vault.git'
            }
        }

        stage('GitOps Check') {
            steps {
                sh '''
                    echo "Checking Git repository..."
                    git status

                    echo "Checking Kubernetes manifests..."
                    ls -la k8s/

                    test -f k8s/deployment.yml
                    test -f k8s/service.yml
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv

                    ./venv/bin/pip install --upgrade pip

                    ./venv/bin/pip install -r requirements.txt

                    ./venv/bin/pip install pytest httpx2
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    ./venv/bin/python -m pytest test_e2e.py -v
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        /opt/sonar-scanner/bin/sonar-scanner \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.projectName=${SONAR_PROJECT_NAME} \
                        -Dsonar.sources=.
                    '''
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    echo "Building Docker image..."
                    docker build -t ${IMAGE} .
                '''
            }
        }

        stage('ECR Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-ecr',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        echo "Logging in to AWS ECR..."

                        aws ecr get-login-password \
                        --region ${AWS_REGION} | \
                        docker login \
                        --username AWS \
                        --password-stdin ${ECR_REGISTRY}
                    '''
                }
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh '''
                    echo "Pushing image to ECR..."
                    docker push ${IMAGE}
                '''
            }
        }

        stage('Update Kubernetes Manifest') {
            steps {
                sh '''
                    echo "Updating Kubernetes deployment image..."

                    sed -i \
                    "s|image: .*|image: ${IMAGE}|" \
                    k8s/deployment.yml

                    echo "New image:"
                    grep "image:" k8s/deployment.yml
                '''
            }
        }

        stage('Git Commit') {
            steps {
                sh '''
                    git config user.name "Jenkins"
                    git config user.email "jenkins@localhost"

                    git add k8s/deployment.yml

                    git commit \
                    -m "Update image to ${IMAGE_TAG}" || true
                '''
            }
        }

        stage('Git Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-credentials',
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_PASSWORD'
                    )
                ]) {
                    sh '''
                        git push \
                        https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/mathewjohn90/digital-inheritance-vault.git \
                        HEAD:main
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '=========================================='
            echo ' CI/CD PIPELINE COMPLETED SUCCESSFULLY '
            echo '=========================================='
            echo "Docker Image: ${IMAGE}"
            echo "ECR Registry: ${ECR_REGISTRY}"
        }

        failure {
            echo '=========================================='
            echo ' PIPELINE FAILED '
            echo '=========================================='
            echo 'Check the failed stage in Jenkins.'
        }
    }
}
```

**Important:** this Jenkinsfile assumes you already changed `test_e2e.py` so pytest discovers the test:

```python
def test_e2e():
```

If you haven't made that change yet, the pipeline will still stop at **Test** with `collected 0 items` and exit code 5.

After pushing the corrected `test_e2e.py` and Jenkinsfile to `main`, run **Build Now**. The next target is to get **Test → SonarQube → Docker Build → ECR Push** all green.
