<template>
  <div class="home">
    <!-- Hero Section - Apple-style -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">MyClean<sup>®</sup></h1>
        <p class="hero-subtitle">Transform your space. Transform your life.</p>
        <div class="hero-links">
          <router-link to="/services" class="hero-link">Book now</router-link>
          <router-link to="/services" class="hero-link secondary">Learn more ></router-link>
        </div>
      </div>
      <div class="hero-image">
        <img src="https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=1200&h=800&fit=crop&crop=center"
             alt="Professional cleaning service"
             class="hero-img" />
      </div>
    </section>

    <!-- Service Grid - Apple-style -->
    <section class="services-grid">
      <div class="service-item">
        <div class="service-content">
          <h2 class="service-title">Residential Cleaning</h2>
          <p class="service-description">From deep cleaning to regular maintenance.</p>
          <router-link to="/services" class="service-link">Learn more ></router-link>
        </div>
        <div class="service-image-container">
          <img src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop&crop=center"
               alt="Residential cleaning"
               class="service-img" />
        </div>
      </div>

      <div class="service-item">
        <div class="service-content">
          <h2 class="service-title">Commercial Cleaning</h2>
          <p class="service-description">Professional solutions for your business.</p>
          <router-link to="/services" class="service-link">Learn more ></router-link>
        </div>
        <div class="service-image-container">
          <img src="https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=600&h=400&fit=crop&crop=center"
               alt="Commercial cleaning"
               class="service-img" />
        </div>
      </div>
    </section>

    <!-- Feature Section - Apple-style -->
    <section class="feature">
      <div class="feature-content">
        <h2 class="feature-title">Why Choose MyClean?</h2>
        <p class="feature-subtitle">Experience the difference that professional cleaning makes.</p>
        <div class="feature-grid">
          <div class="feature-item">
            <div class="feature-icon">✨</div>
            <h3>Premium Quality</h3>
            <p>Professional-grade equipment and eco-friendly products</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">⏰</div>
            <h3>Flexible Scheduling</h3>
            <p>Book at your convenience, 24/7 online booking</p>
          </div>
          <div class="feature-item">
            <div class="feature-icon">🛡️</div>
            <h3>Trusted & Insured</h3>
            <p>Fully insured and background-checked professionals</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section - Apple-style -->
    <section class="cta">
      <div class="cta-content">
        <h2 class="cta-title">Ready to get started?</h2>
        <p class="cta-subtitle">Book your first cleaning service today.</p>
        <router-link to="/services" class="cta-button">Book Now</router-link>
      </div>
    </section>

    <!-- Footer Section - Apple-style -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <p class="footer-promo">Remember to offer beautiful flowers from Kyiv LuxeBouquets Valentines Day, Mothers Day, Christmas... Reminds you 3 days before. No spam or sharing your address</p>
          <div class="newsletter">
            <input type="email" placeholder="Your Email" class="email-input">
            <button class="remind-btn">REMIND</button>
          </div>
        </div>

        <div class="footer-links">
          <div class="footer-column">
            <h3>Contact Us</h3>
            <p><strong>Address</strong><br>15/4 Khreshchatyk Street, Kyiv</p>
            <p><strong>Phone</strong><br>+380980099777</p>
            <p><strong>General Enquiry:</strong><br>Kiev.Florist.Studio@gmail.com</p>
            <h4>Follow Us</h4>
            <div class="social-icons">
              <a href="#" class="social-icon">📘 Facebook</a>
              <a href="#" class="social-icon">📷 Instagram</a>
              <a href="#" class="social-icon">🐦 Twitter</a>
            </div>
          </div>

          <div class="footer-column">
            <h3>Shop</h3>
            <ul>
              <li>All Products</li>
              <li>Fresh Flowers</li>
              <li>Dried Flowers</li>
              <li>Live Plants</li>
              <li>Designer Vases</li>
              <li>Aroma Candles</li>
              <li>Freshener Diffuser</li>
            </ul>
          </div>

          <div class="footer-column">
            <h3>Service</h3>
            <ul>
              <li v-for="service in activeServices" :key="service.id">
                {{ service.name }}
              </li>
            </ul>
          </div>

          <div class="footer-column">
            <h3>About Us</h3>
            <ul>
              <li>Our story</li>
              <li>Blog</li>
              <li>Shipping & returns</li>
              <li>Terms & conditions</li>
              <li>Privacy policy</li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// Home page component - hardcoded services for footer
const activeServices = [
  { id: 1, name: 'Fresh Flowers' },
  { id: 2, name: 'Dried Flowers' },
  { id: 3, name: 'Designer Vases' },
  { id: 4, name: 'House Cleaning' },
  { id: 5, name: 'Office Cleaning' },
  { id: 6, name: 'Aroma Candles' }
]
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: #fff;
  color: #333;
}

/* Hero Section */
.hero {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0 20px;
  background: #fff;
}

.hero-content {
  max-width: 800px;
  margin-bottom: 60px;
}

.hero-title {
  font-size: 6rem;
  font-weight: 600;
  line-height: 1.1;
  margin-bottom: 20px;
  color: #333;
}

.hero-title sup {
  font-size: 2rem;
  vertical-align: super;
}

.hero-subtitle {
  font-size: 1.5rem;
  color: #666;
  margin-bottom: 40px;
  font-weight: 400;
}

.hero-links {
  display: flex;
  gap: 30px;
  justify-content: center;
  align-items: center;
}

.hero-link {
  color: #333;
  text-decoration: none;
  font-size: 1.2rem;
  font-weight: 500;
  transition: color 0.3s ease;
}

.hero-link:hover {
  color: #666;
}

.hero-link.secondary {
  color: #666;
}

.hero-link.secondary:hover {
  color: #333;
}

.hero-image {
  width: 100%;
  max-width: 1000px;
  margin-top: 40px;
}

.hero-img {
  width: 100%;
  height: 500px;
  object-fit: cover;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}

/* Services Grid */
.services-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  background: #fff;
  color: #333;
}

.service-item {
  position: relative;
  overflow: hidden;
  min-height: 600px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  text-align: center;
  padding: 60px 40px;
}

.service-item:nth-child(odd) {
  background: #f8f8f8;
}

.service-item:nth-child(even) {
  background: #fff;
  color: #333;
}

.service-content {
  max-width: 400px;
  z-index: 2;
  position: relative;
  margin-bottom: 40px;
}

.service-title {
  font-size: 3rem;
  font-weight: 600;
  margin-bottom: 20px;
  line-height: 1.1;
  color: #333;
}

.service-description {
  font-size: 1.3rem;
  color: #666;
  margin-bottom: 30px;
  line-height: 1.4;
}

.service-item:nth-child(even) .service-description {
  color: #666;
}

.service-link {
  color: #333;
  text-decoration: none;
  font-size: 1.2rem;
  font-weight: 500;
  transition: color 0.3s ease;
}

.service-link:hover {
  color: #666;
}

.service-image-container {
  width: 100%;
  max-width: 500px;
  position: relative;
  overflow: hidden;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.service-img {
  width: 100%;
  height: 300px;
  object-fit: cover;
  display: block;
}

/* Feature Section */
.feature {
  background: #f5f5f5;
  color: #333;
  padding: 120px 20px;
  text-align: center;
}

.feature-content {
  max-width: 1200px;
  margin: 0 auto;
}

.feature-title {
  font-size: 4rem;
  font-weight: 600;
  margin-bottom: 20px;
  line-height: 1.1;
  color: #333;
}

.feature-subtitle {
  font-size: 1.5rem;
  color: #666;
  margin-bottom: 80px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 60px;
  margin-top: 60px;
}

.feature-item {
  text-align: center;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.feature-item h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.feature-item p {
  color: #666;
  line-height: 1.5;
}

/* CTA Section */
.cta {
  background: #fff;
  color: #333;
  padding: 120px 20px;
  text-align: center;
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-size: 4rem;
  font-weight: 600;
  margin-bottom: 20px;
  line-height: 1.1;
  color: #333;
}

.cta-subtitle {
  font-size: 1.5rem;
  color: #666;
  margin-bottom: 40px;
}

.cta-button {
  display: inline-block;
  background: #333;
  color: #fff;
  text-decoration: none;
  padding: 15px 40px;
  border-radius: 25px;
  font-size: 1.2rem;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.cta-button:hover {
  background: #666;
}

/* Footer Section */
.footer {
  background: #f5f5f5;
  color: #333;
  padding: 80px 20px 40px;
  border-top: 1px solid #e0e0e0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  gap: 60px;
}

.footer-section {
  flex: 1;
  text-align: left;
}

.footer-promo {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 20px;
  line-height: 1.4;
  max-width: none;
}

.newsletter {
  display: flex;
  gap: 8px;
  max-width: 300px;
}

.email-input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.8rem;
  outline: none;
  transition: border-color 0.3s ease;
}

.email-input:focus {
  border-color: #333;
}

.remind-btn {
  background: #333;
  color: #fff;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.remind-btn:hover {
  background: #666;
}

.footer-links {
  flex: 3;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
  text-align: left;
}

.footer-column h3 {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.footer-column h4 {
  font-size: 0.9rem;
  font-weight: 600;
  margin: 20px 0 10px 0;
  color: #333;
}

.footer-column p {
  font-size: 0.8rem;
  color: #666;
  line-height: 1.4;
  margin-bottom: 6px;
}

.footer-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-column li {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 8px;
  line-height: 1.3;
  cursor: pointer;
  transition: color 0.3s ease;
}

.footer-column li:hover {
  color: #333;
}

.social-icons {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.social-icon {
  color: #666;
  text-decoration: none;
  font-size: 0.8rem;
  font-weight: 500;
  transition: color 0.3s ease;
}

.social-icon:hover {
  color: #333;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 3.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
  }
  
  .service-item {
    min-height: 500px;
    padding: 40px 20px;
  }
  
  .service-title {
    font-size: 2.5rem;
  }
  
  .feature-grid {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  
  .feature-title,
  .cta-title {
    font-size: 2.5rem;
  }
  
  .hero-links {
    flex-direction: column;
    gap: 20px;
  }

  .footer-links {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }

  .footer-content {
    flex-direction: column;
    gap: 40px;
  }

  .footer-section {
    text-align: center;
  }

  .newsletter {
    margin: 0 auto;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .service-title {
    font-size: 2rem;
  }
  
  .feature-title,
  .cta-title {
    font-size: 2rem;
  }

  .footer-links {
    grid-template-columns: 1fr;
    gap: 25px;
    text-align: center;
  }

  .footer-content {
    gap: 30px;
  }

  .newsletter {
    flex-direction: column;
    gap: 10px;
  }
}
</style>