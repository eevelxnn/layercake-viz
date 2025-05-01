<script>
  import { LayerCake } from 'layercake';
  import CircleForce from '../_components/CircleForce.svelte';
  import raw from '../_data/billionaires_by_year.json';
  import { format } from 'd3-format';

let width = 3000;
let height = 3300;

  const years = Array.from(new Set(raw.map(d => d.year))).sort();
  const formatNumber = format(',d');
  const formatPercent = format('.1f');

  let year = 1997; // default year
  let data = [];
  let stats = { total: 0, selfMade: 0, inherited: 0, selfMadePercent: 0 };

  $: data = raw
    .filter(d => d.year === year && d.avg_net_worth > 0)
.map((d, i) => ({
  id: d.full_name,           
  key: `${d.full_name}-${i}`,
  value: d.avg_net_worth,
  self_made: d.self_made
}))

  $: {
    stats.total = data.length;
    stats.selfMade = data.filter(d => d.self_made).length;
    stats.inherited = stats.total - stats.selfMade;
    stats.selfMadePercent = (stats.selfMade / stats.total) * 100 || 0;
  }
</script>

<div class="container">
  <header>
    <h1>The Rise of Self-Made Billionaires</h1>
    <p class="subtitle">Exploring the changing landscape of wealth creation from {Math.min(...years)} to {Math.max(...years)}</p>
  </header>

  <div class="stats-container">
    <div class="stat-box">
      <span class="stat-value">{formatNumber(stats.total)}</span>
      <span class="stat-label">Total Billionaires</span>
    </div>
    <div class="stat-box self-made">
      <span class="stat-value">{formatNumber(stats.selfMade)}</span>
      <span class="stat-label">Self-Made</span>
    </div>
    <div class="stat-box inherited">
      <span class="stat-value">{formatNumber(stats.inherited)}</span>
      <span class="stat-label">Inherited Wealth</span>
    </div>
    <div class="stat-box">
      <span class="stat-value">{formatPercent(stats.selfMadePercent)}%</span>
      <span class="stat-label">Self-Made Percentage</span>
    </div>
  </div>

  <div class="year-control">
    <div class="year-label">
      <h2>{year}</h2>
      <p>Drag to change year</p>
    </div>
    <div class="slider-container">
      <input
        type="range"
        id="year"
        min={Math.min(...years)}
        max={Math.max(...years)}
        bind:value={year}
        step="1"
      />
      <div class="year-markers">
        {#each years.filter((_, i) => i % 5 === 0 || i === years.length - 1) as markerYear}
          <span class="year-marker" style="left: {((markerYear - Math.min(...years)) / (Math.max(...years) - Math.min(...years))) * 100}%">
            {markerYear}
          </span>
        {/each}
      </div>
    </div>
  </div>

  <div class="legend">
    <div class="legend-item">
      <span class="legend-color self-made-color"></span>
      <span>Self-Made Billionaires</span>
    </div>
    <div class="legend-item">
      <span class="legend-color inherited-color"></span>
      <span>Inherited Wealth</span>
    </div>
    <div class="legend-note">
      <span>Circle size represents net worth in billions</span>
    </div>
  </div>

  <div class="visualization">
    <LayerCake {width} {height} {data}>
      <CircleForce/>
    </LayerCake>
  </div>
</div>

<style>
  :global(body) {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
    color: #333;
    margin: 0;
    padding: 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }

  header {
    text-align: center;
    margin-bottom: 2rem;
  }

  h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    color: #2c3e50;
  }

  .subtitle {
    font-size: 1.1rem;
    color: #7f8c8d;
    margin-top: 0;
  }

  .stats-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .stat-box {
    background-color: white;
    border-radius: 8px;
    padding: 1rem;
    flex: 1;
    min-width: 150px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    text-align: center;
    display: flex;
    flex-direction: column;
    border-top: 4px solid #95a5a6;
  }

  .stat-box.self-made {
    border-top-color: #9b59b6;
  }

  .stat-box.inherited {
    border-top-color: #d3d3d3;
  }

  .stat-value {
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }

  .stat-label {
    font-size: 0.9rem;
    color: #7f8c8d;
  }

  .year-control {
    display: flex;
    align-items: center;
    margin-bottom: 2rem;
    background-color: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  }

  .year-label {
    width: 150px;
    margin-right: 2rem;
  }

  .year-label h2 {
    font-size: 2.5rem;
    margin: 0;
    color: #2c3e50;
  }

  .year-label p {
    margin: 0;
    color: #7f8c8d;
    font-size: 0.9rem;
  }

  .slider-container {
    flex: 1;
    position: relative;
  }

  input[type="range"] {
    width: 100%;
    height: 8px;
    -webkit-appearance: none;
    background: #ecf0f1;
    border-radius: 4px;
    outline: none;
    margin-bottom: 1.5rem;
  }

  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 20px;
    height: 20px;
    background: #3498db;
    border-radius: 50%;
    cursor: pointer;
    transition: background 0.15s ease;
  }

  input[type="range"]::-webkit-slider-thumb:hover {
    background: #2980b9;
  }

  .year-markers {
    position: relative;
    height: 20px;
  }

  .year-marker {
    position: absolute;
    transform: translateX(-50%);
    font-size: 0.8rem;
    color: #7f8c8d;
  }

  .legend {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    flex-wrap: wrap;
    gap: 1.5rem;
    background-color: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  }

  .legend-item {
    display: flex;
    align-items: center;
  }

  .legend-color {
    display: inline-block;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    margin-right: 8px;
  }

  .self-made-color {
    background-color: #9b59b6;
  }

  .inherited-color {
    background-color: #d3d3d3;
  }

  .legend-note {
    margin-left: auto;
    font-style: italic;
    color: #7f8c8d;
    font-size: 0.9rem;
  }

.visualization {
  background-color: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  width: 100%;
  height: 800px;
}

  @media (max-width: 768px) {
    .stats-container {
      flex-direction: column;
    }
    
    .year-control {
      flex-direction: column;
    }
    
    .year-label {
      width: 100%;
      margin-right: 0;
      margin-bottom: 1rem;
      text-align: center;
    }
    
    .legend {
      flex-direction: column;
      align-items: flex-start;
    }
    
    .legend-note {
      margin-left: 0;
      margin-top: 0.5rem;
    }
  }
.arrow-float {
  position: fixed;
  top: 50%;
  transform: translateY(-50%);
  font-size: 2.5rem;
  color: white;
  background-color: #2c3e50;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  text-decoration: none;
  z-index: 999;
  transition: background 0.2s ease;
}

.arrow-float:hover {
  background-color: #34495e;
}

.arrow-float.left {
  left: 20px;
}

.arrow-float.right {
  right: 20px;
}

</style>

<a href="/intro" class="arrow-float left" aria-label="Previous page">←</a>
<a href="/age-distribution" class="arrow-float right" aria-label="Next page">→</a>