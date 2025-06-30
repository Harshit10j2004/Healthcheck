# Healthcheck

A real-time website monitoring tool that tracks URL status, response time, and performance changes. Sends email alerts when a website is down or slow. Built with microservices, containerized using Docker, and deployed with Docker Swarm on AWS EC2.

- Monitor websites in real time (every 30 seconds)
- View response time and percentage changes
- Email alerts for downtime or slow performance
- OTP-based login/signup (no passwords)
- Microservices architecture
- Dockerized and Swarm-deployed

- FastAPI
- Python
- MySQL
- Docker
- Docker Swarm
- SMTP (for email alerts, login ,signup)

# Clone the repository
git clone https://github.com/your-username/healthcheck.git

cd healthcheck

# Make sure Docker and Docker Compose are installed

# Do a local test
docker compose up

# Initialize Docker Swarm (if not already)
docker swarm init

# Deploy the full stack
docker stack deploy -c docker-compose.yml healthcheck

# for whole journey visit

https://harshithere.hashnode.dev/hello-swarm

