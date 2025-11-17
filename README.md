# 🤖 Tool-Using AI Agent - MLOps Project

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![MLflow](https://img.shields.io/badge/MLflow-2.9+-orange.svg)](https://mlflow.org/)

An intelligent AI agent that automatically selects and uses appropriate tools to answer user queries, with full MLOps practices including monitoring, experiment tracking, and containerization.

![Architecture Diagram](docs/architecture.png)

---

## 🎯 Project Overview

This project demonstrates a complete MLOps pipeline for deploying an intelligent agent that can:
- 🧮 Perform calculations
- 🌤️ Fetch weather data
- 📚 Search Wikipedia
- 🗓️ Handle date/time queries

### Key Features

- **Intelligent Tool Selection**: Automatically chooses the right tool based on user query
- **RESTful API**: FastAPI-based service with interactive documentation
- **Real-time Monitoring**: Prometheus + Grafana dashboards
- **Experiment Tracking**: MLflow for versioning and metrics
- **Containerized**: Docker & Docker Compose for easy deployment
- **Production-Ready**: Health checks, error handling, and logging

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **API Framework** | FastAPI, Uvicorn |
| **Tools** | Calculator, OpenWeatherMap API, Wikipedia API, Python datetime |
| **Monitoring** | Prometheus, Grafana |
| **Experiment Tracking** | MLflow |
| **Containerization** | Docker, Docker Compose |
| **Language** | Python 3.11+ |

---

## 📁 Project Structure
```
app/
├── main.py                      # FastAPI application entry point
├── agent/
│   ├── logic.py                 # Agent decision-making logic
│   └── memory.py                # Conversation history management
├── tools/
│   ├── calculator.py            # Math expression evaluator
│   ├── weather.py               # Weather API integration
│   ├── wiki.py                  # Wikipedia search
│   └── datetime_tool.py         # Date/time utilities
├── monitoring/
│   ├── metrics.py               # Prometheus metrics
│   └── experiment.py            # MLflow experiment tracking
├── config/
│   ├── mlflow_config.py         # MLflow configuration
│   └── settings.yaml            # Agent configuration
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Multi-container orchestration
├── prometheus.yml               # Prometheus configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose installed
- OpenWeatherMap API key (free tier: https://openweathermap.org/api)

### Option 1: Docker (Recommended)

1. **Clone the repository**
```bash
   git clone https://github.com/yourusername/tool-using-ai-agent.git
   cd tool-using-ai-agent/app
```

2. **Set up environment variables**
```bash
   # Create .env file
   echo "OPENWEATHER_API_KEY=your_api_key_here" > .env
```

3. **Start all services**
```bash
   docker-compose up -d
```

4. **Access the services**
   - API Documentation: http://localhost:8000/docs
   - MLflow UI: http://localhost:5000
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (admin/admin)

### Option 2: Local Development

1. **Create virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
   pip install -r requirements.txt
```

3. **Set environment variables**
```bash
   export OPENWEATHER_API_KEY=your_api_key_here
```

4. **Start MLflow server**
```bash
   mlflow ui --host 0.0.0.0 --port 5000
```

5. **Start the API (in another terminal)**
```bash
   cd app
   uvicorn main:app --reload
```

---

## 📊 Usage Examples

### API Request
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is 25 * 4?",
    "user_id": "user123"
  }'
```

### Response
```json
{
  "query": "What is 25 * 4?",
  "tool_used": "calculator",
  "result": {
    "success": true,
    "result": 100,
    "expression": "25 * 4"
  },
  "timestamp": "2025-11-10T15:30:00",
  "processing_time": 0.003
}
```

### Query Types

| Query | Tool Used | Example |
|-------|-----------|---------|
| Math calculations | Calculator | "Calculate 10 + 20" |
| Weather info | Weather API | "Weather in London" |
| General knowledge | Wikipedia | "Tell me about Python programming" |
| Date/time | DateTime | "What is today's date?" |

---

## 📈 Monitoring & Tracking

### Prometheus Metrics

- `agent_request_total` - Total API requests
- `agent_tool_usage_total` - Tool usage by type
- `agent_request_latency_seconds` - Request latency
- `agent_error_total` - Error count by type
- `agent_successful_requests_total` - Successful requests

### Grafana Dashboards

Access pre-configured dashboards at http://localhost:3000:
1. Request Rate & Volume
2. Tool Usage Distribution
3. Performance Metrics
4. Error Tracking

### MLflow Experiments

Track and compare different runs:
- Agent configurations
- Performance metrics over time
- Success rates by tool
- Request latency trends

---

## 🏗️ Architecture
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────────┐
│  FastAPI API    │
│  (Port 8000)    │
└────┬────────────┘
     │
     ├──► Agent Logic ──► Tool Selection
     │                    │
     │                    ├──► Calculator
     │                    ├──► Weather API
     │                    ├──► Wikipedia
     │                    └──► DateTime
     │
     ├──► Prometheus Metrics (Port 9090)
     │    └──► Grafana Dashboards (Port 3000)
     │
     └──► MLflow Tracking (Port 5000)
```

---

## 🔧 Configuration

Edit `app/config/settings.yaml` to customize:
```yaml
agent:
  name: "Tool-Using AI Agent"
  version: "1.0.0"
  tools:
    - calculator
    - weather
    - wikipedia
    - datetime
  reasoning_strategy: "keyword_matching"
  max_history: 3

monitoring:
  prometheus_enabled: true
  mlflow_enabled: true
  log_level: "INFO"
```

---

## 🧪 Testing
```bash
# Run all tests
pytest

# Test specific tool
python app/tools/calculator.py

# Check health
curl http://localhost:8000/health
```

---

## 📸 Screenshots

### API Documentation
![API Docs](docs/api-docs.png)

### Grafana Dashboard
![Grafana](docs/grafana-dashboard.png)

### MLflow Tracking
![MLflow](docs/mlflow-ui.png)

---

## 🔮 Future Enhancements

- [ ] Add authentication (JWT tokens)
- [ ] Implement caching layer (Redis)
- [ ] Add LLM reasoning (OpenAI/HuggingFace)
- [ ] Create CI/CD pipeline (GitHub Actions)
- [ ] Deploy to cloud (AWS/GCP/Azure)
- [ ] Add more tools (email, database, file operations)
- [ ] Implement async tool execution
- [ ] Add user feedback system

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### Docker Issues
```bash
# Clean restart
docker-compose down -v
docker-compose up -d --build
```

### Weather API Not Working
- Wait 10-30 minutes for API key activation
- Verify key in `.env` file
- Check API quota at OpenWeatherMap dashboard

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- MLflow for experiment tracking
- Prometheus & Grafana for monitoring
- OpenWeatherMap for weather data
- Wikipedia API for knowledge base

---

## 📚 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Docker Documentation](https://docs.docker.com/)

---

**⭐ If you found this project helpful, please give it a star!**