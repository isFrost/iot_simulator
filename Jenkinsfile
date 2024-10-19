pipeline{
    agent any

    environment{
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
        CONTAINER_NAME = 'iot_sim_1'
    }

    stages{
        stage('Clone Repository'){
            steps{
                git branch: 'mvp1', url: 'git@github.com:isFrost/iot_simulator.git'
            }
        }

        stage('Build and Start Services'){
            steps{
                script{
                    sh 'docker-compose -f DOCKER_COMPOSE_FILE up --build -d'
                }
            }
        }
    }

    post{
        always {
            script{
                echo 'To delete the containers manually after testing, run the following command:'
                echo 'docker-compose down'
            }
        }
    }
}