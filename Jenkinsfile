pipeline {
  agent none

  environment {
    APP_ID = "L88h-MFTGdhexpR796h0y"
  }

  parameters {
    string(name: 'DEPLOY_URL_CRED_ID', defaultValue: 'DEPLOY_URL', description: 'Credentials ID for the deployment URL (Secret Text)')
    string(name: 'DEPLOY_KEY_CRED_ID', defaultValue: 'DEPLOY_KEY', description: 'Credentials ID for the deployment API key (Secret Text)')
  }

  stages {
    stage('Checkout') {
      agent any
      steps {
        checkout scm
      }
    }

    stage('Env setup') {
      agent {
        docker {
          image 'python:3.11-slim'
          args '--user root:root' // run as root so installs can happen if needed
        }
      }
      steps {
        // create virtualenv in workspace (will be persisted in workspace mount)
        sh 'python3 -m venv .venv'
        sh '. .venv/bin/activate && pip install --upgrade pip'
      }
    }

    stage('Install requirements') {
      agent {
        docker {
          image 'python:3.11-slim'
        }
      }
      steps {
        sh '. .venv/bin/activate && pip install -r requirements.txt'
      }
    }

    stage('Migrations') {
      agent {
        docker {
          image 'python:3.11-slim'
        }
      }
      steps {
        sh '. .venv/bin/activate && python manage.py makemigrations'
        sh '. .venv/bin/activate && python manage.py migrate'
      }
    }

    stage('Unit Tests') {
      agent {
        docker {
          image 'python:3.11-slim'
        }
      }
      steps {
        sh '. .venv/bin/activate && python manage.py test'
      }
    }

    stage('Start Server') {
      agent {
        docker {
          image 'python:3.11-slim'
        }
      }
      steps {
        // run server in background (use nohup to ensure it doesn't get killed immediately)
        sh 'nohup . .venv/bin/activate && python manage.py runserver 0.0.0.0:8000 >/dev/null 2>&1 &'
        sh 'sleep 5'
      }
    }

    stage('API Test') {
      agent {
        docker {
          image 'python:3.11-slim'
        }
      }
      steps {
        sh '. .venv/bin/activate && python check.py'
      }
    }
  }

  post {
    success {
      echo "✅ Tests passed, triggering deployment API..."
      withCredentials([
        string(credentialsId: params.DEPLOY_URL_CRED_ID, variable: 'DEPLOY_URL'),
        string(credentialsId: params.DEPLOY_KEY_CRED_ID, variable: 'DEPLOY_KEY')
      ]) {
        sh '''
          json_payload=$(printf '{"applicationId":"%s"}' "$APP_ID")
          curl -fS -X POST \
            "$DEPLOY_URL" \
            -H 'accept: application/json' \
            -H 'Content-Type: application/json' \
            -H "x-api-key: $DEPLOY_KEY" \
            --data-binary "$json_payload" \
            -w "\\nHTTP %{http_code}\\n"
        '''
      }
      mail to: 'princedev2112@gmail.com',
           subject: "Jenkins Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
           body: """Hello,

The Jenkins pipeline for ${env.JOB_NAME} (build #${env.BUILD_NUMBER}) has succeeded.

* Branch: ${env.BRANCH_NAME}
* Commit: ${env.GIT_COMMIT}
* Build URL: ${env.BUILD_URL}

Deployment API was triggered successfully.

Regards,
Jenkins
"""
    }

    failure {
      echo "❌ Pipeline failed, sending error email..."
      mail to: 'princedev2112@gmail.com',
           subject: "Jenkins Failure: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
           body: """Hello,

The Jenkins pipeline for ${env.JOB_NAME} (build #${env.BUILD_NUMBER}) has failed.

* Branch: ${env.BRANCH_NAME}
* Commit: ${env.GIT_COMMIT}
* Build URL: ${env.BUILD_URL}

Please check the console output for details.

Regards,
Jenkins
"""
    }
  }
}
