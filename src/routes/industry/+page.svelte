<script>
  import { onMount } from 'svelte';
  import { LayerCake, Svg } from 'layercake';
  import { stack } from 'd3-shape';
  import { scaleLinear, scaleTime, scaleOrdinal } from 'd3-scale';
  import { extent, max, sum } from 'd3-array';
  import { format } from 'd3-format';
  import { timeParse, timeFormat } from 'd3-time-format';
  import Area from '../_components/Area.svelte';
  import AxisX from '../_components/AxisX.svelte';
  import AxisY from '../_components/AxisY.svelte';
  import * as d3 from 'd3';
  
  // Data loading and processing
  let industryData = [];
  let years = [];
  let selectedYear = 2023;
  let selectedFilter = 'all'; // 'all', 'self-made', 'inherited'
  let isLoading = true;
  let error = null;
  
  // Industry colors - using a rich color palette
  const industryColors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
  ];
  
  // Format functions
  const formatMoney = format('$,.1f');
  const formatPercent = format('.1%');
  const parseYear = timeParse('%Y');
  const formatYear = timeFormat('%Y');
  
  // Stats for the selected year
  let totalWealth = 0;
  let wealthiestIndustry = '';
  let wealthiestIndustryPercentage = 0;
  
  // Variables for stacked area chart
  let series = [];
  let flatData = [];
  let industryKeys = [];
  let allData = [];
  
  onMount(async () => {
    try {
      // Load the preprocessed industry data
      const response = await fetch('/src/routes/_data/industry_wealth.json');
      allData = await response.json();
      
      // Get unique years
      years = [...new Set(allData.map(d => d.year))].sort();
      
      // Get industry keys (removing the year and filter keys)
      const firstItem = allData[0];
      industryKeys = Object.keys(firstItem).filter(key => 
        key !== 'year' && key !== 'filter'
      );
      
      // Clean up industry names (remove brackets and quotes)
      industryKeys = industryKeys.map(key => {
        return key.replace(/[\[\]']/g, '');
      });
      
      // Process data for visualization
      updateDataForFilter();
      
      isLoading = false;
    } catch (err) {
      console.error('Error loading data:', err);
      error = 'Failed to load industry data. Please try again later.';
      isLoading = false;
    }
  });
  
  function updateDataForFilter() {
    // Filter data for the selected filter
    industryData = allData.filter(d => d.filter === selectedFilter);
    
    // Prepare data for stacked area chart
    prepareStackedData();
    
    // Update stats for selected year
    updateYearStats();
  }
  
  function prepareStackedData() {
    if (industryData.length === 0 || industryKeys.length === 0) {
      series = [];
      flatData = [];
      return;
    }
    
    // Clean up the data for stacking
    const cleanData = industryData.map(d => {
      const cleanItem = { year: d.year };
      
      // Process each industry key
      industryKeys.forEach(key => {
        // Find the corresponding key in the original data
        const originalKey = Object.keys(d).find(k => k.includes(key));
        if (originalKey) {
          cleanItem[key] = d[originalKey];
        } else {
          cleanItem[key] = 0;
        }
      });
      
      return cleanItem;
    });
    
    // Create stack generator
    const stackGen = stack()
      .keys(industryKeys)
      .order(d3.stackOrderNone)
      .offset(d3.stackOffsetNone);
    
    // Generate stacked series
    series = stackGen(cleanData);
    
    // Flatten the stacked data for LayerCake
    flatData = [];
    series.forEach((s, i) => {
      const industryName = s.key;
      s.forEach((d, j) => {
        flatData.push({
          industry: industryName,
          year: cleanData[j].year,
          value: d[1] - d[0],
          y0: d[0],
          y1: d[1]
        });
      });
    });
  }
  
  function updateYearStats() {
    const yearData = industryData.find(d => d.year === selectedYear);
    
    if (yearData) {
      // Calculate total wealth for the year
      totalWealth = Object.entries(yearData)
        .filter(([key]) => key !== 'year' && key !== 'filter')
        .reduce((sum, [_, value]) => sum + value, 0);
      
      // Find wealthiest industry
      const wealthiestEntry = Object.entries(yearData)
        .filter(([key]) => key !== 'year' && key !== 'filter')
        .sort((a, b) => b[1] - a[1])[0];
      
      if (wealthiestEntry) {
        // Clean up industry name
        wealthiestIndustry = wealthiestEntry[0].replace(/[\[\]']/g, '');
        wealthiestIndustryPercentage = wealthiestEntry[1] / totalWealth;
      } else {
        wealthiestIndustry = 'N/A';
        wealthiestIndustryPercentage = 0;
      }
    }
  }
  
  function handleYearChange(event) {
    selectedYear = parseInt(event.target.value);
    updateYearStats();
  }
  
  function handleFilterChange(filter) {
    selectedFilter = filter;
    updateDataForFilter();
  }
</script>

<div class="industry-page">
  <header class="page-header">
    <h1>Billionaire Wealth by Industry</h1>
    <p class="subtitle">Exploring how wealth is distributed across the top industries from 1997 to 2024</p>
  </header>

    <div class="controls-container">
      <div class="year-slider">
        <div class="year-display">
          <span>Selected Year: <strong>{selectedYear}</strong></span>
        </div>
        <input 
          type="range" 
          min="{Math.min(...years)}" 
          max="{Math.max(...years)}" 
          value="{selectedYear}" 
          on:input={handleYearChange}
          class="timeline-slider"
        />
        <div class="year-labels">
          <span>{Math.min(...years)}</span>
          <span>{Math.max(...years)}</span>
        </div>
      </div>
      
      <div class="filter-buttons">
        <button 
          class:active={selectedFilter === 'all'} 
          on:click={() => handleFilterChange('all')}
        >
          All Billionaires
        </button>
        <button 
          class:active={selectedFilter === 'self-made'} 
          on:click={() => handleFilterChange('self-made')}
        >
          Self-Made
        </button>
        <button 
          class:active={selectedFilter === 'inherited'} 
          on:click={() => handleFilterChange('inherited')}
        >
          Inherited
        </button>
      </div>
    </div>
    
    <div class="stats-cards">
      <div class="stat-card">
        <h3>Total Wealth</h3>
        <p class="stat-value">{formatMoney(totalWealth)} Billion</p>
      </div>
      <div class="stat-card">
        <h3>Wealthiest Industry</h3>
        <p class="stat-value">{wealthiestIndustry}</p>
      </div>
      <div class="stat-card">
        <h3>Percentage of Total</h3>
        <p class="stat-value">{formatPercent(wealthiestIndustryPercentage)}</p>
      </div>
    </div>
    
    <div class="chart-container">
      {#if series.length > 0 && flatData.length > 0}
        <LayerCake
          padding={{ top: 20, right: 20, bottom: 40, left: 80 }}
          x={d => d.year}
          y0={d => d.y0}
          y1={d => d.y1}
          yDomain={[0, null]}
          data={flatData}
        >
          <Svg>
            <AxisX 
              gridlines={false}
              tickMarks={true}
              baseline={true}
              snapLabels={true}
            />
            <AxisY 
              gridlines={true}
              tickMarks={true}
              format={d => formatMoney(d)}
            />
            
            {#each series as group, i}
              <g class="area-group">
                <Area 
                  data={group}
                  fill={industryColors[i % industryColors.length]}
                />
              </g>
            {/each}
          </Svg>
        </LayerCake>
        
        <div class="legend-container">
          <h3>Industries</h3>
          <div class="legend">
            {#each series as group, i}
              <div class="legend-item">
                <span class="legend-color" style="background-color: {industryColors[i % industryColors.length]};"></span>
                <span class="legend-label">{group.key}</span>
              </div>
            {/each}
          </div>
        </div>
      {:else}
        <p class="no-data">No data available for the selected filters. Try changing the filter options.</p>
      {/if}
    </div>

</div>

<style>
  .industry-page {
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
  
  .loading, .error {
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
  
  .filter-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
  }
  
  .filter-buttons button {
    padding: 0.6rem 1.2rem;
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .filter-buttons button:hover {
    background-color: #eee;
  }
  
  .filter-buttons button.active {
    background-color: #9c8c61;
    color: white;
    border-color: #9c8c61;
  }
  
  .stats-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .stat-card {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    text-align: center;
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
  
  .chart-container {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    height: 500px;
    position: relative;
  }
  
  .no-data {
    text-align: center;
    padding: 2rem;
    font-size: 1.2rem;
    color: #666;
  }
  
  .legend-container {
    margin-top: 2rem;
  }
  
  .legend-container h3 {
    font-size: 1rem;
    margin-bottom: 0.5rem;
    color: #666;
  }
  
  .legend {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.5rem;
  }
  
  .legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
  }
  
  .legend-color {
    display: inline-block;
    width: 16px;
    height: 16px;
    border-radius: 3px;
  }
  
  .area-group {
    transition: opacity 0.2s ease;
  }
  
  .area-group:hover {
    opacity: 0.8;
  }
  
  @media (max-width: 768px) {
    .industry-page {
      padding: 1rem;
    }
    
    h1 {
      font-size: 2rem;
    }
    
    .stats-cards {
      grid-template-columns: 1fr;
    }
    
    .chart-container {
      height: 400px;
      padding: 1rem;
    }
    
    .legend {
      grid-template-columns: 1fr 1fr;
    }
  }
</style>
