pipeline {
    agent any

    parameters {
        booleanParam(
            name: 'RUN_SONAR',
            defaultValue: false,
            description: 'Run SonarQube scanner. Requires Jenkins SonarQube config named SonarQube.'
        )
    }

    environment {
        VENV_DIR = 'venv'
        REPORT_DIR = 'reports'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    set -eu
                    python3 -m venv "$VENV_DIR"
                    . "$VENV_DIR/bin/activate"
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install -r requirements-dev.txt
                    mkdir -p "$REPORT_DIR"
                '''
            }
        }

        stage('Format Check') {
            steps {
                sh '''
                    set -eu
                    . "$VENV_DIR/bin/activate"
                    black --check .
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    set -eu
                    . "$VENV_DIR/bin/activate"
                    ruff check .
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    set -eu
                    . "$VENV_DIR/bin/activate"
                    bandit -r . \
                        -x "$VENV_DIR,.git,__pycache__,.pytest_cache,.ruff_cache,reports,rag/chroma_db" \
                        -f txt \
                        -o "$REPORT_DIR/bandit-report.txt" || true
                '''
            }
        }

        stage('Lab Readiness') {
            steps {
                sh '''
                    set -eu
                    . "$VENV_DIR/bin/activate"
                    python scripts/check_lab_ready.py
                '''
            }
        }

        stage('Pytest') {
            steps {
                sh '''
                    set -eu
                    . "$VENV_DIR/bin/activate"
                    pytest -v tests generated_scripts \
                        --junitxml="$REPORT_DIR/pytest-report.xml" \
                        --cov=. \
                        --cov-report=xml:"$REPORT_DIR/coverage.xml"
                '''
            }
            post {
                always {
                    junit 'reports/pytest-report.xml'
                    archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
                }
            }
        }

        stage('SonarQube') {
            when {
                expression { return params.RUN_SONAR }
            }
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Sonar Quality Gate') {
            when {
                expression { return params.RUN_SONAR }
            }
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}
