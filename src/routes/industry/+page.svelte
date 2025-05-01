<script>
  import { onMount } from 'svelte';
  import { scaleLinear, scaleBand } from 'd3-scale';
  import { max } from 'd3-array';
  import { format } from 'd3-format';
  import { forceSimulation, forceX, forceY, forceCollide, forceManyBody } from 'd3-force';
  import raw from '../_data/industry_wealth.json';

  // Layout and state
  const margin = { top: 40, right: 30, bottom: 50, left: 60 };
  let width = 1000;
  let height = 600;
  let years = [];
  let selectedYear = 2023;
  let isLoading = true;

  // Industry setup
  let industryColors = {};
  function getRandomColor() {
    // Generate a pastel random color
    const hue = Math.floor(Math.random() * 360);
    return `hsl(${hue}, 60%, 60%)`;
  }
  let topIndustries = [];
  let industryScale, rScale;
  let filtered = [];
  let nodes = [];
  let simulation;

  // Formatting
  const fmtWealth = format('$,.1f');

  onMount(() => {
    // Get all years and top 10 industries by total wealth
    years = [...new Set(raw.map(d => d.year))].sort();
    if (years.length) selectedYear = years[years.length - 1];

    // Find top 10 industries by max value across all years
    const industryTotals = {};
    raw.forEach(d => {
      Object.keys(d).forEach(k => {
        if (k !== 'year' && k !== 'filter') {
          industryTotals[k] = (industryTotals[k] || 0) + (d[k] || 0);
        }
      });
    });
    topIndustries = Object.entries(industryTotals)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([k]) => k);

    // Assign a color to each industry if not already present
    topIndustries.forEach(ind => {
      if (!industryColors[ind.replace(/[\[\]']/g, '').trim()]) {
        industryColors[ind.replace(/[\[\]']/g, '').trim()] = getRandomColor();
      }
    });

    updateVis();
    isLoading = false;
  });

  function updateVis() {
    filtered = raw.filter(d => d.year === selectedYear && d.filter === 'all');
    // Flatten to one array of {industry, value} for each billionaire
    let allCircles = [];
    // Assume you have a data source with individual billionaires and their industry/wealth for the selected year
    // If not, this is a placeholder for how you would do it if you had such data
    // For now, we will simulate with synthetic individuals proportional to wealth, but with much smaller radii
    topIndustries.forEach((industry, i) => {
      const val = filtered[0]?.[industry] || 0;
      // Simulate: 1 circle per 1B, min 1
      const count = Math.max(1, Math.round(val));
      for (let j = 0; j < count; j++) {
        allCircles.push({
          industry,
          value: 1, // Each person is 1B for this simulation
          color: industryColors[industry.replace(/[\[\]']/g, '').trim()] || '#ccc',
          key: `${industry}-${j}`
        });
      }
    });

    // Scales
    industryScale = scaleBand()
      .domain(topIndustries)
      .range([margin.left, width - margin.right])
      .padding(0.1);

    const maxVal = max(allCircles, d => d.value) || 1;
    // Make all circles 10x smaller than before
    rScale = scaleLinear().domain([0, maxVal]).range([0.5, 3]);

    // Force simulation
    nodes = allCircles.map(d => ({
      ...d,
      x: industryScale(d.industry) + industryScale.bandwidth() / 2 + (Math.random() - 0.5) * industryScale.bandwidth() * 0.6,
      y: margin.top + Math.random() * (height - margin.top - margin.bottom),
      r: rScale(d.value)
    }));

    if (simulation) simulation.stop();
    simulation = forceSimulation(nodes)
      // Strongly attract nodes to their industry center (clusters same industry)
      .force('x', forceX(d => industryScale(d.industry) + industryScale.bandwidth() / 2).strength(0.5))
      .force('y', forceY(height / 2).strength(0.05))
      .force('collide', forceCollide(d => d.r + 1).strength(1))
      // Much weaker repulsive force (reduce by 1000%)
      .force('repulse', forceManyBody().strength(-0.03))
      .alpha(0.7)
      .alphaDecay(0.03)
      .on('tick', () => {
        nodes = [...nodes];
      });
  }

  function onYear(e) {
    selectedYear = +e.target.value;
    updateVis();
  }
</script>

<div class="container">
  <header>
    <h1>Industry Wealth Distribution</h1>
    <p class="subtitle">How industry composition of billionaire wealth has evolved over time</p>
  </header>

  <div class="controls-container">
    <div class="year-slider">
      <div class="year-display">
        <span>Selected Year: <strong>{selectedYear}</strong></span>
      </div>
      <input
        type="range"
        min={Math.min(...years)}
        max={Math.max(...years)}
        bind:value={selectedYear}
        on:input={onYear}
        class="timeline-slider"
      />
      <div class="year-labels">
        <span>{Math.min(...years)}</span>
        <span>{Math.max(...years)}</span>
      </div>
    </div>
  </div>

  <div class="chart-container">
    <svg {width} {height}>
      {#each topIndustries as industry, i}
        {#if i > 0}
          <line
            x1={industryScale(industry)}
            x2={industryScale(industry)}
            y1={margin.top}
            y2={height - margin.bottom}
            stroke="#eee"
            stroke-width="1"
            stroke-dasharray="4,2"
            class="industry-separator"
          />
        {/if}
        <line
          x1={industryScale(industry) + industryScale.bandwidth() / 2}
          x2={industryScale(industry) + industryScale.bandwidth() / 2}
          y1={margin.top}
          y2={height - margin.bottom}
          class="grid-line"
        />
      {/each}

      {#each nodes as d (d.key)}
        <circle
          cx={d.x}
          cy={d.y}
          r={d.r}
          fill={d.color}
          stroke="#fff"
          stroke-width="1"
        />
      {/each}
    </svg>
  </div>

  <div class="chart-legend">
    {#each topIndustries as industry}
      <div class="legend-item">
        <span class="legend-color" style="background-color: {industryColors[industry.replace(/[\[\]']/g, '').trim()] || '#ccc'};"></span>
        <span class="legend-label">{industry.replace(/\\[|\\]|'/g, '')}</span>
      </div>
    {/each}
  </div>
</div>

<style>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
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

  .controls-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
 }

 .year-slider {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
 }

 .year-display {
  font-size: 1.2rem;
  text-align: center;
  margin-bottom: 0.5rem;
 }

 .timeline-slider {
  width: 100%;
  height: 8px;
  -webkit-appearance: none;
  appearance: none;
  background: #ddd;
  outline: none;
  border-radius: 4px;
  cursor: pointer;
 }

 .timeline-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: #9c8c61;
  border-radius: 50%;
  cursor: pointer;
 }

 .timeline-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: #9c8c61;
  border-radius: 50%;
  cursor: pointer;
  border: none;
 }

  .year-labels {
    position: absolute;
    top: 100%;
    left: 10px;
    right: 10px;
    text-align: center;
    font-size: 0.8rem;
    color: #7f8c8d;
  }

  .chart-container {
    background-color: white;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    overflow: hidden;
    width: 100%;
    height: 600px;
  }

  .chart-legend {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
    margin-top: 2rem;
  }

  .legend-item {
    display: flex;
    align-items: center;
    font-size: 0.9rem;
  }

  .legend-color {
    display: inline-block;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    margin-right: 8px;
  }

  .tooltip {
    position: fixed;
    background-color: white;
    padding: 0.75rem 1rem;
    border-radius: 6px;
    font-size: 0.9rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    z-index: 1000;
    pointer-events: none;
    max-width: 250px;
  }

  @media (max-width: 768px) {
    .chart-container {
      height: 400px;
    }

    .legend-item {
      font-size: 0.8rem;
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

<a href="/age-distribution" class="arrow-float left" aria-label="Previous page">←</a>
<a href="/map" class="arrow-float right" aria-label="Next page">→</a>