# HanzlaGPT Frontend

A modern, industry-level React TypeScript frontend for HanzlaGPT - an AI-powered personal assistant.

## 🚀 Tech Stack

- **React 18** - Latest React with concurrent features
- **TypeScript** - Type-safe development
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Smooth animations
- **Lucide React** - Beautiful icons
- **React Hot Toast** - Elegant notifications
- **React Router** - Client-side routing
- **Date-fns** - Modern date utilities

## 🎨 Features

- **Modern UI/UX** - Beautiful, responsive design with smooth animations
- **Real-time Chat** - Live messaging with typing indicators
- **Provider Status** - Shows active AI provider with fallback indicators
- **Intent Detection** - Visual badges for different conversation types
- **Performance Metrics** - Response times and confidence scores
- **Mobile Responsive** - Works perfectly on all devices
- **Accessibility** - WCAG compliant design
- **Dark Mode Ready** - Easy theme switching capability

## 📦 Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🔧 Configuration

1. Copy `env.example` to `.env.local`:
```bash
cp env.example .env.local
```

2. Update the API URL in `.env.local`:
```env
VITE_API_URL=http://localhost:9090
```

## 🚀 Deployment

### Vercel (Recommended)

1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Manual Deployment

```bash
# Build the project
npm run build

# The dist folder contains your production build
```

## 🎯 Key Components

### ChatInterface
Main chat component with real-time messaging, loading states, and error handling.

### Message
Individual message component with intent badges, timestamps, and provider indicators.

### GreetingMessage
Welcome message with animated introduction and feature highlights.

### Header
Navigation header with status indicators and provider information.

## 🔄 API Integration

The frontend integrates with the HanzlaGPT backend API:

- **Health Check** - `/api/chat/health`
- **Greeting** - `/api/chat/greeting`
- **Chat Query** - `/api/chat/query`

## 🎨 Design System

### Colors
- Primary: Blue gradient (`#3b82f6` to `#8b5cf6`)
- Secondary: Purple gradient (`#d946ef` to `#a855f7`)
- Success: Green (`#10b981`)
- Warning: Yellow (`#f59e0b`)
- Error: Red (`#ef4444`)

### Typography
- **Font**: Inter (Google Fonts)
- **Monospace**: JetBrains Mono
- **Weights**: 300, 400, 500, 600, 700

### Animations
- Fade-in effects for messages
- Slide-up animations for new content
- Smooth transitions for interactions
- Loading spinners and progress indicators

## 📱 Responsive Design

- **Mobile**: 320px - 768px
- **Tablet**: 768px - 1024px
- **Desktop**: 1024px+

## 🔧 Development

### Code Structure
```
src/
├── components/     # React components
├── hooks/         # Custom React hooks
├── types/         # TypeScript type definitions
├── App.tsx        # Main app component
├── main.tsx       # Entry point
└── index.css      # Global styles
```

### Adding New Features

1. Create components in `src/components/`
2. Add types in `src/types/`
3. Create custom hooks in `src/hooks/`
4. Update styles in `src/index.css`

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests in watch mode
npm test -- --watch
```

## 📊 Performance

- **Bundle Size**: Optimized with Vite
- **Lazy Loading**: Route-based code splitting
- **Image Optimization**: Automatic optimization
- **Caching**: Efficient caching strategies

## 🔒 Security

- **CSP Headers**: Content Security Policy
- **XSS Protection**: Built-in XSS protection
- **HTTPS Only**: Secure connections
- **Input Validation**: Client-side validation

## 🌟 Future Enhancements

- [ ] Dark mode toggle
- [ ] Voice input/output
- [ ] File upload support
- [ ] Conversation history
- [ ] Export chat functionality
- [ ] Custom themes
- [ ] Accessibility improvements
- [ ] PWA capabilities

## 📄 License

MIT License - see LICENSE file for details.
