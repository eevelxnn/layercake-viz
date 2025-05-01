<script>
 import { onMount } from 'svelte';
 import { scaleLinear } from 'd3-scale';
 import { extent, max, min } from 'd3-array';
 import { format } from 'd3-format';
 import raw from '../_data/billionaire_ages.json';
 import CircleForce from '../_components/CircleForce.svelte';
 import { LayerCake } from 'layercake';

 // raw & UI state
 let ageData = [];
 let years = [];
 let selectedYear = 2023;
 let isLoading = true;
 let error = null;

 // dims & margins
 const margin = { top: 40, right: 30, bottom: 50, left: 60 };
 let width = 1000;
 let height = 500;
 let innerWidth;
 let innerHeight;

 // bins
 const minAge = 20;
 const maxAge = 100;
 const ageInterval = 10;

 // formatting
 const formatNumber = format(',d');
 const formatBillion = format('$,.1f');

 // colors
 const selfMadeColor = '#9b59b6';
 const inheritedColor = '#d3d3d3';

 // scales & data for the force layout
 let xScale; // horizontal (age) axis
 let rScale; // circle radius
 let forceData = [];

 // for tooltips
 let tooltip = null;
 let tooltipX = 0;
 let tooltipY = 0;

 // stats summary
 let stats = {
  totalBillionaires: 0,
  selfMade: 0,
  inherited: 0,
  selfMadePercent: 0,
  youngestAge: 0,
  oldestAge: 0,
  medianAge: 0,
  totalWealth: 0
 };

 // recomputed slice
 let filteredData = [];

 // slider ticks
 $: ageTicks = Array.from(
  { length: Math.floor((maxAge - minAge) / ageInterval) + 1 },
  (_, i) => minAge + i * ageInterval
 );

 onMount(() => {
  ageData = raw;
  years = [...new Set(ageData.map(d => d.year))].sort();
  if (years.length) selectedYear = years[years.length - 1];
  updateVisualization();
  isLoading = false;
 });

 function updateVisualization() {
  filteredData = ageData.filter(d => d.year === selectedYear);

  innerWidth = width - margin.left - margin.right;
  innerHeight = height - margin.top - margin.bottom;

  // 1) xScale from minAge → maxAge
  xScale = scaleLinear()
   .domain([minAge, maxAge])
   .range([margin.left, width - margin.right]);

  // 2) radius scale based on total_wealth
  const maxW = max(filteredData, d => d.total_wealth) || 100;
  rScale = scaleLinear().domain([0, maxW]).range([5, 30]);

  // 3) build the forceData array
  forceData = filteredData.map((d, i) => ({
    ...d,
    id: `${selectedYear}-${d.age}-${i}`,
    value: rScale(d.total_wealth),
    color: d.self_made_count > 0 ? selfMadeColor : inheritedColor
  }));


  updateStats();
 }

 function updateStats() {
  if (!filteredData.length) {
   stats = {
    totalBillionaires: 0,
    selfMade: 0,
    inherited: 0,
    selfMadePercent: 0,
    youngestAge: 0,
    oldestAge: 0,
    medianAge: 0,
    totalWealth: 0
   };
   return;
  }

  const selfMadeCount = filteredData.reduce((sum, d) => sum + d.self_made_count, 0);
  const inheritedCount = filteredData.reduce((sum, d) => sum + d.inherited_count, 0);
  const totalCount = selfMadeCount + inheritedCount;
  const totalWealth = filteredData.reduce((sum, d) => sum + d.total_wealth, 0);

  const ages = filteredData.map(d => d.age);
  const youngestAge = min(ages);
  const oldestAge = max(ages);

  // median by expanding each age by its total_count
  let allAges = [];
  filteredData.forEach(d =>
   Array(d.total_count)
    .fill(d.age)
    .forEach(a => allAges.push(a))
  );
  allAges.sort((a, b) => a - b);
  const mid = Math.floor(allAges.length / 2);
  const medianAge =
   allAges.length % 2 === 0 ? (allAges[mid - 1] + allAges[mid]) / 2 : allAges[mid];

  stats = {
   totalBillionaires: totalCount,
   selfMade: selfMadeCount,
   inherited: inheritedCount,
   selfMadePercent: totalCount ? (selfMadeCount / totalCount) * 100 : 0,
   youngestAge,
   oldestAge,
   medianAge,
   totalWealth
  };
 }

 function handleYearChange(e) {
  selectedYear = +e.target.value;
  updateVisualization();
 }

 function handleMouseMove(e) {
  tooltipX = e.clientX + 12;
  tooltipY = e.clientY + 12;
 }
 function showTooltip(d) {
  tooltip = d;
 }
 function hideTooltip() {
  tooltip = null;
 }

 // recalc on resize
 $: if (!isLoading) updateVisualization();
</script>

<div class="age-distribution-page">
 <header class="page-header">
  <h1>Billionaire Age Distribution</h1>
  <p class="subtitle">Exploring how wealth is distributed across different age groups</p >
 </header>

 {#if isLoading}
  <div class="loading"><p>Loading age distribution data...</p ></div>
 {:else if error}
  <div class="error"><p>{error}</p ></div>
 {:else}
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
     on:input={handleYearChange}
     class="timeline-slider"
    />
    <div class="year-labels">
     <span>{Math.min(...years)}</span>
     <span>{Math.max(...years)}</span>
    </div>
   </div>
  </div>

  <div class="stats-cards">
   <div class="stat-card">
    <h3>Total Billionaires</h3>
    <p class="stat-value">{formatNumber(stats.totalBillionaires)}</p >
   </div>
   <div class="stat-card self-made">
    <h3>Self-Made</h3>
    <p class="stat-value">
     {formatNumber(stats.selfMade)} ({stats.selfMadePercent.toFixed(1)}%)
    </p >
   </div>
   <div class="stat-card inherited">
    <h3>Inherited Wealth</h3>
    <p class="stat-value">{formatNumber(stats.inherited)}</p >
   </div>
   <div class="stat-card">
    <h3>Age Range</h3>
    <p class="stat-value">{stats.youngestAge} – {stats.oldestAge}</p >
    <p class="stat-subtitle">Median: {stats.medianAge}</p >
   </div>
   <div class="stat-card">
    <h3>Total Wealth</h3>
    <p class="stat-value">{formatBillion(stats.totalWealth)}B</p >
   </div>
  </div>

  <div class="chart-container" on:mousemove={handleMouseMove}>
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
     <span>Circle size represents total wealth in billions</span>
    </div>
   </div>

   <svg {width} {height}>
    {#each ageTicks as tick}
     <line
      x1={xScale(tick)}
      x2={xScale(tick)}
      y1={margin.top}
      y2={height - margin.bottom}
      class="grid-line"
     />
     <text
      x={xScale(tick)}
      y={height - margin.bottom + 20}
      text-anchor="middle"
      class="axis-label">{tick}</text
     >
    {/each}
   </svg>

   <LayerCake {width} {height} data={forceData}>
    <CircleForce
      key={selectedYear}
      valueKey="value"
      idKey="id"
      manyBodyStrength={-10}
      nodeStroke="#fff"
      nodeStrokeWidth={2}
      getColor={d => d.color}
      {rScale}
      xGet={d => d.x}
      yGet={d => d.y}
    />
   </LayerCake>

   {#if tooltip}
    <div class="tooltip" style="top:{tooltipY}px; left:{tooltipX}px">
     <strong>Age: {tooltip.age}</strong><br />
     {#if tooltip.self_made_count > 0}
      <span class="tooltip-label">Self-Made:</span>
      {tooltip.self_made_count}<br />
      <span class="tooltip-label">Wealth:</span>
      {formatBillion(tooltip.self_made_wealth)}B
     {:else}
      <span class="tooltip-label">Inherited:</span>
      {tooltip.inherited_count}<br />
      <span class="tooltip-label">Wealth:</span>
      {formatBillion(tooltip.inherited_wealth)}B
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
  font-family: 'Arial', sans-serif;
 }

 .page-header {
  text-align: center;
  margin-bottom: 2rem;
 }

 h1 {
  font-family: 'Playfair Display', 'Georgia', serif;
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

 .legend {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1.5rem;
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

 .axis-title {
  font-size: 14px;
  fill: #333;
  font-weight: bold;
 }

 .section-label {
  font-size: 14px;
  font-weight: bold;
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