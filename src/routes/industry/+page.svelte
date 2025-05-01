<script>
  import { LayerCake, Svg, flatten, stack } from 'layercake';
  import { format } from 'd3-format';
  import AxisX from '../_components/AxisX.svelte';
  import AxisY from '../_components/AxisY.svelte';
  import AreaStacked from '../_components/StackedAreas.svelte';

  import raw from '../_data/industry_wealth.json';

  let tooltip = { visible: false, x: 0, y: 0, industry: '', value: 0, year: 0, percentage: 0 };

  const industryColors = {
    'Manufacturing': '#9c8c61',
    'Technology': '#333333',
    'Real Estate': '#555555',
    'Fashion & Retail': '#777777',
    'Diversified': '#999999',
    'Finance & Investments': '#a89876',
    'Finance and Investments': '#8a7c51',
    'Healthcare': '#6a5d41',
    'Energy': '#444444',
    'Food and Beverage': '#666666'
  };

  function colorScale(industry) {
    return industryColors[industry] || '#ccc';
  }

  const xKey = 'year';
  const rawKeys = Object.keys(raw[0]).filter(k => k !== 'year' && k !== 'filter');
  const clean = k => k.replace(/[\[\]']/g, '').trim();
  const keyMap = {};
  rawKeys.forEach(k => keyMap[clean(k)] = k);
  const seriesNames = Object.keys(keyMap);

  const filtered = raw.filter(d => d.filter === 'all');

  const cleanData = filtered.map(d => {
    const row = { year: d.year };
    seriesNames.forEach(k => {
      row[k] = d[keyMap[k]] || 0;
    });
    return row;
  });

  const yearlyTotals = {};
  cleanData.forEach(row => {
    const total = seriesNames.reduce((sum, k) => sum + (row[k] || 0), 0);
    yearlyTotals[row.year] = total;
  });

  const stackedData = stack(cleanData, seriesNames);
  stackedData.forEach((layer, i) => {
    layer.key = seriesNames[i];
    layer.forEach(d => d.key = seriesNames[i]);
  });

  const flatData = flatten(stackedData);
  const formatBillion = format(',.2f');

  function handleMousemove(event, d) {
    const year = d.data.year;
    const value = d[1] - d[0];
    const total = yearlyTotals[year] || 1;
    const percentage = (value / total) * 100;

    tooltip = {
      visible: true,
      x: event.clientX,
      y: event.clientY,
      industry: d.key,
      value,
      year,
      percentage
    };
  }

  function handleMouseleave() {
    tooltip.visible = false;
  }
</script>

<div class="container">
  <header>
    <h1>Industry Wealth Distribution</h1>
    <p class="subtitle">How industry composition of billionaire wealth has evolved over time</p>
  </header>

  <div class="visualization">
    <LayerCake
      padding={{ top: 30, right: 30, bottom: 40, left: 50 }}
      x={d => d.data.year}
      y={[0, 1]}
      z={d => d.key}
      zDomain={seriesNames}
      flatData={flatData}
      data={stackedData}
    >
      <Svg>
        <AxisX gridlines={false} tickColor="#333" baselineColor="#9c8c61" />
        <AxisY gridlines={true} gridColor="#e0e0e0" tickColor="#333" baselineColor="#9c8c61" />
        <AreaStacked 
          on:hover={(e) => handleMousemove(e.detail.e, e.detail.d)}
          on:leave={handleMouseleave}
        />
      </Svg>
    </LayerCake>
  </div>

  <div class="chart-legend">
    {#each Object.keys(industryColors) as industry}
      <div class="legend-item">
        <span class="legend-color" style="background-color: {industryColors[industry]};"></span>
        <span class="legend-label">{industry}</span>
      </div>
    {/each}
  </div>

  {#if tooltip.visible}
    <div class="tooltip" style="top: {tooltip.y}px; left: {tooltip.x}px;">
      <strong>{tooltip.industry}</strong><br />
      Year: {tooltip.year}<br />
      Net Worth: ${formatBillion(tooltip.value)}B<br />
      Share of Total Wealth: {tooltip.percentage.toFixed(1)}%
    </div>
  {/if}
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

  .visualization {
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
    .visualization {
      height: 400px;
    }

    .legend-item {
      font-size: 0.8rem;
    }
  }
</style>

<a href="/age" class="arrow-float right" aria-label="Next page">→</a>