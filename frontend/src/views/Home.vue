<template>
  <div class="home">
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-text">
          <h1>My<sup>®</sup><br>Clean</h1>
          <p>Discover Uniquely Crafted Bouquets and Gifts for Any Occasion:<br>
             Spread Joy with Our Online Flower Delivery Service</p>
          <div class="hero-divider"></div>
        </div>

        <div class="hero-image">
          <div class="service-card">
            <h2>Booking Services</h2>
            <router-link to="/services" class="shop-link">
              Shop now →
            </router-link>
          </div>
          <div class="flower-image">
            <!-- Placeholder for flower image -->
            <div class="flower-placeholder"></div>
          </div>
        </div>
      </div>
    </div>

    <div class="content-section">
      <div class="content-grid">
        <div class="content-left">
          <div class="service-info">
            <div class="service-image-placeholder"></div>
            <p>Experience the orderly joy in our modern cleaning services. Place your order online and get the cleaning service immediately. Transform your space into a brand new one.</p>
          </div>
        </div>

        <div class="content-right">
          <div class="booking-section">
            <h2>Booking Services</h2>
            <router-link to="/services" class="back-link">
              ← Shop now
            </router-link>
          </div>
          <div class="content-image">
            <div class="content-image-placeholder"></div>
          </div>
        </div>
      </div>
    </div>

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
              <!-- Social media icons would go here -->
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
              <li>Flower Subcription</li>
              <li>Wedding & Event Decor</li>
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
// Home page component
</script>

<style scoped>
.home {
  min-height: 100vh;
}

.hero-section {
  background: white;
  padding: 40px 20px;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: center;
}

.hero-text h1 {
  font-size: 4rem;
  font-weight: bold;
  color: #333;
  line-height: 1.1;
  margin-bottom: 20px;
}

.hero-text sup {
  font-size: 1.5rem;
}

.hero-text p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 30px;
}

.hero-divider {
  width: 100px;
  height: 3px;
  background: #333;
}

.hero-image {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.service-card {
  background: #f8f8f8;
  padding: 40px 20px;
  text-align: center;
  border-radius: 8px;
}

.service-card h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #333;
}

.shop-link {
  color: #333;
  text-decoration: none;
  font-weight: 500;
}

.flower-placeholder {
  width: 100%;
  height: 200px;
  background: #e0e0e0;
  border-radius: 8px;
}

.content-section {
  background: #f5f5f5;
  padding: 40px 20px;
}

.content-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

.service-image-placeholder {
  width: 100%;
  height: 200px;
  background: #d0d0d0;
  border-radius: 8px;
  margin-bottom: 20px;
}

.content-image-placeholder {
  width: 100%;
  height: 300px;
  background: #ffd700;
  border-radius: 8px;
}

.booking-section {
  text-align: right;
  margin-bottom: 20px;
}

.back-link {
  color: #333;
  text-decoration: none;
  font-weight: 500;
}

.footer {
  background: white;
  padding: 40px 20px;
  border-top: 1px solid #e0e0e0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-section {
  margin-bottom: 40px;
}

.footer-promo {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.newsletter {
  display: flex;
  gap: 0;
  max-width: 400px;
}

.email-input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-right: none;
}

.remind-btn {
  background: #333;
  color: white;
  border: none;
  padding: 12px 24px;
  cursor: pointer;
  font-weight: bold;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
}

.footer-column h3 {
  color: #333;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.footer-column ul {
  list-style: none;
}

.footer-column li {
  color: #666;
  margin-bottom: 8px;
  cursor: pointer;
}

.footer-column li:hover {
  color: #333;
}

@media (max-width: 768px) {
  .hero-content,
  .content-grid,
  .footer-links {
    grid-template-columns: 1fr;
  }

  .hero-text h1 {
    font-size: 2.5rem;
  }
}
</style>