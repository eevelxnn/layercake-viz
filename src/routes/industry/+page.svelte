<script>
  import { LayerCake, Svg, flatten, stack } from 'layercake';
  import { format } from 'd3-format';
  import AxisX from '../_components/AxisX.svelte';
  import AxisY from '../_components/AxisY.svelte';
  import AreaStacked from '../_components/StackedAreas.svelte';

  import raw from '../_data/industry_wealth.json';

  let tooltip = { visible: false, x: 0, y: 0, industry: '', value: 0, year: 0 };

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

  

  function handleMousemove(event, d) {
    tooltip = {
      visible: true,
      x: event.clientX,
      y: event.clientY,
      industry: d.key,
      value: d[1] - d[0],
      year: d.data.year
    };
  }

  function handleMouseleave() {
    tooltip.visible = false;
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

  const stackedData = stack(cleanData, seriesNames);
  stackedData.forEach((layer, i) => {
    layer.key = seriesNames[i];
    layer.forEach(d => d.key = seriesNames[i]);
  });

  const flatData = flatten(stackedData);
  const formatBillion = format(',.2f');
</script>

<div class="chart-container">
  <h2 class="chart-title">Industry Wealth Distribution</h2>

  <div class="chart-wrapper">
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
  <div class="legend-item">
    <span class="legend-color" style="background-color: #9c8c61;"></span>
    <span class="legend-label">Manufacturing</span>
  </div>
  <div class="legend-item">
    <span class="legend-color" style="background-color: #1f77b4;"></span>
    <span class="legend-label">Technology</span>
  </div>
  <div class="legend-item">
    <span class="legend-color" style="background-color: #ff7f0e;"></span>
    <span class="legend-label">Real Estate</span>
  </div>
  <div class="legend-item">
    <span class="legend-color" style="background-color: #2ca02c;"></span>
    <span class="legend-label">Fashion & Retail</span>
  </div>
  <div class="legend-item">
    <span class="legend-color" style="background-color: #d62728;"></span>
    <span class="legend-label">Diversified</span>
  </div>
  <div class="legend-item">
    <span class="legend-color" style="background-color: #9467bd;"></span>
    <span class="legend-label">Finance & Investments</span>
  </div>
  <div class="legend-item">
    <span class="legend-color" style="background-color: #8c564b;"></span>
    <span class="legend-label">Finance and Investments</span>
  </div>
  <div class="legend-item">
    <span class="legend-color" style="background-color: #e377c2;"></span>
    <span class="legend-label">Healthcare</span>
  </div>
  <div class="legend-item">
    <span class="legend-color" style="background-color: #7f7f7f;"></span>
    <span class="legend-label">Energy</span>
  </div>
  <div class="legend-item">
    <span class="legend-color" style="background-color: #bcbd22;"></span>
    <span class="legend-label">Food and Beverage</span>
  </div>
</div>



  {#if tooltip.visible}
    <div class="tooltip" style="top: {tooltip.y}px; left: {tooltip.x}px;">
      <strong>{tooltip.industry}</strong><br />
      Year: {tooltip.year}<br />
      Net Worth: ${formatBillion(tooltip.value)}B
    </div>
  {/if}
</div>

<style>
  .chart-container {
    width: 100%;
    height: auto;
    padding: 2rem;
    background-color: #f5f5f5;
    font-family: 'Playfair Display', 'Georgia', serif;
    color: #333;
    border-radius: 4px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  }

  .chart-title {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #333;
  }

  .chart-wrapper {
    width: 100%;
    height: 400px;
    margin-bottom: 2rem;
  }

  .chart-legend {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
    margin-top: 1rem;
  }

  .legend-item {
    display: flex;
    align-items: center;
    margin-right: 1rem;
  }

  .legend-color {
    display: inline-block;
    width: 16px;
    height: 16px;
    margin-right: 6px;
    border-radius: 2px;
  }

  .legend-label {
    font-size: 0.9rem;
    color: #555;
  }

  .chart-title::after {
    content: '';
    display: block;
    width: 100px;
    height: 1px;
    background-color: #9c8c61;
    margin: 1rem auto;
  }

  .tooltip {
    position: fixed;
    background: white;
    color: black;
    padding: 6px 10px;
    font-size: 13px;
    border: 1px solid #ccc;
    border-radius: 6px;
    pointer-events: none;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    z-index: 1000;
    max-width: 200px;
  }

  @media (max-width: 768px) {
    .chart-wrapper {
      height: 300px;
    }

    .chart-legend {
      flex-direction: column;
      align-items: center;
    }
  }
</style>
