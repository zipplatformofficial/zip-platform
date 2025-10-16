# ZIP Platform Frontend - Implementation Plan

## 🎨 Design System Complete!

### Color Palette (Red & Black Theme)

**Primary Colors:**
- Red 500 (#EF4444) - Primary actions, CTAs
- Red 600 (#DC2626) - Primary hover states
- Red 700 (#B91C1C) - Primary active states

**Dark/Black Colors:**
- Midnight 950 (#030712) - Main background
- Dark 900 (#0F172A) - Card backgrounds
- Dark 800 (#1E293B) - Input backgrounds
- Dark 700 (#334155) - Borders

**UI Components Configured:**
- `.btn-primary` - Red gradient buttons with glow effect
- `.btn-secondary` - Dark buttons
- `.btn-outline` - Red outline buttons
- `.card` - Dark glass-morphism cards
- `.input` - Dark inputs with red focus
- `.badge-primary` - Red badge with glow

---

## 📁 Project Structure (To Be Created)

```
frontend-web/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── Sidebar.jsx
│   │   ├── ui/
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Badge.jsx
│   │   │   ├── Modal.jsx
│   │   │   └── Loading.jsx
│   │   ├── auth/
│   │   │   ├── LoginForm.jsx
│   │   │   └── RegisterForm.jsx
│   │   ├── maintenance/
│   │   │   ├── ServiceCard.jsx
│   │   │   ├── BookingForm.jsx
│   │   │   └── BookingList.jsx
│   │   ├── rentals/
│   │   │   ├── VehicleCard.jsx
│   │   │   ├── RentalBookingForm.jsx
│   │   │   └── RentalList.jsx
│   │   └── store/
│   │       ├── ProductCard.jsx
│   │       ├── CartSidebar.jsx
│   │       └── CheckoutForm.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   ├── maintenance/
│   │   │   ├── Services.jsx
│   │   │   └── MyBookings.jsx
│   │   ├── rentals/
│   │   │   ├── Vehicles.jsx
│   │   │   └── MyRentals.jsx
│   │   ├── store/
│   │   │   ├── Products.jsx
│   │   │   ├── Cart.jsx
│   │   │   └── Orders.jsx
│   │   └── Profile.jsx
│   ├── context/
│   │   ├── AuthContext.jsx
│   │   ├── CartContext.jsx
│   │   └── BookingContext.jsx
│   ├── services/
│   │   ├── api.js
│   │   ├── authService.js
│   │   ├── maintenanceService.js
│   │   ├── rentalService.js
│   │   └── storeService.js
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useCart.js
│   │   └── useBooking.js
│   ├── utils/
│   │   ├── formatters.js
│   │   └── validators.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css ✅ DONE
├── tailwind.config.js ✅ DONE
└── package.json ✅ DONE
```

---

## 🚀 Implementation Steps

### Phase 1: Setup & Infrastructure ✅ COMPLETE
- [x] TailwindCSS configuration with red/black theme
- [x] Custom CSS utilities and components
- [x] Font imports (Inter, Poppins)
- [x] Scrollbar styling
- [ ] Install additional dependencies (axios, react-icons, etc.)

### Phase 2: Core Components (Priority 1)
- [ ] Button component
- [ ] Card component
- [ ] Input component
- [ ] Badge component
- [ ] Loading spinner
- [ ] Modal component

### Phase 3: Layout Components
- [ ] Navbar with logo and navigation
- [ ] Footer
- [ ] Sidebar for dashboard
- [ ] Page container/wrapper

### Phase 4: Authentication
- [ ] Login page
- [ ] Register page
- [ ] Auth context provider
- [ ] Protected route wrapper
- [ ] API service for auth

### Phase 5: Home Page
- [ ] Hero section with red/black gradient
- [ ] Services showcase
- [ ] Features section
- [ ] CTA sections
- [ ] Testimonials

### Phase 6: Mobile Car Maintenance
- [ ] Services listing page
- [ ] Service detail modal
- [ ] Booking form
- [ ] My bookings page
- [ ] Booking status tracking

### Phase 7: Car Rentals
- [ ] Vehicles listing with filters
- [ ] Vehicle detail page
- [ ] Availability checker
- [ ] Rental booking form
- [ ] My rentals page

### Phase 8: Online Auto Store
- [ ] Products catalog with search
- [ ] Product detail page
- [ ] Shopping cart sidebar
- [ ] Checkout flow
- [ ] Order history

### Phase 9: User Dashboard
- [ ] Dashboard overview
- [ ] Profile management
- [ ] All bookings/orders view
- [ ] Settings page

### Phase 10: Polish & Optimization
- [ ] Add animations and transitions
- [ ] Responsive design refinement
- [ ] Performance optimization
- [ ] Error handling
- [ ] Loading states

---

## 🎨 Design Guidelines

### Typography
- Headings: Poppins font, bold, large
- Body: Inter font, regular, readable
- Use `.heading-1`, `.gradient-text` for emphasis

### Colors Usage
- **Red (#EF4444)**: CTAs, links, active states, important info
- **Black (#030712)**: Main background
- **Dark grays**: Cards, inputs, secondary elements
- **White/Light gray**: Text, icons

### Spacing
- Sections: py-16 to py-24
- Cards: p-6 to p-8
- Margins: mb-8 to mb-12

### Shadows & Effects
- Use `.shadow-red-glow` for important elements
- Use `.hover:shadow-red-glow-lg` for hover states
- Use `.card-hover` for interactive cards

### Animations
- Fade in on page load: `.animate-fade-in`
- Slide up: `.animate-slide-up`
- Glow effect: `.animate-glow`

---

## 📦 Additional Dependencies Needed

```bash
npm install axios react-icons framer-motion
npm install react-hook-form zod
npm install react-hot-toast
npm install date-fns
```

---

## 🔌 API Integration

### Base Configuration
```javascript
// src/services/api.js
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

---

## 🎯 Key Features to Implement

### 1. Hero Section
- Full-screen hero with red gradient overlay
- Animated text and CTAs
- Service category cards

### 2. Service Cards
- Glass-morphism effect
- Red accent on hover
- Price display
- Quick action buttons

### 3. Vehicle/Product Cards
- Image carousel
- Specifications grid
- Availability indicator
- Price and rating display

### 4. Booking Flows
- Multi-step forms
- Date/time pickers
- Location selector
- Payment method selection

### 5. User Dashboard
- Stats cards with icons
- Recent activity timeline
- Quick actions menu
- Notifications panel

---

## 📱 Responsive Breakpoints

- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

Use Tailwind's responsive prefixes:
- `sm:` for tablet
- `md:` for small desktop
- `lg:` for large desktop
- `xl:` for extra large

---

## ✨ Example Component Patterns

### Button
```jsx
<button className="btn btn-primary">
  Book Service
</button>
```

### Card
```jsx
<div className="card card-hover">
  <img src="..." alt="..." className="w-full h-48 object-cover" />
  <div className="p-6">
    <h3 className="text-xl font-bold mb-2">Service Name</h3>
    <p className="text-gray-400 mb-4">Description...</p>
    <span className="badge badge-primary">GH₵ 150</span>
  </div>
</div>
```

### Input
```jsx
<input
  type="text"
  placeholder="Enter your email"
  className="input"
/>
```

---

## 🚀 Quick Start

```bash
cd frontend-web
npm install
npm run dev
```

Visit: http://localhost:5173

---

## 🎨 Live Preview

The theme features:
- ✅ Dark midnight black background
- ✅ Red accents and CTAs
- ✅ Glass-morphism cards
- ✅ Smooth animations
- ✅ Glow effects on hover
- ✅ Custom red scrollbars
- ✅ Modern typography
- ✅ Responsive design ready

---

**Status**: Theme configured, ready for component development
**Next**: Start building core UI components and pages
