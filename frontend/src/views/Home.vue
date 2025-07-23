<template>
  <div class="home">
    <!-- Hero Section - Compact -->
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
        <img src="https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=1200&h=600&fit=crop&crop=center"
             alt="Professional cleaning service"
             class="hero-img" />
      </div>
    </section>

    <!-- Compact Services & Features Combined -->
    <section class="main-content">
      <div class="services-grid">
        <div class="service-item">
          <div class="service-content">
            <h2 class="service-title">Residential Cleaning</h2>
            <p class="service-description">From deep cleaning to regular maintenance.</p>
            <router-link to="/services" class="service-link">Learn more ></router-link>
          </div>
          <div class="service-image-container">
            <img src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=300&fit=crop&crop=center"
                 alt="Residential cleaning"
                 class="service-img" />
          </div>
        </div>

        <div class="service-item">
          <div class="service-content">
            <h2 class="service-title">Commercial Cleaning</h2>
            <p class="service-description">Professional cleaning solutions for your business needs.</p>
            <router-link to="/services" class="service-link">Learn more ></router-link>
          </div>
          <div class="service-image-container">
            <img src="https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=600&h=300&fit=crop&crop=center"
                 alt="Commercial cleaning"
                 class="service-img" />
          </div>
        </div>
      </div>

      <!-- Compact Features -->
      <div class="features-section">
        <h2 class="features-title">Why Choose MyClean?</h2>
        <div class="features-grid">
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

      <!-- Compact CTA -->
      <div class="cta-section">
        <h2 class="cta-title">Ready to get started?</h2>
        <router-link to="/services" class="cta-button">Book Now</router-link>
      </div>
    </section>

    <!-- Compact Footer -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-main">
          <div class="footer-info">
            <h3>Contact Us</h3>
            <p><strong>Address:</strong> 15/4 Khreshchatyk Street, Kyiv</p>
            <p><strong>Phone:</strong> +380980099777</p>
            <p><strong>Email:</strong> Kiev.Florist.Studio@gmail.com</p>
          </div>
          
          <div class="footer-services">
            <h3>Services</h3>
            <div class="service-list">
              <span v-for="service in activeServices" :key="service.id" class="service-tag">
                {{ service.name }}
              </span>
            </div>
          </div>

          <div class="footer-newsletter">
            <h3>Stay Updated</h3>
            <p>Get reminders for special occasions</p>
            <div class="newsletter">
              <input type="email" placeholder="Your Email" class="email-input">
              <button class="remind-btn">REMIND</button>
            </div>
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

/* Compact Hero Section */
.hero {
  min-height: 70vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 20px;
  background: #fff;
}

.hero-content {
  max-width: 800px;
  margin-bottom: 40px;
}

.hero-title {
  font-size: 4.5rem;
  font-weight: 600;
  line-height: 1.1;
  margin-bottom: 15px;
  color: #333;
}

.hero-title sup {
  font-size: 1.5rem;
  vertical-align: super;
}

.hero-subtitle {
  font-size: 1.3rem;
  color: #666;
  margin-bottom: 30px;
  font-weight: 400;
}

.hero-links {
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: center;
}

.hero-link {
  color: #333;
  text-decoration: none;
  font-size: 1.1rem;
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
  max-width: 800px;
  margin-top: 30px;
}

.hero-img {
  width: 100%;
  height: 350px;
  object-fit: cover;
  border-radius: 15px;
  box-shadow: 0 15px 30px rgba(0,0,0,0.1);
}

/* Main Content Section */
.main-content {
  background: #fff;
  padding: 60px 20px;
}

/* Compact Services Grid */
.services-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin-bottom: 60px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.service-item {
  display: flex;
  flex-direction: column;
  background: #f8f8f8;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.service-content {
  padding: 30px;
  flex: 1;
}

.service-title {
  font-size: 2.2rem;
  font-weight: 600;
  margin-bottom: 15px;
  line-height: 1.1;
  color: #333;
}

.service-description {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 20px;
  line-height: 1.4;
}

.service-link {
  color: #333;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 500;
  transition: color 0.3s ease;
}

.service-link:hover {
  color: #666;
}

.service-image-container {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.service-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Compact Features Section */
.features-section {
  text-align: center;
  margin-bottom: 50px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.features-title {
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 40px;
  line-height: 1.1;
  color: #333;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.feature-item {
  text-align: center;
  padding: 20px;
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.feature-item h3 {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 10px;
  color: #333;
}

.feature-item p {
  color: #666;
  line-height: 1.4;
  font-size: 0.95rem;
}

/* Compact CTA Section */
.cta-section {
  text-align: center;
  padding: 40px 20px;
  background: #f5f5f5;
  border-radius: 15px;
  max-width: 600px;
  margin: 0 auto 40px auto;
}

.cta-title {
  font-size: 2.2rem;
  font-weight: 600;
  margin-bottom: 40px;
  line-height: 1.1;
  color: #333;
}

.cta-button {
  display: inline-block;
  background: #333;
  color: #fff;
  text-decoration: none;
  padding: 15px 35px;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.cta-button:hover {
  background: #666;
}

/* Compact Footer */
.footer {
  background: #f5f5f5;
  color: #333;
  padding: 40px 20px;
  border-top: 1px solid #e0e0e0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-main {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 40px;
  align-items: start;
}

.footer-info h3,
.footer-services h3,
.footer-newsletter h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.footer-info p {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
  margin-bottom: 8px;
}

.service-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.service-tag {
  background: #fff;
  color: #666;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  border: 1px solid #e0e0e0;
}

.footer-newsletter p {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 15px;
}

.newsletter {
  display: flex;
  gap: 8px;
  max-width: 250px;
}

.email-input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.85rem;
  outline: none;
  transition: border-color 0.3s ease;
}

.email-input:focus {
  border-color: #333;
}

.remind-btn {
  background: #333;
  color: #fff;
  padding: 10px 14px;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
  white-space: nowrap;
}

.remind-btn:hover {
  background: #666;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero {
    min-height: 60vh;
    padding: 30px 20px;
  }

  .hero-title {
    font-size: 3rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .service-title {
    font-size: 1.8rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .features-title,
  .cta-title {
    font-size: 2rem;
  }
  
  .hero-links {
    flex-direction: column;
    gap: 15px;
  }

  .footer-main {
    grid-template-columns: 1fr;
    gap: 30px;
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
    font-size: 1.6rem;
  }
  
  .features-title,
  .cta-title {
    font-size: 1.8rem;
  }

  .main-content {
    padding: 40px 15px;
  }

  .newsletter {
    flex-direction: column;
    gap: 10px;
  }
}
</style>