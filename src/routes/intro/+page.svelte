<script>
  import { onMount } from 'svelte';
  
  let isLoaded = false;
  let animationComplete = false;
  
  onMount(() => {
    isLoaded = true;
    setTimeout(() => {
      animationComplete = true;
    }, 2000);
  });

  // Billionaire silhouettes for background
  const billionaires = [
    { top: '10%', left: '5%', size: '180px', rotation: '-5deg' },
    { top: '15%', left: '75%', size: '220px', rotation: '8deg' },
    { top: '60%', left: '15%', size: '200px', rotation: '3deg' },
    { top: '50%', left: '85%', size: '190px', rotation: '-7deg' },
    { top: '80%', left: '60%', size: '210px', rotation: '5deg' },
    { top: '30%', left: '40%', size: '170px', rotation: '-3deg' },
  ];
</script>

<div class="intro-container" class:loaded={isLoaded}>
  <div class="background-overlay"></div>
  
  <!-- Billionaire silhouettes -->
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
  
  <div class="content">
    <div class="title-section">
      <h1 class="main-title">
        <span class="title-word">SELF</span>
        <span class="title-separator">—</span>
        <span class="title-word">MADE?</span>
      </h1>
      
      <p class="subtitle">
        Examining the reality behind wealth creation: 
        <span class="highlight">Are billionaires truly self-made or beneficiaries of privilege?</span>
      </p>
    </div>
    
    <div class="visual-element">
      <div class="divider">
        <div class="divider-line"></div>
        <div class="divider-icon">$</div>
        <div class="divider-line"></div>
      </div>
    </div>
    
    <div class="cta-section" class:visible={animationComplete}>
      <p class="cta-text">An evidence-based analysis of wealth accumulation patterns among the world's economic elite</p>
      <a href="/self-made-trend" class="cta-button">View Analysis</a>
    </div>
    
    <div class="team-section">
      <p class="team-intro">Research & Visualization by</p>
      <div class="team-names">
        <span class="team-member">Evelyn Martinez</span>
        <span class="team-divider">•</span>
        <span class="team-member">Jeremiah Xu</span>
        <span class="team-divider">•</span>
        <span class="team-member">Haiyue Zhang</span>
        <span class="team-divider">•</span>
        <span class="team-member">Benny Yang</span>
      </div>
    </div>
  </div>
  
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f5f5f5;
    color: #333;
    overflow-x: hidden;
  }
  
  .intro-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 2rem;
    box-sizing: border-box;
    position: relative;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 1s ease, transform 1s ease;
    background-color: #f5f5f5;
  }
  
  .intro-container.loaded {
    opacity: 1;
    transform: translateY(0);
  }
  

  
  .billionaire-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
  }
  
  .billionaire-silhouette {
    position: absolute;
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
  
  .content {
    max-width: 1200px;
    width: 100%;
    text-align: center;
    position: relative;
    z-index: 2;
  }
  
  .title-section {
    margin-bottom: 3rem;
  }
  
  .main-title {
    font-size: 5.5rem;
    font-weight: 900;
    margin: 0 0 1rem;
    line-height: 1;
    letter-spacing: -0.02em;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    color: #333;
  }
  
  .title-word {
    display: inline-block;
    position: relative;
  }
  
  .title-separator {
    margin: 0 1rem;
    color: #9c8c61;
  }
  
  .subtitle {
    font-size: 1.5rem;
    font-weight: 400;
    max-width: 800px;
    margin: 0 auto;
    color: #555;
    line-height: 1.5;
    font-family: 'Georgia', serif;
  }
  
  .highlight {
    color: #333;
    font-weight: 500;
    position: relative;
    display: inline-block;
  }
  
  .highlight::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 1px;
    background-color: #9c8c61;
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.5s ease;
  }
  
  .intro-container.loaded .highlight::after {
    transform: scaleX(1);
  }
  
  .visual-element {
    margin: 4rem 0;
    height: 50px;
    position: relative;
  }
  
  .divider {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
  }
  
  .divider-line {
    height: 1px;
    background-color: #9c8c61;
    flex-grow: 1;
    max-width: 200px;
    opacity: 0;
    transform: scaleX(0);
    transition: transform 1s ease, opacity 1s ease;
    transition-delay: 0.5s;
  }
  
  .intro-container.loaded .divider-line {
    opacity: 1;
    transform: scaleX(1);
  }
  
  .divider-icon {
    font-size: 2rem;
    color: #9c8c61;
    margin: 0 2rem;
    font-weight: 700;
    opacity: 0;
    transform: translateY(20px);
    transition: transform 1s ease, opacity 1s ease;
    transition-delay: 0.8s;
  }
  
  .intro-container.loaded .divider-icon {
    opacity: 1;
    transform: translateY(0);
  }
  
  .cta-section {
    margin: 2rem 0 4rem;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 1s ease, transform 1s ease;
  }
  
  .cta-section.visible {
    opacity: 1;
    transform: translateY(0);
  }
  
  .cta-text {
    font-size: 1.2rem;
    color: #555;
    margin-bottom: 2rem;
    font-family: 'Georgia', serif;
    font-style: italic;
  }
  
  .cta-button {
    display: inline-block;
    padding: 1rem 2.5rem;
    background-color: #333;
    color: #fff;
    border: none;
    border-radius: 2px;
    font-size: 1rem;
    font-weight: 600;
    text-decoration: none;
    transition: background-color 0.3s ease, transform 0.3s ease;
    font-family: 'Arial', sans-serif;
    letter-spacing: 1px;
  }
  
  .cta-button:hover {
    background-color: #555;
    transform: translateY(-2px);
  }
  
  .team-section {
    margin-top: 4rem;
  }
  
  .team-intro {
    font-size: 1rem;
    color: #777;
    margin-bottom: 0.5rem;
    font-family: 'Georgia', serif;
  }
  
  .team-names {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .team-member {
    color: #333;
    font-weight: 500;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  
  .team-divider {
    color: #9c8c61;
  }
  
  .arrow-float {
    position: fixed;
    top: 50%;
    transform: translateY(-50%);
    font-size: 2.5rem;
    color: white;
    background-color: #333;
    padding: 0.75rem 1rem;
    border-radius: 2px;
    text-decoration: none;
    z-index: 999;
    transition: background 0.2s ease;
  }

  .arrow-float:hover {
    background-color: #555;
  }

  .arrow-float.left {
    left: 20px;
  }

  .arrow-float.right {
    right: 20px;
  }
  
  @media (max-width: 768px) {
    .main-title {
      font-size: 3.5rem;
    }
    
    .subtitle {
      font-size: 1.2rem;
    }
    
    .team-names {
      flex-direction: column;
      align-items: center;
    }
    
    .team-divider {
      display: none;
    }
    
.billionaire-silhouette {
  position: absolute;
  opacity: 0.2;
  filter: grayscale(100%);
  overflow: hidden;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
  }
</style>

