<script>
  import '../app.css';
  import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';

  
  
  // Navigation items
  const navItems = [
    { name: 'Home', path: '/' },
    { name: 'Visualization', path: '/self-made-trend' },
    { name: 'Analysis', path: '/analysis' },
    { name: 'Methodology', path: '/methodology' },
    { name: 'About', path: '/about' }
  ];
  
  // Current page path
  let currentPath = '/';
  
  // Mobile menu state
  let mobileMenuOpen = false;
  
  // Billionaire silhouettes for background (used across all pages)
  const billionaires = [
    { top: '10%', left: '5%', size: '180px', rotation: '-5deg' },
    { top: '15%', left: '75%', size: '220px', rotation: '8deg' },
    { top: '60%', left: '15%', size: '200px', rotation: '3deg' },
    { top: '50%', left: '85%', size: '190px', rotation: '-7deg' },
    { top: '80%', left: '60%', size: '210px', rotation: '5deg' },
    { top: '30%', left: '40%', size: '170px', rotation: '-3deg' },
  ];
  
  let isLoaded = false;
  
  // Update current path when component mounts
  onMount(() => {
    currentPath = window.location.pathname;
    
    // Update current path when navigation occurs
    const handleNavigation = () => {
      currentPath = window.location.pathname;
      mobileMenuOpen = false;
    };
    
    window.addEventListener('popstate', handleNavigation);
    
    // Set loaded state for animations
    setTimeout(() => {
      isLoaded = true;
    }, 100);
    
    return () => {
      window.removeEventListener('popstate', handleNavigation);
    };
  });
  
  // Toggle mobile menu
  function toggleMobileMenu() {
    mobileMenuOpen = !mobileMenuOpen;
  }
  
  // Handle navigation and prevent default if it's a local link
  function handleNavClick(event, path) {
    if (event.target.tagName === 'A' && event.target.getAttribute('href').startsWith('/')) {
      event.preventDefault();
      window.history.pushState({}, '', path);
      currentPath = path;
      mobileMenuOpen = false;
    }
  }
</script>

<div class="app-container" class:loaded={isLoaded}>
  <!-- Background with billionaire silhouettes (applied to all pages) -->
  
  <div class="billionaire-background">
    {#each billionaires as billionaire, i}
      <div 
        class="billionaire-silhouette" 
        style="top: {billionaire.top}; left: {billionaire.left}; width: {billionaire.size}; height: {billionaire.size}; transform: rotate({billionaire.rotation});"
      >
        <div class="silhouette silhouette-{i % 4 + 1}"></div>
      </div>
    {/each}
  </div>

<div in:fade={{ duration: 300 }} out:fade={{ duration: 300 }}>
  <slot />
</div>

  
  <!-- Main Content -->
  <main id="main-content" class="app-main">
    <slot />
  </main>
  

</div>

<style>
  /* Base Styles */
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: 'Playfair Display', 'Georgia', serif;
    color: #333;
    background-color: #f5f5f5;
    min-height: 100vh;
    overflow-x: hidden;
  }
  
  :global(*) {
    box-sizing: border-box;
  }
  
  .app-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    position: relative;
    opacity: 0;
    transition: opacity 0.5s ease;
  }
  
  .app-container.loaded {
    opacity: 1;
  }
  
  /* Background Styles (applied to all pages) */
  .background-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(245, 245, 245, 0.85);
    z-index: -1;
  }
  
  .billionaire-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -2;
  }
  
  .billionaire-silhouette {
    position: fixed;
    opacity: 0.12;
    filter: grayscale(100%);
    overflow: hidden;
    border-radius: 50%;
  }
  
  .silhouette {
    width: 100%;
    height: 100%;
    background-size: cover;
    background-position: center;
  }
  
  .silhouette-1 {
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/3/34/Elon_Musk_Royal_Society_%28crop2%29.jpg');
  }
  
  .silhouette-2 {
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/a/a8/Bill_Gates_2017_%28cropped%29.jpg');
  }
  
  .silhouette-3 {
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/1/18/Mark_Zuckerberg_F8_2019_Keynote_%2832830578717%29_%28cropped%29.jpg');
  }
  
  .silhouette-4 {
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/9/91/Jeff_Bezos_at_Amazon_Spheres_Grand_Opening_in_Seattle_-_2018_%2839074799225%29_%28cropped%29.jpg');
  }
  
  /* Skip Link (Accessibility) */
  .skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #333;
    color: white;
    padding: 8px;
    z-index: 100;
    transition: top 0.3s;
  }
  
  .skip-link:focus {
    top: 0;
  }
  
  
  .logo {
    display: flex;
    align-items: center;
  }
  
  .logo-link {
    text-decoration: none;
    color: #333;
    display: flex;
    align-items: center;
  }
  
  .logo-text {
    font-family: 'Playfair Display', 'Georgia', serif;
    font-weight: 900;
    font-size: 1.5rem;
    letter-spacing: -0.02em;
  }
  
  .logo-separator {
    margin: 0 0.25rem;
    color: #9c8c61;
  }
  
  /* Desktop Navigation */
  .desktop-nav {
    display: block;
  }
  
  .nav-list {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 2rem;
  }
  
  .nav-item {
    position: relative;
  }
  
  .nav-link {
    text-decoration: none;
    color: #555;
    font-family: 'Arial', sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
    transition: color 0.3s;
    padding: 0.5rem 0;
    position: relative;
  }
  
  .nav-link:hover {
    color: #333;
  }
  
  .nav-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: #9c8c61;
    transform: scaleX(0);
    transform-origin: center;
    transition: transform 0.3s ease;
  }
  
  .nav-link:hover::after,
  .nav-link.active::after {
    transform: scaleX(1);
  }
  
  /* Mobile Menu Toggle */
  .mobile-menu-toggle {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
  }
  
  .menu-icon {
    display: block;
    position: relative;
    width: 24px;
    height: 2px;
    background-color: #333;
    transition: background-color 0.3s;
  }
  
  .menu-icon::before,
  .menu-icon::after {
    content: '';
    position: absolute;
    width: 24px;
    height: 2px;
    background-color: #333;
    transition: transform 0.3s;
  }
  
  .menu-icon::before {
    top: -8px;
  }
  
  .menu-icon::after {
    bottom: -8px;
  }
  
  .menu-icon.open {
    background-color: transparent;
  }
  
  .menu-icon.open::before {
    transform: rotate(45deg);
    top: 0;
  }
  
  .menu-icon.open::after {
    transform: rotate(-45deg);
    bottom: 0;
  }
  
  /* Mobile Navigation */
  .mobile-nav {
    display: none;
    background-color: rgba(255, 255, 255, 0.95);
    padding: 0;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease, padding 0.3s ease;
  }
  
  .mobile-nav.open {
    max-height: 300px;
    padding: 1rem 2rem;
    border-top: 1px solid #eee;
  }
  
  .mobile-nav-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  
  .mobile-nav-item {
    margin: 1rem 0;
  }
  
  .mobile-nav-link {
    text-decoration: none;
    color: #555;
    font-family: 'Arial', sans-serif;
    font-size: 1rem;
    font-weight: 500;
    transition: color 0.3s;
    display: block;
    padding: 0.5rem 0;
  }
  
  .mobile-nav-link:hover,
  .mobile-nav-link.active {
    color: #9c8c61;
  }
  
  /* Main Content */
  .app-main {
    flex: 1;
    width: 100%;
    position: relative;
    z-index: 1;
  }
  
  /* Footer Styles */
  .app-footer {
    background-color: rgba(51, 51, 51, 0.95);
    color: #fff;
    padding: 3rem 2rem 1.5rem;
    margin-top: auto;
    position: relative;
    z-index: 1;
  }
  
  .footer-content {
    max-width: 1400px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
  }
  
  .footer-heading {
    font-family: 'Playfair Display', 'Georgia', serif;
    font-size: 1.2rem;
    margin-top: 0;
    margin-bottom: 1rem;
    color: #fff;
  }
  
  .footer-text {
    color: #ccc;
    line-height: 1.6;
    margin: 0;
  }
  
  .footer-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .footer-list li {
    margin-bottom: 0.5rem;
    color: #ccc;
  }
  
  .footer-link {
    color: #ccc;
    text-decoration: none;
    transition: color 0.3s;
  }
  
  .footer-link:hover {
    color: #9c8c61;
  }
  
  .footer-bottom {
    max-width: 1400px;
    margin: 2rem auto 0;
    padding-top: 1.5rem;
    border-top: 1px solid #444;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .copyright,
  .attribution {
    color: #999;
    font-size: 0.9rem;
    margin: 0;
  }
  
  /* Responsive Styles */
  @media (max-width: 768px) {
    .header-content {
      padding: 1rem;
    }
    
    .desktop-nav {
      display: none;
    }
    
    .mobile-menu-toggle {
      display: block;
    }
    
    .mobile-nav {
      display: block;
    }
    
    .footer-content {
      grid-template-columns: 1fr;
    }
    
    .footer-bottom {
      flex-direction: column;
      align-items: center;
      text-align: center;
    }
    
    .billionaire-silhouette {
      opacity: 0.08;
    }
  }
</style>