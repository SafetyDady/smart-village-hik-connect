# Smart Village HIK Connect

ระบบจัดการรถเข้าออกหมู่บ้านด้วยกล้อง ANPR และ Hikvision Integration

## 🎯 MVP Features (Phase 1)

- **Camera Connection**: เชื่อมต่อกับกล้อง Hikvision
- **Live Stream Monitoring**: ดูภาพสดจากกล้อง
- **Manual Gate Control**: เปิด/ปิดไม้กั้นด้วยตนเอง
- **Vehicle Registration**: ลงทะเบียนรถพื้นฐาน
- **Basic Dashboard**: หน้าจอควบคุมหลัก

## 🏗️ Project Structure

```
smart-village-hik-connect/
├── backend/                 # Flask API Server
│   ├── app/
│   │   ├── models/         # Database Models
│   │   ├── routes/         # API Routes
│   │   ├── services/       # Business Logic
│   │   └── utils/          # Utilities
│   ├── requirements.txt
│   └── run.py
├── frontend/               # React Web Application
│   ├── src/
│   │   ├── components/     # React Components
│   │   ├── pages/          # Page Components
│   │   ├── services/       # API Services
│   │   └── utils/          # Utilities
│   ├── package.json
│   └── public/
├── docs/                   # Documentation
└── README.md
```

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python run.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🔧 Configuration

### Camera Configuration
- IP Address: `192.168.1.xxx`
- Protocol: RTSP/HTTP
- Authentication: Username/Password

### Database Configuration
- MySQL/MariaDB
- phpMyAdmin for management

## 📋 Development Roadmap

### Phase 1: MVP (Current)
- [x] Project Setup
- [ ] Camera Connection
- [ ] Live Stream Display
- [ ] Manual Gate Control
- [ ] Vehicle Registration

### Phase 2: Core Features
- [ ] ANPR Integration
- [ ] Member Management
- [ ] Approval Workflow
- [ ] Notification System

### Phase 3: Advanced Features
- [ ] Multi-Camera Support
- [ ] Offline Mode
- [ ] Health Monitoring
- [ ] Analytics Dashboard

## 🛠️ Tech Stack

- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Backend**: Flask + SQLAlchemy + MySQL
- **Camera**: Hikvision ISAPI/RTSP
- **Development**: Local XAMPP/WAMP Stack

## 📞 Support

สำหรับคำถามและการสนับสนุน กรุณาติดต่อทีมพัฒนา

