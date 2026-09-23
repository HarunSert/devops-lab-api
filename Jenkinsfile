pipeline {
    agent any

    environment {
        IMAGE_REPOSITORY = "harunsert/devops-lab-api"

        HELM_RELEASE = "devops-lab-api"
        K8S_NAMESPACE = "devops-lab"

        DEPLOY_REPOSITORY = "https://github.com/HarunSert/kubernetes-production-lab.git"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Get Release Version') {
            when {
                buildingTag()
            }

            steps {
                script {
                    env.VERSION = sh(
                        script: 'git describe --tags --exact-match HEAD',
                        returnStdout: true
                    ).trim()

                    if (!(env.VERSION ==~ /^[0-9]+\\.[0-9]+\\.[0-9]+$/)) {
                        error(
                            "Invalid release tag: ${env.VERSION}. " +
                            "Expected semantic version format: 1.10.5"
                        )
                    }

                    echo "Release version: ${env.VERSION}"
                    echo "Docker image: ${IMAGE_REPOSITORY}:${env.VERSION}"
                }
            }
        }

        stage('Run Tests') {
            when {
                buildingTag()
            }

            steps {
                sh '''
                    docker run --rm \
                      -v "$WORKSPACE:/workspace" \
                      -w /workspace \
                      python:3.13-slim \
                      sh -c '
                        pip install --no-cache-dir -r requirements.txt &&
                        pytest -v
                      '
                '''
            }
        }

        stage('Build Docker Image') {
            when {
                buildingTag()
            }

            steps {
                sh '''
                    docker build \
                      --pull \
                      -t ${IMAGE_REPOSITORY}:${VERSION} .
                '''
            }
        }

        stage('Push Docker Image') {
            when {
                buildingTag()
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {

                    sh '''
                        echo "$DOCKER_TOKEN" | \
                        docker login \
                          -u "$DOCKER_USER" \
                          --password-stdin

                        docker push \
                          ${IMAGE_REPOSITORY}:${VERSION}
                    '''
                }
            }
        }

        stage('Get Deployment Repository') {
            when {
                buildingTag()
            }

            steps {
                sh '''
                    rm -rf deployment-repository

                    git clone \
                      --depth 1 \
                      ${DEPLOY_REPOSITORY} \
                      deployment-repository
                '''
            }
        }

        stage('Deploy with Helm') {
            when {
                buildingTag()
            }

            steps {
                sh '''
                    helm upgrade \
                      --install \
                      ${HELM_RELEASE} \
                      deployment-repository/helm/devops-lab-api \
                      --namespace ${K8S_NAMESPACE} \
                      --set image.repository=${IMAGE_REPOSITORY} \
                      --set-string image.tag=${VERSION} \
                      --set-string config.APP_VERSION=${VERSION} \
                      --atomic \
                      --timeout 3m
                '''
            }
        }

        stage('Verify Deployment') {
            when {
                buildingTag()
            }

            steps {
                sh '''
                    kubectl rollout status \
                      deployment/devops-lab-api \
                      -n ${K8S_NAMESPACE} \
                      --timeout=180s

                    echo ""
                    echo "Running Docker image:"

                    kubectl get deployment devops-lab-api \
                      -n ${K8S_NAMESPACE} \
                      -o jsonpath='{.spec.template.spec.containers[0].image}{"\\n"}'

                    echo ""
                    echo "Application version:"

                    kubectl exec \
                      -n ${K8S_NAMESPACE} \
                      deployment/devops-lab-api \
                      -- printenv APP_VERSION
                '''
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }

        success {
            echo "Release pipeline completed successfully."
        }

        failure {
            echo "Release pipeline failed."
        }
    }
}
