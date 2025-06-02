pipeline {
    agent any
    
    environment {
        IMAGE='selmi1999/pythonimg:latest'
    }

    stages {
        stage('git') {
            steps {
                git url: 'https://github.com/SelmiNazeeb/python-helloworld.git', branch: 'master'
            }
        }
        stage('build') {
            steps {
                sh '''
                docker build -t $IMAGE .
                '''
            }
        }
        stage('login and push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockercred', passwordVariable: 'PASSWORD', usernameVariable: 'USER')]) {
                sh '''
                docker login -u $USER -p $PASSWORD
                docker push $IMAGE
                '''
                }
            }
        }
        stage('deploy') {
            steps {
                sh '''
                kubectl delete deploy --all
                kubectl apply -f deploy.yaml
                '''
            }
        }
        stage('service') {
            steps {
                sh '''
                if (kubectl get svc | grep 'pythonservice'); then
                    kubectl delete svc pythonservice
                fi
                kubectl apply -f service.yaml
                '''
            }
        }
    }
}
