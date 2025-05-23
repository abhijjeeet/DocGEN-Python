
pipeline {
  agent { label 'panel-assist-chatbot' }
  stages {
    stage('Build & Deploy') {
      steps {
        script {
          sh '''
            # Rebuild images
            docker-compose build
            
            # Tear down any running containers, then bring them up detached
            docker-compose down
            docker-compose up -d
          '''
        }
      }
    }
  }
  
}
