# 🚗 ZIP Platform

> Ghana's Premier Automotive Services Marketplace

Your complete solution for car rentals, mobile maintenance, and auto parts - all in one platform.

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://your-netlify-url.netlify.app)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## ✨ Features

- 🚗 **Car Rentals** - Browse and rent premium vehicles
- 🔧 **Mobile Maintenance** - On-demand car servicing at your location
- 🛒 **Auto Parts Store** - Genuine spare parts delivery
- 💳 **Secure Payments** - Integrated with Paystack
- 📱 **Mobile Responsive** - Works on all devices
- 🔐 **KYC Verification** - Smile ID integration
- 📊 **Admin Dashboard** - Complete management system

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend-web
npm install
npm run dev
```

### Access
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000/api/v1
- **API Documentation:** http://localhost:8000/docs

### Admin Setup
- **See:** `SECURITY_SETUP.md` for secure admin account creation
- **⚠️ NEVER use default credentials in production!**

## 📦 Tech Stack

### Frontend
- ⚛️ React 18
- ⚡ Vite
- 🎨 TailwindCSS
- 🔄 Redux Toolkit
- 📱 Framer Motion
- 🎯 React Router
- 📊 Recharts

### Backend
- 🐍 Python FastAPI
- 🗄️ PostgreSQL
- 🔐 JWT Authentication
- 📧 Email Service
- 💾 SQLAlchemy ORM

### Integrations
- 💳 Paystack (Payments)
- 🆔 Smile ID (KYC)
- 🗺️ Google Maps
- 🔔 Firebase (Notifications)

## 🌐 Deployment

### Deploy to Netlify

1. **Fork/Clone this repository**

2. **Configure Environment Variables**
   ```bash
   cd frontend-web
   cp .env.example .env
   # Update .env with your production values
   ```

3. **Deploy via Netlify CLI**
   ```bash
   npm install -g netlify-cli
   cd frontend-web
   netlify deploy --prod
   ```

4. **Or Connect via Netlify Dashboard**
   - Go to [Netlify](https://app.netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Connect your repository
   - Build settings:
     - **Base directory:** `frontend-web`
     - **Build command:** `npm run build`
     - **Publish directory:** `dist`
   - Add environment variables from `.env.example`
   - Deploy!

### Backend Deployment

Deploy backend to platforms like:
- Railway
- Render
- Heroku
- DigitalOcean

Update `VITE_API_URL` in frontend `.env` with your backend URL.

## 📱 Services

### Car Rentals
- Wide selection of vehicles
- Flexible rental periods
- GPS tracking
- Insurance included

### Mobile Maintenance
- Doorstep service
- Certified technicians
- Real-time tracking
- Service history

### Auto Parts
- Genuine parts
- Fast delivery
- Expert consultation
- Warranty included

## 👥 User Roles

- **Customer** - Book services, rent vehicles, shop parts
- **Admin** - Platform management
- **Technician** - Service provider
- **Vendor** - Parts supplier
- **Rental Manager** - Fleet management

## 🔐 Security

- JWT token authentication
- Password hashing with bcrypt
- CORS protection
- Rate limiting
- Input validation
- XSS protection

## 📄 License

MIT License - feel free to use this project for learning and commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support, email support@zipplatform.com

---

**Built with ❤️ for Ghana's Automotive Industry**
