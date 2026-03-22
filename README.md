# Coffee Shop App - "Cozy Cup Corner"

A prototype online coffee shop ordering application demonstrating full-stack web development with user authentication, product browsing, shopping cart, and order management.

## ⚠️ Important Notice

**The development of this App has been terminated.** This App will not be maintained in the future, as it is a school project. Additionally, this App may contain bugs which will not be fixed.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Technology Stack](#technology-stack)
5. [Project Structure](#project-structure)
6. [Getting Started](#getting-started)
7. [How It Works](#how-it-works)
8. [User Guide](#user-guide)
9. [Database Schema](#database-schema)
10. [API Endpoints](#api-endpoints)
11. [Troubleshooting](#troubleshooting)

---

## Overview

**Cozy Cup Corner** is a full-stack web application for an online coffee shop. It demonstrates the integration between:

- **Frontend Layer**: HTML5, CSS3, and JavaScript providing an interactive user interface
- **Backend Layer**: Python Flask server handling business logic and user authentication  
- **Database Layer**: MySQL storing user accounts, product information, and orders

The application is designed as an educational prototype to test connectivity between the web interface and backend services.

---

## Features

### User Management
- **User Registration**: Create new accounts with username and password
- **User Authentication**: Secure login system with session management
- **Session Tracking**: Maintains user state across the application with unique order keys

### Product Browsing
- **Menu Categories**: 
  - Cold Beverages
  - Delights (specialty items)
  - Desserts
- **Product Display**: Organized product cards with details
- **No Login Required**: Browse the menu without authentication

### Shopping & Orders
- **Add to Cart**: Select quantities and add items to your cart
- **Dynamic Quantities**: Increase/decrease item quantities easily
- **Cart Persistence**: Cart data stored per user in the database
- **Order Tracking**: View all items in your cart with running total cost
- **Automatic Total Calculation**: Real-time cost summation

### Additional Pages
- **Home Page**: Welcome landing page with navigation
- **About Page**: Information about the coffee shop
- **3D Visualization**: Interactive Three.js 3D scene (experimental feature)

---

## System Architecture

```
┌─────────────────────────────────────┐
│      Client Layer (Browser)         │
│  HTML + CSS + JavaScript            │
│  (Templates & Static Files)         │
└────────────────┬────────────────────┘
                 │
                 │ HTTP/Fetch Requests
                 ▼
┌─────────────────────────────────────┐
│    Flask Backend (Python)           │
│  • Route Handling                   │
│  • Authentication & Sessions        │
│  • Business Logic                   │
│  • Cart Management                  │
└────────────────┬────────────────────┘
                 │
                 │ SQL Queries
                 ▼
┌─────────────────────────────────────┐
│      MySQL Database                 │
│  • User Accounts                    │
│  • Shopping Carts (per user)        │
│  • Order Management                 │
└─────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
- **HTML5**: Page structure and content
- **CSS3**: Styling and responsive layouts
  - Custom stylesheets for each page
  - Navigation bar, menu items, forms, buttons
- **JavaScript (Vanilla)**: 
  - `Menu.js`: Shopping cart interactions
  - `Renderer.js`: 3D visualization with Three.js
- **Three.js Library**: 3D graphics and animation (via CDN)
- **Font Awesome Icons**: Vector icons (via CDN)

### Backend
- **Python 3.6+**: Server-side logic
- **Flask**: Lightweight web framework
- **Flask Sessions**: User authentication and state management

### Database
- **MySQL**: Relational database for persistence
- **PyMySQL**: Python MySQL connector

### Desktop Application (Legacy)
- **CEF (Chromium Embedded Framework)**: Browser embedding
- **Tkinter**: GUI framework for desktop windows
- **cefpython3**: Python bindings for CEF

---

## Project Structure

```
Coffee-Shop-App/
├── WebApp.py                          # Main Flask web server (RECOMMENDED)
├── DesktopApp.py                      # Legacy desktop app (Deprecated)
├── README.md                          # This documentation
├── Components/
│   ├── WebRenderer.py                 # CEF browser rendering engine
│   └── __pycache__/                   # Python cache
├── templates/                         # HTML page templates
│   ├── index.html                     # Home page
│   ├── Menu.html                      # Main menu page
│   ├── Menu-Cold.html                 # Cold beverages submenu
│   ├── Menu-Delights.html             # Special items submenu
│   ├── Menu-Desserts.html             # Desserts submenu
│   ├── Orders.html                    # Shopping cart page
│   ├── Login.html                     # Login form page
│   ├── Signup.html                    # Registration form page
│   ├── About.html                     # About page
│   ├── ThreeJS.html                   # 3D visualization page
│   └── UIStyles/
│       └── NavigationBarStyles.css    # Navbar styling
├── static/                            # Static assets
│   ├── Home.css                       # Home page styles
│   ├── menu.css                       # Menu page styles
│   ├── Order.css                      # Orders page styles
│   ├── Buttons.css                    # Button component styles
│   ├── Account.css                    # Login/Signup form styles
│   ├── Scripts/
│   │   ├── Menu.js                    # Shopping cart logic
│   │   └── Renderer.js                # 3D scene rendering
│   └── assets/
│       └── cold-coffee.jpg            # Product image assets
└── __pycache__/                       # Python cache
```

---

## Getting Started

### Prerequisites

- **Python 3.6 - 3.9** (3.9.x recommended)
- **MySQL Server** (running and accessible)
- **pip** (Python package manager)

### Installation & Setup

1. **Clone or download the repository**
   ```bash
   cd Coffee-Shop-App
   ```

2. **Install Python dependencies**
   ```bash
   pip install Flask flask-mysqldb PyMySQL
   ```
   
   *(Optional) For desktop app support:*
   ```bash
   pip install cefpython3
   ```

3. **Set up MySQL Database**
   ```sql
   CREATE DATABASE coffee;
   USE coffee;
   
   CREATE TABLE users (
     userID INT AUTO_INCREMENT PRIMARY KEY,
     username VARCHAR(50) UNIQUE NOT NULL,
     password VARCHAR(100) NOT NULL,
     orderKey VARCHAR(12) UNIQUE NOT NULL
   );
   ```

4. **Configure Database Connection**
   - Ensure MySQL server is running (typically `localhost:3306`)
   - Default configuration: 
     - Host: `localhost`
     - User: `root`
     - Password: (prompted at startup)
     - Database: `coffee`

### Running the Application

#### **Option 1: Web Server (RECOMMENDED)** ✅

```bash
python WebApp.py
```

You will be prompted for:
- MySQL root password
- Debug mode (Y/N) - recommended for development

The app will start at `http://localhost:5000`

#### **Option 2: Desktop Application (DEPRECATED)** ❌

```bash
python DesktopApp.py
```

**Note:** This option is obsolete and not recommended due to:
- Limited CSS/blur effect support
- Numerous bugs
- Python 3.9.x maximum compatibility
- Poor web component rendering

---

## How It Works

### 1. Application Startup (WebApp.py)

```
1. Start Flask development server on port 5000
2. Initialize MySQL database connection
3. Set up Flask session management with secret key
4. Load all route handlers
5. Listen for HTTP requests on localhost:5000
```

### 2. User Registration Flow

```
User visits /Signup
    ↓
Fills registration form (username, password)
    ↓
POST /Signup
    ↓
Flask validates input
    ↓
Generate random 12-character orderKey
    ↓
Create user record in database
    ↓
Set session variables (logged_in=True, username, order-key)
    ↓
Redirect to home page (logged in)
```

### 3. Login Flow

```
User visits /login
    ↓
Enters credentials (username, password)
    ↓
POST /login
    ↓
Flask queries database for user
    ↓
Validates password
    ↓
Retrieves stored orderKey
    ↓
Set session variables
    ↓
Redirect to home page (logged in)
```

### 4. Product Browsing Flow

```
User visits /menu (no login required)
    ↓
Flask renders Menu.html with all categories
    ↓
User selects category (Cold, Delights, Desserts)
    ↓
Navigates to corresponding page (/menu-cold, etc.)
    ↓
Displays product cards with prices
    ↓
User can select quantity (JavaScript Menu.js)
```

### 5. Shopping Cart Flow

```
User selects product & quantity
    ↓
Clicks "Add to Cart"
    ↓
JavaScript (Menu.js) sends fetch request to /add-to-cart
    ↓
Includes: {qty, itemName, price} in JSON payload
    ↓
Flask checks if user is logged in
    ├─ NOT logged in: Redirect to /login
    └─ Logged in: Continue
    ↓
Flask creates table: cart_for_{orderKey}
    (if not already exists)
    ↓
INSERT item record in cart table:
    - orderID (auto-increment)
    - orderKey (user's unique key)
    - user_name (username)
    - item (product name)
    - quantity (user selected qty)
    - price (unit price)
    - added_time (timestamp)
    ↓
Return JSON success response
    ↓
JavaScript updates button state on page
```

### 6. View Orders Flow

```
User visits /orders
    ↓
Flask checks session (must be logged in)
    ├─ NOT logged in: Redirect to /login
    └─ Logged in: Continue
    ↓
Flask queries cart_for_{orderKey} table
    ↓
Retrieves all items for user
    ↓
Calculates total: SUM(quantity × price)
    ↓
Renders Orders.html with:
    - Itemized list (name, qty, price, subtotal)
    - Grand total
```

### 7. Logout Flow

```
User clicks "Logout"
    ↓
GET /logout
    ↓
Flask clears cart table (DELETE from cart_for_{orderKey})
    ↓
Clears session variables
    ↓
Redirect to home page (logged out)
```

---

## User Guide

### Step 1: Create an Account

1. Click **"Sign Up"** link in top navigation
2. Enter a unique username
3. Enter a password
4. Click **"Sign Up"** button
5. You are automatically logged in

### Step 2: Browse the Menu

1. Click **"Menu"** in navigation
2. Select a category:
   - **Cold** - Cold beverages
   - **Delights** - Specialty items  
   - **Desserts** - Sweet treats
3. View product cards with names, descriptions, and prices

### Step 3: Add Items to Cart

1. On any menu page, find the product you want
2. Use the **quantity selector** (+ and - buttons)
3. Click **"Add to Cart"** button
4. A confirmation message appears

### Step 4: View Your Cart

1. Click **"Orders"** in navigation
2. See all items you've added
3. View quantities, unit prices, and subtotals
4. See the **Grand Total** at the bottom

### Step 5: Logout

1. Click the **user dropdown** (top right) showing your username
2. Click **"Logout"**
3. Your cart is automatically cleared
4. You are returned to the home page

---

## Database Schema

### `users` Table

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| `userID` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| `username` | VARCHAR(50) | UNIQUE, NOT NULL | User login name |
| `password` | VARCHAR(100) | NOT NULL | User password (hashed) |
| `orderKey` | VARCHAR(12) | UNIQUE, NOT NULL | Unique order/cart identifier |

### `cart_for_{orderKey}` Tables

*Created dynamically per user (named with their orderKey)*

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| `orderID` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique order item identifier |
| `orderKey` | VARCHAR(12) | NOT NULL | Links to user's orderKey |
| `user_name` | VARCHAR(50) | NOT NULL | Username of cart owner |
| `item` | VARCHAR(100) | NOT NULL | Product name |
| `quantity` | INT | NOT NULL | Item quantity ordered |
| `price` | DECIMAL(10,2) | NOT NULL | Unit price per item |
| `added_time` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When item was added |

---

## API Endpoints

### Navigation & Page Routes

| Method | Route | Authentication | Purpose |
|--------|-------|-----------------|---------|
| GET | `/` | None | Home page |
| GET | `/menu` | None | Main menu page |
| GET | `/menu-cold` | None | Cold beverages menu |
| GET | `/menu-delights` | None | Special items menu |
| GET | `/menu-desserts` | None | Desserts menu |
| GET | `/about-us` | None | About page |
| GET | `/ThreeJS` | None | 3D visualization page |

### Authentication Routes

| Method | Route | Authentication | Purpose |
|--------|-------|-----------------|---------|
| GET | `/login` | None | Display login form |
| POST | `/login` | None | Process login credentials |
| GET | `/Signup` | None | Display registration form |
| POST | `/Signup` | None | Create new user account |
| GET | `/logout` | Required | Clear session and cart |

### Shopping Routes

| Method | Route | Authentication | Purpose | Request Body |
|--------|-------|-----------------|---------|--------------|
| GET | `/orders` | Required | Display user's cart | N/A |
| POST | `/add-to-cart` | Required | Add item to cart | `{"qty": int, "itemName": string, "price": float}` |

### Response Formats

**Success Response (add-to-cart):**
```json
{
  "status": "success",
  "message": "Item added to cart"
}
```

**Error Response (not logged in):**
```json
{
  "status": "redirect",
  "redirect": "/login"
}
```

---

## Logging

The Flask application logs all activities to `flask.log` in the application directory:

```
[TIMESTAMP] INFO: User login successful - username=john
[TIMESTAMP] INFO: Item added to cart - itemName=Latte, quantity=2
[TIMESTAMP] INFO: User logout - username=john, cart cleared
[TIMESTAMP] ERROR: Database connection failed
```

Log levels: DEBUG, INFO, WARNING, ERROR

---

## Troubleshooting

### Application Won't Start

**Error**: `ConnectionError: MySQL server not accessible`

**Solution**:
1. Ensure MySQL server is running: `mysql -u root -p`
2. Verify database exists: `SHOW DATABASES;`
3. Check correct password is entered when prompted

**Error**: `Port 5000 already in use`

**Solution**:
1. Kill the process using port 5000: `lsof -i :5000` then `kill -9 <PID>`
2. Or modify Flask port in code: `app.run(port=5001)`

### Login Not Working

**Issue**: Login credentials rejected

**Solution**:
1. Verify you created an account first (Go to /Signup)
2. Check username and password match exactly (case-sensitive)
3. Clear browser cookies and try again

### Item Not Adding to Cart

**Issue**: "Add to Cart" button doesn't work

**Solution**:
1. Verify you are logged in (check top-right username)
2. If not logged in, you'll be redirected to /login
3. Check browser console for JavaScript errors (F12)

### Cart is Empty After Login

**Issue**: Items disappeared from cart

**Solution**:
1. Default behavior: Cart clears on logout
2. Cart is user-specific; verify you're logged in as the right user
3. Database may need recreation if corrupted

### Desktop App Crashes

**Issue**: DesktopApp.py won't run

**Solution**:
1. Desktop app is **deprecated and not supported**
2. Use WebApp.py instead: `python WebApp.py`
3. If you must use desktop:
   - Downgrade to Python 3.9.x
   - Run: `pip install cefpython3`
   - Accept numerous bugs/limitations

### 3D Scene Not Display (ThreeJS Page)

**Issue**: 3D visualization page is blank

**Solution**:
1. Verify internet connection (Three.js loads from CDN)
2. Check browser console for JavaScript errors (F12)
3. This is an experimental feature with basic implementation

---

## Development Notes

- **Session Management**: Each user gets a unique 12-character `orderKey` to track orders
- **Cart Isolation**: Each user has their own database table (`cart_for_{orderKey}`)
- **No Order Persistence**: Carts are cleared on logout (not a persistent order history)
- **No Payment System**: App is for demonstration only
- **No Email Verification**: Registration is instant, no email required

---

## License & Attribution

Non-proprietary prototype project created for educational purposes.

---

## Support

As this is a terminated school project, **no support or maintenance is provided**. For questions or reporting bugs, refer to the code comments and database schema above.
   
