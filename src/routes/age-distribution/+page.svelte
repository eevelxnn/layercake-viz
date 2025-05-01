<script>
 import { onMount } from 'svelte';
 import { scaleLinear } from 'd3-scale';
 import { max, min } from 'd3-array';
 import { format } from 'd3-format';
 import raw from '../_data/billionaire_ages.json';
 import CircleForce from '../_components/CircleForce.svelte';
 import { forceSimulation, forceX, forceY, forceCollide, forceManyBody } from 'd3-force';

 // raw & UI state
 let ageData = [];
 let years = [];
 let selectedYear = 2023;
 let isLoading = true;

 // dims & margins
 const margin = { top: 40, right: 30, bottom: 50, left: 60 };
 let width = 1000;
 let height = 500;
 let innerWidth, innerHeight;

 // age bins
 const minAge = 20;
 const maxAge = 100;
 const ageInterval = 10;

 // formatting
 const fmtCount = format(',d');
 const fmtWealth = format('$,.1f');

 // colors
 const selfMadeColor = '#9b59b6';
 const inheritedColor = '#d3d3d3';

 // scales
 let xScale, rScale;

 // stats summary
 let stats = {
  total: 0,
  selfMade: 0,
  inherited: 0,
  pctSelf: 0,
  youngest: 0,
  oldest: 0,
  median: 0,
  totalWealth: 0
 };

 // filtered data for current year
 let filtered = [];
 let forceData = [];

 // tooltip state
 let tooltip = null;
 let tooltipX = 0;
 let tooltipY = 0;

 // slider ticks
 $: ageTicks = Array.from(
  { length: Math.floor((maxAge - minAge) / ageInterval) + 1 },
  (_, i) => minAge + i * ageInterval
 );

 let nodes = [];
 let simulation;

 onMount(() => {
  ageData = raw;
  years = [...new Set(ageData.map(d => d.year))].sort();
  if (years.length) selectedYear = years[years.length - 1];
  updateVis();
  isLoading = false;
 });

 function updateVis() {
  filtered = ageData.filter(d => d.year === selectedYear);
  innerWidth = width - margin.left - margin.right;
  innerHeight = height - margin.top - margin.bottom;

  // horizontal scale: age → x
  xScale = scaleLinear()
   .domain([minAge, maxAge])
   .range([margin.left, width - margin.right]);

  // radius scale: total_wealth → r
  const maxW = max(filtered, d => d.total_wealth) || 1;
  rScale = scaleLinear().domain([0, maxW]).range([3, 20]);

  computeStats();

  // --- FORCE SIMULATION SETUP ---
  // Initialize nodes with x/y positions
  nodes = filtered.map((d, i) => ({
    ...d,
    x: xScale(d.age),
    y: margin.top + innerHeight / 2 + (Math.random() - 0.5) * 40, // start near center
    r: rScale(d.total_wealth)
  }));

  // Stop previous simulation if any
  if (simulation) simulation.stop();

  // Set up d3-force simulation
  simulation = forceSimulation(nodes)
    .force('x', forceX(d => xScale(d.age)).strength(0.2))
    .force('y', forceY(d => d.self_made_count > 0 ? height / 3 : (height * 2) / 3).strength(0.15))
    .force('collide', forceCollide(d => d.r + 1).strength(1))
    .force('charge', forceManyBody().strength(2)) // mild attraction
    .alpha(0.7)
    .alphaDecay(0.03)
    .on('tick', () => {
      // Svelte will reactively update the DOM
      nodes = [...nodes];
    });
 }

 function computeStats() {
  if (!filtered.length) {
   stats = {
    total: 0,
    selfMade: 0,
    inherited: 0,
    pctSelf: 0,
    youngest: 0,
    oldest: 0,
    median: 0,
    totalWealth: 0
   };
   return;
  }
  const sm = filtered.reduce((s, d) => s + d.self_made_count, 0);
  const inh = filtered.reduce((s, d) => s + d.inherited_count, 0);
  const tot = sm + inh;
  const tw = filtered.reduce((s, d) => s + d.total_wealth, 0);
  const ages = filtered.map(d => d.age);
  const youngest = min(ages),
   oldest = max(ages);

  // build expanded list for median
  const all = [];
  filtered.forEach(d => {
   for (let i = 0; i < d.total_count; i++) all.push(d.age);
  });
  all.sort((a, b) => a - b);
  const mid = Math.floor(all.length / 2);
  const median = all.length % 2 === 0 ? (all[mid - 1] + all[mid]) / 2 : all[mid];

  stats = {
   total: tot,
   selfMade: sm,
   inherited: inh,
   pctSelf: tot ? (sm / tot) * 100 : 0,
   youngest,
   oldest,
   median,
   totalWealth: tw
  };
 }

 function onYear(e) {
  selectedYear = +e.target.value;
  updateVis();
 }

 // tooltip handlers
 function showTooltip(d, e) {
  tooltip = d;
  updateTooltipPosition(e);
 }
 function hideTooltip() {
  tooltip = null;
 }
 function updateTooltipPosition(e) {
  tooltipX = e.clientX + 10;
  tooltipY = e.clientY + 10;
 }
</script>

<div class="age-distribution-page">
 <header class="page-header">
  <h1>Billionaire Age Distribution</h1>
  <p class="subtitle">Wealth vs. age for {selectedYear}</p >
 </header>

 {#if isLoading}
  <div class="loading"><p>Loading age distribution data...</p ></div>
 {:else}


  <div class="stats-cards">
   <div class="stat-card">
    <h3>Total:</h3>
    <p class="stat-value">{fmtCount(stats.total)}</p >
   </div>
   <div class="stat-card self-made">
    <h3>Self-Made:</h3>
    <p class="stat-value">{fmtCount(stats.selfMade)} ({stats.pctSelf.toFixed(1)}%)</p >
   </div>
   <div class="stat-card inherited">
    <h3>Inherited:</h3>
    <p class="stat-value">{fmtCount(stats.inherited)}</p >
   </div>
   <div class="stat-card">
    <h3>Age Range:</h3>
    <p class="stat-value">{stats.youngest} – {stats.oldest}</p >
    <p class="stat-subtitle">Median: {stats.median}</p >
   </div>
   <div class="stat-card">
    <h3>Total Wealth:</h3>
    <p class="stat-value">{fmtWealth(stats.totalWealth)}B</p >
   </div>
  </div>

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
    {#each ageTicks as t}
     <line
      x1={xScale(t)}
      x2={xScale(t)}
      y1={margin.top}
      y2={height - margin.bottom}
      class="grid-line"
     />
     <text
      x={xScale(t)}
      y={height - margin.bottom + 20}
      text-anchor="middle"
      class="axis-label">{t}</text
     >
    {/each}

    {#each nodes as d (d.year + '-' + d.age + '-' + d.total_wealth)}
     <circle
      cx={d.x}
      cy={d.y}
      r={d.r}
      fill={d.self_made_count > 0 ? selfMadeColor : inheritedColor}
      stroke="#fff"
      stroke-width="1"
      on:mouseenter={e => showTooltip(d, e)}
      on:mousemove={updateTooltipPosition}
      on:mouseleave={hideTooltip}
     />
    {/each}
   </svg>

   {#if tooltip}
    <div class="tooltip" style="top: {tooltipY}px; left: {tooltipX}px;">
     <strong>Age: {tooltip.age}</strong><br />
     {#if tooltip.self_made_count > 0}
      <span class="tooltip-label">Self-Made:</span>
      {tooltip.self_made_count}<br />
      <span class="tooltip-label">Wealth:</span>
      {fmtWealth(tooltip.self_made_wealth)}B
     {:else}
      <span class="tooltip-label">Inherited:</span>
      {tooltip.inherited_count}<br />
      <span class="tooltip-label">Wealth:</span>
      {fmtWealth(tooltip.inherited_wealth)}B
     {/if}
    </div>
   {/if}
  </div>
 {/if}
</div>

<a href=" " class="arrow-float left" aria-label="Previous page">←</a >
<a href="/industry" class="arrow-float right" aria-label="Next page">→</a >

<style>
 .age-distribution-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
 }

 .page-header {
  text-align: center;
  margin-bottom: 2rem;
 }

 h1 {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #333;
 }

 .subtitle {
  font-size: 1.1rem;
  color: #666;
  max-width: 800px;
  margin: 0 auto;
 }

 .loading,
 .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
 }

 .error {
  color: #d62728;
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
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #666;
 }

 .stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
 }

 .stat-card {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  text-align: center;
  border-top: 4px solid #95a5a6;
 }

 .stat-card.self-made {
  border-top-color: #9b59b6;
 }

 .stat-card.inherited {
  border-top-color: #d3d3d3;
 }

 .stat-card h3 {
  font-size: 1rem;
  color: #666;
  margin-bottom: 0.5rem;
  font-weight: normal;
 }

 .stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  margin: 0;
 }

 .stat-subtitle {
  font-size: 1rem;
  color: #666;
  margin: 0.5rem 0 0;
 }

 .chart-container {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: relative;
 }

 svg {
  width: 100%;
  height: 100%;
  display: block;
 }

 .grid-line {
  stroke: #eee;
  stroke-width: 1;
 }

 .axis-label {
  font-size: 12px;
  fill: #666;
 }

 .tooltip {
  position: fixed;
  background: white;
  color: black;
  padding: 8px 12px;
  font-size: 13px;
  border: 1px solid #ccc;
  border-radius: 6px;
  pointer-events: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  max-width: 250px;
 }

 .tooltip-label {
  color: #666;
 }

 @media (max-width: 768px) {
  .age-distribution-page {
   padding: 1rem;
  }

  h1 {
   font-size: 2rem;
  }

  .stats-cards {
   grid-template-columns: 1fr;
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
<a href="/self-made-trend" class="arrow-float left" aria-label="Previous page">←</a>
<a href="/industry" class="arrow-float right" aria-label="Home">→</a>