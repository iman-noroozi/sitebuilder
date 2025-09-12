# 🚀 PEY Builder - World-Class Website Builder Platform

<div align="center">

![PEY Builder Logo](https://img.shields.io/badge/PEY%20Builder-World%20Class-blue?style=for-the-badge&logo=webpack&logoColor=white)
![Version](https://img.shields.io/badge/version-2.0.0-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/django-4.2+-green?style=for-the-badge&logo=django&logoColor=white)

**The most advanced, AI-powered website builder platform for global users**

[🌐 Live Demo](https://pey-builder-demo.vercel.app) • [📖 Documentation](https://docs.peyai.ir) • [🎥 Video Demo](https://youtube.com/watch?v=demo) • [💬 Discord](https://discord.gg/pey-builder)

</div>

---

## 🌟 Key Features

### 🎨 **Advanced Visual Design**
- **Glass Morphism Effects** - Modern glass-like UI components
- **Neon & Glow Effects** - Eye-catching neon lighting effects
- **Particle Systems** - Interactive particle animations
- **3D Transformations** - Advanced 3D effects and rotations
- **Advanced Gradients** - Mesh gradients and animated backgrounds
- **Responsive Design** - Mobile-first, adaptive layouts

### 🤖 **AI-Powered Intelligence**
- **Smart Design Generation** - AI creates designs based on your needs
- **Color Psychology** - Emotionally optimized color schemes
- **Typography Optimization** - AI-optimized font choices and spacing
- **Content Generation** - AI-powered content in 12+ languages
- **Voice Commands** - Build websites using voice in 3 languages
- **Design Analysis** - AI analyzes and improves your designs

### 🔄 **Real-Time Collaboration**
- **Live Preview** - See changes instantly across all devices
- **Multi-User Editing** - Collaborate with team members in real-time
- **Cursor Tracking** - See where others are working
- **Comment System** - Threaded discussions on design elements
- **Version Control** - Track and revert changes
- **User Presence** - See who's online and active

### 💰 **Monetization System**
- **Subscription Tiers** - Free, Basic, Pro, Enterprise, VIP plans
- **Global Marketplace** - Sell templates and components
- **Affiliate Program** - Earn from referrals
- **Premium Features** - Unlock advanced capabilities
- **API Access** - Integrate with external services
- **White-label Solutions** - Custom branding for clients

### 🎮 **Viral Features**
- **Gamification** - Levels, badges, and achievements
- **Daily Challenges** - Engaging daily tasks
- **Leaderboards** - Compete with global users
- **Social Sharing** - Share creations on social media
- **Template Sharing** - Global template marketplace
- **Referral System** - Invite friends and earn rewards

### 📤 **Advanced Export**
- **Multiple Formats** - HTML, CSS, JS, PDF, PNG, ZIP
- **PWA Support** - Progressive Web App generation
- **Static Site Generator** - JAMstack-ready exports
- **SEO Optimization** - Built-in SEO best practices
- **Performance Optimization** - Minified and optimized code
- **Accessibility** - WCAG 2.1 AA compliant

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Redis (for real-time features)
- PostgreSQL (for production)

### 1. Clone the Repository
```bash
git clone https://github.com/iman-noroozi/sitebuilder.git
cd sitebuilder
```

### 2. Install Dependencies
```bash
# Backend dependencies
pip install -r backend/requirements.txt

# Frontend dependencies
npm install
```

### 3. Setup Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Run Database Migrations
```bash
python backend/manage.py migrate
```

### 5. Start the Development Server
```bash
# Start backend
python backend/manage.py runserver

# Start frontend (in another terminal)
npm run dev

# Start real-time preview server
python real_time_preview_system.py
```

### 6. Access the Application
- **Main App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Docs**: http://localhost:8000/api/docs
- **Real-time Preview**: ws://localhost:8765

---

## 🛠️ Installation

### Docker Installation (Recommended)
```bash
# Clone repository
git clone https://github.com/iman-noroozi/sitebuilder.git
cd sitebuilder

# Build and start with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:8000
```

### Manual Installation
```bash
# 1. Clone repository
git clone https://github.com/iman-noroozi/sitebuilder.git
cd sitebuilder

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r backend/requirements.txt

# 4. Install Node.js dependencies
npm install

# 5. Setup database
python backend/manage.py migrate
python backend/manage.py createsuperuser

# 6. Collect static files
python backend/manage.py collectstatic

# 7. Start services
python backend/manage.py runserver &
npm run dev &
python real_time_preview_system.py &
```

---

## 🎨 Usage Examples

### Creating a Website
```python
from sitebuilder import SiteBuilder

# Initialize builder
builder = SiteBuilder()

# Create new website
website = builder.create_website({
    'name': 'My Portfolio',
    'template': 'modern_portfolio',
    'ai_optimization': True
})

# Add content with AI
content = builder.generate_ai_content({
    'type': 'about_section',
    'language': 'en',
    'tone': 'professional'
})

# Apply design
builder.apply_design(website, {
    'style': 'modern',
    'colors': ['#667eea', '#764ba2'],
    'typography': 'inter'
})

# Export website
builder.export(website, {
    'format': 'html',
    'optimize': True,
    'seo': True
})
```

### Real-Time Collaboration
```python
from real_time_preview_system import RealTimePreviewSystem

# Start collaboration server
preview = RealTimePreviewSystem(port=8765)

# Add collaborators
preview.add_collaborator('user1', {
    'name': 'John Doe',
    'role': 'editor',
    'permissions': ['edit', 'comment']
})

# Start real-time preview
preview.start()
```

### AI Design Generation
```python
from ai_powered_design_system import AIPoweredDesignSystem

# Initialize AI design system
ai_design = AIPoweredDesignSystem()

# Generate design based on requirements
design = ai_design.generate_design({
    'industry': 'technology',
    'mood': 'professional',
    'style': 'modern'
})

# Analyze and optimize
analysis = ai_design.analyze_design(design)
optimized = ai_design.optimize_design(design, {
    'performance': True,
    'accessibility': True
})
```

---

## 🤖 AI Features

### Content Generation
- **12+ Languages** - Generate content in multiple languages
- **Industry-Specific** - Tailored content for different industries
- **SEO Optimized** - AI-optimized for search engines
- **Tone Adaptation** - Professional, casual, or creative tones
- **Readability Analysis** - Ensures content is easy to read

### Design Intelligence
- **Color Psychology** - Emotionally optimized color schemes
- **Typography Selection** - AI-chosen fonts for readability
- **Layout Optimization** - Responsive and accessible layouts
- **Performance Analysis** - Speed and accessibility scoring
- **A/B Testing** - Test different design variations

### Voice Commands
- **Multi-Language** - Persian, English, Arabic support
- **Natural Language** - Speak naturally to build websites
- **Command Recognition** - Understands complex instructions
- **Text-to-Speech** - Audio feedback for actions
- **Accessibility** - Voice-first design approach

---

## 🌍 Global Features

### Internationalization
- **50+ Languages** - Full translation support
- **RTL Support** - Right-to-left language layouts
- **Cultural Adaptation** - Region-specific design patterns
- **Currency Support** - Multi-currency payment processing
- **Time Zones** - Global time zone handling

### Localization
- **Regional Templates** - Location-specific design templates
- **Local Payment Methods** - Region-appropriate payment options
- **Cultural Colors** - Culturally appropriate color schemes
- **Local Fonts** - Region-specific typography choices
- **Holiday Themes** - Seasonal and cultural themes

---

## 📊 Performance

### Benchmarks
- **Page Load Time**: < 2 seconds
- **First Contentful Paint**: < 1.5 seconds
- **Largest Contentful Paint**: < 2.5 seconds
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

### Optimization Features
- **Code Splitting** - Load only necessary code
- **Image Optimization** - Automatic image compression
- **CDN Integration** - Global content delivery
- **Caching Strategy** - Intelligent caching system
- **Progressive Loading** - Load content progressively

---

## 🔧 API Documentation

### REST API Endpoints

#### Authentication
```http
POST /api/auth/login
POST /api/auth/register
POST /api/auth/refresh
POST /api/auth/logout
```

#### Website Management
```http
GET    /api/websites/          # List websites
POST   /api/websites/          # Create website
GET    /api/websites/{id}/     # Get website
PUT    /api/websites/{id}/     # Update website
DELETE /api/websites/{id}/     # Delete website
```

#### AI Features
```http
POST /api/ai/generate-content  # Generate AI content
POST /api/ai/analyze-design    # Analyze design
POST /api/ai/optimize-layout   # Optimize layout
POST /api/ai/voice-command     # Process voice command
```

#### Real-Time Collaboration
```http
WebSocket /ws/preview/         # Real-time preview
WebSocket /ws/collaboration/   # Live collaboration
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Fork the repository
git clone https://github.com/your-username/sitebuilder.git
cd sitebuilder

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and commit
git commit -m "feat: add amazing feature"

# Push to branch
git push origin feature/amazing-feature

# Create Pull Request
```

### Code Style
- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Write tests for new features
- Update documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Django Team** - For the amazing web framework
- **React Team** - For the powerful frontend library
- **OpenAI** - For AI capabilities
- **Contributors** - All the amazing contributors
- **Community** - For feedback and support

---

<div align="center">

**Made with ❤️ by the PEY Builder Team**

[⭐ Star this repo](https://github.com/iman-noroozi/sitebuilder) • [🐛 Report Bug](https://github.com/iman-noroozi/sitebuilder/issues) • [💡 Request Feature](https://github.com/iman-noroozi/sitebuilder/issues)

[Website](https://peyai.ir) • [Documentation](https://docs.peyai.ir) • [Support](https://support.peyai.ir)

</div>

---

*Last updated: December 2024*
