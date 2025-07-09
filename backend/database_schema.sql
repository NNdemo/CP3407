-- MyClean Service Booking Application Database Schema

-- Users table for authentication and user management
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_provider BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Service categories (Flowers, Cleaning, etc.)
CREATE TABLE service_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Service types within categories
CREATE TABLE service_types (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES service_categories(id),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    base_price DECIMAL(10,2),
    duration_minutes INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Duration options for services
CREATE TABLE service_durations (
    id SERIAL PRIMARY KEY,
    service_type_id INTEGER REFERENCES service_types(id),
    duration_minutes INTEGER NOT NULL,
    duration_label VARCHAR(50) NOT NULL, -- e.g., "1 hour", "2 hours"
    price_multiplier DECIMAL(3,2) DEFAULT 1.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders/Bookings
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    customer_id INTEGER REFERENCES users(id),
    provider_id INTEGER REFERENCES users(id),
    service_type_id INTEGER REFERENCES service_types(id),
    service_duration_id INTEGER REFERENCES service_durations(id),

    -- Booking details
    service_date DATE NOT NULL,
    service_time_start TIME NOT NULL,
    service_time_end TIME NOT NULL,

    -- Pricing
    base_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,

    -- Status management
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'in_progress', 'completed', 'cancelled')),

    -- Additional information
    customer_notes TEXT,
    provider_notes TEXT,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confirmed_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Order status history for tracking changes
CREATE TABLE order_status_history (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    old_status VARCHAR(20),
    new_status VARCHAR(20),
    changed_by INTEGER REFERENCES users(id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Company/Business information
CREATE TABLE business_info (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_provider_id ON orders(provider_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_service_date ON orders(service_date);
CREATE INDEX idx_orders_order_number ON orders(order_number);

-- Insert initial data
INSERT INTO business_info (name, address, phone, email, description) VALUES
('MyClean', '15/4 Khreshchatyk Street, Kyiv', '+380980099777', 'Kiev.Florist.Studio@gmail.com', 'Discover Uniquely Crafted Bouquets and Gifts for Any Occasion: Spread Joy with Our Online Flower Delivery Service');

INSERT INTO service_categories (name, description) VALUES
('Flowers', 'Fresh flowers and bouquet delivery services'),
('Cleaning', 'Professional cleaning services'),
('Gifts', 'Special occasion gifts and arrangements');

INSERT INTO service_types (category_id, name, description, base_price, duration_minutes) VALUES
(1, 'Fresh Flowers', 'Beautiful fresh flower arrangements', 21.00, 60),
(1, 'Dried Flowers', 'Long-lasting dried flower arrangements', 25.00, 60),
(1, 'Designer Vases', 'Custom designer vase arrangements', 35.00, 90),
(2, 'House Cleaning', 'Complete house cleaning service', 50.00, 120),
(2, 'Office Cleaning', 'Professional office cleaning', 40.00, 90),
(3, 'Aroma Candles', 'Scented candles for special occasions', 15.00, 30);

INSERT INTO service_durations (service_type_id, duration_minutes, duration_label, price_multiplier) VALUES
(1, 60, '1 hour', 1.00),
(1, 120, '2 hours', 1.50),
(2, 90, '1.5 hours', 1.00),
(2, 180, '3 hours', 1.80),
(3, 30, '30 minutes', 1.00),
(4, 120, '2 hours', 1.00),
(4, 240, '4 hours', 1.75),
(5, 90, '1.5 hours', 1.00),
(5, 180, '3 hours', 1.60),
(6, 30, '30 minutes', 1.00);