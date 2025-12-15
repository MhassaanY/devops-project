pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'mhassaany/flask-app'
    }
    
    stages {
        stage('Code Fetch') {
            steps {
                echo '========== STAGE 1: CODE FETCH =========='
                echo 'Marks: 6/50'
                checkout scm
                sh 'echo "✅ Code fetched from GitHub"'
                sh 'ls -la'
            }
        }
        
        stage('Docker Build') {
            steps {
                echo '========== STAGE 2: DOCKER BUILD =========='
                echo 'Marks: 10/50'
                script {
                    docker.build("${env.DOCKER_IMAGE}:${BUILD_ID}")
                    echo "✅ Docker image built: ${env.DOCKER_IMAGE}:${BUILD_ID}"
                }
            }
        }
        
        stage('Kubernetes Deployment') {
            steps {
                echo '========== STAGE 3: KUBERNETES DEPLOYMENT =========='
                echo 'Marks: 17/50'
                sh '''
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                kubectl apply -f k8s/pvc.yaml
                echo "✅ Kubernetes deployment complete"
                kubectl get pods
                kubectl get services
                '''
            }
        }
        
        stage('Monitoring Setup') {
            steps {
                echo '========== STAGE 4: MONITORING SETUP =========='
                echo 'Marks: 17/50'
                sh '''
                # Add Helm repos
                helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
                helm repo add grafana https://grafana.github.io/helm-charts
                helm repo update
                
                # Create monitoring namespace
                kubectl create namespace monitoring 2>/dev/null || true
                
                # Install Prometheus
                helm install prometheus prometheus-community/prometheus \
                    --namespace monitoring \
                    --set server.service.type=NodePort \
                    --set server.service.nodePort=30002
                
                # Install Grafana
                helm install grafana grafana/grafana \
                    --namespace monitoring \
                    --set persistence.enabled=true \
                    --set adminPassword="admin123" \
                    --set service.type=NodePort \
                    --set service.nodePort=30003
                
                echo "✅ Monitoring setup complete"
                '''
            }
        }
    }
    
    post {
        success {
            echo '========== 🎉 PIPELINE SUCCESS =========='
            sh '''
            echo "Application: http://$(minikube ip):30001"
            echo "Grafana: http://$(minikube ip):30003 (admin/admin123)"
            echo "Prometheus: http://$(minikube ip):30002"
            '''
        }
        failure {
            echo '========== ❌ PIPELINE FAILED =========='
        }
    }
}
