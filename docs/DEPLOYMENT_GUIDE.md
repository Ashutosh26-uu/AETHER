# AETHER Deployment Guide

## Quick Start (5 Minutes)

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git

### 1. Clone and Setup
```bash
cd "c:\Users\Ashutosh Mishra\OneDrive\Desktop\EY hackethon\AETHER"
pip install -r requirements.txt
```

### 2. Start Backend
```bash
python main.py --backend-only
```

### 3. Start Frontend
```bash
cd frontend
npm install
npm start
```

### 4. Access Dashboard
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Full System Deployment

### 1. Start Complete AETHER System
```bash
python main.py
```

### 2. System Components
- ✅ AI Health Monitoring
- ✅ Accident Prediction
- ✅ IoT Sensor Management
- ✅ Satellite Integration
- ✅ Drone Control
- ✅ Blockchain Security

## Production Deployment

### AWS Deployment
```bash
# Deploy infrastructure
aws cloudformation create-stack \
  --stack-name aether-prod \
  --template-body file://cloud-infrastructure/aws-deployment.yml \
  --parameters ParameterKey=Environment,ParameterValue=prod

# Deploy application
docker build -t aether-backend .
docker push your-registry/aether-backend:latest
```

### Database Setup
```bash
# PostgreSQL with PostGIS
psql -U postgres -d aether -f database/schema.sql
```

## Configuration

### Environment Variables
```bash
export AETHER_ENV=production
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=aether
export MQTT_BROKER=localhost
export AWS_REGION=us-east-1
```

## Monitoring
- System logs: `/var/log/aether/`
- Health endpoint: `/api/health`
- Metrics: Grafana dashboard
- Alerts: CloudWatch alarms

## Troubleshooting

### Common Issues
1. **WebSocket connection failed**: Check backend is running on port 8000
2. **Sensor data not updating**: Verify MQTT broker connection
3. **AI models not loading**: Check TensorFlow/PyTorch installation
4. **Database connection error**: Verify PostgreSQL is running

### Support
- Documentation: `/docs/`
- API Reference: `/api/docs`
- Issues: GitHub repository