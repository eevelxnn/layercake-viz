<script>
  import { onMount } from 'svelte';
</script>

<div class="page-container">
  <h1 class="page-title">Conclusions</h1>
  <p class="subtitle">What we’ve learned from a decade of billionaire data</p>

  <div class="content">
    <p>
      From 2014 to 2024, the billionaire class didn’t just grow — it evolved. While the total number of billionaires surged from around <strong>1,600 to nearly 2,700</strong>, the share of self-made individuals has been consistently <strong>increasing<strong>. This suggests that entrepreneurship and innovation is becoming more and more of key wealth drivers.
    </p>

    <p>
      <strong>Technology emerged as the undisputed powerhouse</strong>, with more than 2,600 billionaires by 2024 — dwarfing every other sector. Industries like manufacturing, fashion, and real estate still hold ground but have not kept pace with tech’s explosive growth.
    </p>

        <p>
      They are also getting <strong>younger</strong> — with many crossing the billionaire threshold in their 30s and even 20s, particularly in fast-moving industries like tech and crypto. But this raises new questions about economic power, access, and sustainability in an increasingly unequal world.
    </p>


    <p>
      Despite the democratization of who can get rich, <strong>wealth inequality deepened</strong>. The number of billionaires expanded, but so did total wealth concentration, reinforcing the idea that new wealth doesn’t necessarily mean broader distribution.
    </p>

    <p>
      Geographically, billionaire wealth is still concentrated in the U.S. and China, but other nations — especially in Asia and the Middle East — are becoming more prominent players in this high-net-worth arena.
    </p>

    <p>
      The modern billionaire is <strong>more global, more self-made, and more tech-driven</strong> than a decade ago. But this also raises new questions about economic power, access, and sustainability in an increasingly unequal world.
    </p>
  </div>

  <div class="nav-buttons">
    <a href="/map" class="arrow-float left" aria-label="Back to map">← Back to Visualization</a>
    <a href="/intro" class="arrow-float right" aria-label="Next page"> Start Over →</a>
  </div>
</div>

<style>
  .page-container {
    max-width: 960px;
    margin: 2rem auto;
    padding: 0 1rem;
  }

  .page-title {
    font-size: 2.25rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.5rem;
  }

  .subtitle {
    font-size: 1.125rem;
    text-align: center;
    margin-bottom: 2rem;
    color: #555;
  }

  .content p {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1rem;
  }

  .content strong {
    color: #9b59b6;
  }

  .nav-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 3rem;
  }

  .arrow-float {
    font-size: 1rem;
    background: #f0f0f0;
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    text-decoration: none;
    color: #333;
    border: 1px solid #ccc;
    transition: background 0.2s ease;
  }

  .arrow-float:hover {
    background: #e2e2e2;
  }
</style>
