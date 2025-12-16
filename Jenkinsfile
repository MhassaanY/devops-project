pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'mhassaany/flask-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Code Fetch') {
            steps {
                echo "========== STAGE 1: CODE FETCH =========="
                echo "Marks: 6/50"
                checkout scm
                sh 'echo "✅ Code fetched from GitHub"'
                sh 'ls -la'
            }
        }
        
        stage('Docker Build') {
            steps {
                echo "========== STAGE 2: DOCKER BUILD =========="
                echo "Marks: 10/50"
                script {
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                        echo "✅ Docker image built: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    """
                }
            }
        }
        
        stage('Docker Push') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-password', variable: 'DOCKER_PASS')]) {
                    script {
                        sh """
                            docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                            echo ${DOCKER_PASS} | docker login -u mhassaany --password-stdin
                            docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                            docker push ${DOCKER_IMAGE}:latest
                            echo "✅ Image pushed to Docker Hub"
                        """
                    }
                }
            }
        }
        
        stage('Kubernetes Deployment') {
            steps {
                echo "========== STAGE 3: KUBERNETES DEPLOYMENT =========="
                echo "Marks: 17/50"
                script {
                    // First, fix the PVC issue by creating a PV for Minikube
                    sh '''
                        # Create a PersistentVolume for Minikube
                        cat <<EOF | kubectl apply -f -
                        apiVersion: v1
                        kind: PersistentVolume
                        metadata:
                          name: flask-app-pv
                        spec:
                          capacity:
                            storage: 1Gi
                          accessModes:
                            - ReadWriteOnce
                          hostPath:
                            path: "/mnt/data"
                          storageClassName: standard
                        EOF
                        
                        # Wait for PV to be ready
                        sleep 5
                    '''
                    
                    // Apply Kubernetes manifests
                    sh '''
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                        kubectl apply -f k8s/pvc.yaml
                        echo "✅ Kubernetes resources created"
                        
                        # Wait for pods to start
                        sleep 20
                        
                        # Check status
                        kubectl get pods
                        kubectl get services
                        kubectl get pvc,pv
                    '''
                }
            }
        }
        
        stage('Monitoring Setup') {
            steps {
                echo "========== STAGE 4: MONITORING SETUP =========="
                echo "Marks: 17/50"
                script {
                    sh '''
                        # Setup helm repos
                        helm repo add prometheus-community https://prometheus-community.github.io/helm-charts 2>/dev/null || true
                        helm repo add grafana https://grafana.github.io/helm-charts 2>/dev/null || true
                        helm repo update
                        
                        # Create monitoring namespace
                        kubectl create namespace monitoring 2>/dev/null || true
                        
                        # Check if Prometheus is already installed
                        if helm list -n monitoring | grep -q prometheus; then
                            echo "✅ Prometheus already installed. Upgrading..."
                            helm upgrade prometheus prometheus-community/prometheus \
                                --namespace monitoring \
                                --set server.service.type=NodePort \
                                --set server.service.nodePort=30002 \
                                --reuse-values
                        else
                            echo "Installing Prometheus..."
                            helm install prometheus prometheus-community/prometheus \
                                --namespace monitoring \
                                --set server.service.type=NodePort \
                                --set server.service.nodePort=30002
                        fi
                        
                        # Check if Grafana is already installed
                        if helm list -n monitoring | grep -q grafana; then
                            echo "✅ Grafana already installed. Skipping..."
                        else
                            echo "Installing Grafana..."
                            helm install grafana grafana/grafana \
                                --namespace monitoring \
                                --set service.type=NodePort \
                                --set service.nodePort=30003 \
                                --set adminPassword=admin
                        fi
                        
                        echo "✅ Monitoring setup completed"
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo "========== ✅ PIPELINE SUCCESS =========="
            sh '''
                echo "All stages completed successfully!"
                echo "Application accessible at: http://$(curl -s ifconfig.me):30001"
                echo "Prometheus accessible at: http://$(curl -s ifconfig.me):30002"
                echo "Grafana accessible at: http://$(curl -s ifconfig.me):30003"
            '''
        }
        failure {
            echo "========== ❌ PIPELINE FAILED =========="
            sh 'echo "Pipeline failed. Check logs above."'
        }
    }
}    
    environment {
        DOCKER_IMAGE = 'mhassaany/flask-app'
    }
    
    stages {
        // Stage 1: Code Fetch [6 marks]
        stage('Code Fetch') {
            steps {
                echo '========== STAGE 1: CODE FETCH =========='
                echo 'Marks: 6/50'
                checkout scm
                sh 'echo "✅ Code fetched from GitHub"'
                sh 'ls -la'
            }
        }
        
        // Stage 2: Docker Build [10 marks]
        stage('Docker Build') {
            steps {
                echo '========== STAGE 2: DOCKER BUILD =========='
                echo 'Marks: 10/50'
                script {
                    docker.build("${env.DOCKER_IMAGE}:${BUILD_ID}")
                    echo "✅ Docker image built: ${env.DOCKER_IMAGE}:${BUILD_ID}"
                }
                
                // Push to Docker Hub
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', 
                                                 usernameVariable: 'DOCKER_USER', 
                                                 passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    docker tag ${DOCKER_IMAGE}:${BUILD_ID} ${DOCKER_IMAGE}:latest
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push ${DOCKER_IMAGE}:${BUILD_ID}
                    docker push ${DOCKER_IMAGE}:latest
                    echo "✅ Image pushed to Docker Hub"
                    '''
                }
            }
        }
        
        // Stage 3: Kubernetes Deployment [17 marks]
        stage('Kubernetes Deployment') {
            steps {
                echo '========== STAGE 3: KUBERNETES DEPLOYMENT =========='
                echo 'Marks: 17/50'
                sh '''
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                kubectl apply -f k8s/pvc.yaml
                echo "✅ Kubernetes resources created"
                
                # Wait for pods to be ready
                sleep 10
                kubectl get pods
                kubectl get services
                '''
            }
        }
        
        // Stage 4: Monitoring Setup [17 marks]
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
            echo '========== 🎉 PIPELINE COMPLETED SUCCESSFULLY! =========='
            sh '''
            echo "\\n📋 FINAL STATUS:"
            echo "Total Marks: 50/50"
            echo "\\n🌐 APPLICATION: http://$(minikube ip):30001"
            echo "📊 GRAFANA: http://$(minikube ip):30003 (admin/admin123)"
            echo "🔍 PROMETHEUS: http://$(minikube ip):30002"
            echo "\\n✅ ALL 4 STAGES COMPLETED:"
            echo "1. Code Fetch ✓ (6/50)"
            echo "2. Docker Build ✓ (10/50)"
            echo "3. Kubernetes Deployment ✓ (17/50)"
            echo "4. Monitoring Setup ✓ (17/50)"
            '''
        }
        failure {
            echo '========== ❌ PIPELINE FAILED =========='
            sh 'echo "Pipeline failed. Check logs above."'
        }
    }
}

