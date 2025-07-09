<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navigation from './components/Navigation.vue'
</script>

<template>
  <div id="app">
    <Navigation />
    <RouterView />
  </div>
</template>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

/* Ensure proper stacking context */
.navigation {
  position: relative;
  z-index: 100;
}

/* Smooth transitions for route changes */
.router-view {
  transition: opacity 0.3s ease;
}

/* Mobile-first responsive breakpoints */
@media (max-width: 320px) {
  /* Extra small devices */
  .container {
    padding: 0 10px;
  }
}

@media (min-width: 321px) and (max-width: 768px) {
  /* Mobile devices */
  .container {
    padding: 0 15px;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  /* Tablet devices */
  .container {
    padding: 0 20px;
  }
}

@media (min-width: 1025px) and (max-width: 1440px) {
  /* Desktop devices */
  .container {
    padding: 0 25px;
  }
}

@media (min-width: 1441px) {
  /* Large desktop devices */
  .container {
    padding: 0 30px;
  }
}

/* Ensure touch targets are accessible */
@media (pointer: coarse) {
  button,
  .btn,
  a {
    min-height: 44px;
    min-width: 44px;
  }
}
</style>
