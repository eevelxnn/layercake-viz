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
    
    
    // Set loaded state for animations
    setTimeout(() => {
      isLoaded = true;
    }, 100);
    
  });
  

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