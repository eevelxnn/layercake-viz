
<script>
  import { LayerCake, Svg } from 'layercake';
  import { stack } from 'd3-shape';
  import { format } from 'd3-format';
  import AxisX from '../_components/AxisX.svelte';
  import AxisY from '../_components/AxisY.svelte';
  import StackedAreas from '../_components/StackedAreas.svelte';
  import raw from '../_data/industry_wealth.json';

  const formatMoney = format('$,.0f');
  const formatPercent = format('.1f');

  const years = Array.from(new Set(raw.map(d => d.year))).sort();
  let year = 1997;
  let selectedFilter = 'all';

  const industryKeysRaw = Object.keys(raw[0]).filter(k => k !== 'year' && k !== 'filter');

  function cleanKey(k) {
    return k.replace(/[\[\]']/g, '').trim();
  }

  // Map cleaned keys to raw keys
  const keyMap = {};
  industryKeysRaw.forEach(k => {
    keyMap[cleanKey(k)] = k;
  });

  const displayKeys = Object.keys(keyMap);

  let filtered = [];
  let stackedSeries = [];

  $: filtered = raw.filter(d => d.year === year && d.filter === selectedFilter);
  $: {
    const stackData = filtered.map(d => {
      const row = { year: d.year };
      displayKeys.forEach(k => {
        row[k] = d[keyMap[k]] || 0;
      });
      return row;
    });

    const stackGen = stack().keys(displayKeys);
    stackedSeries = stackGen(stackData);

    // Needed for zGet
    stackedSeries.forEach((layer, i) => {
      layer.key = displayKeys[i];
      layer.forEach(d => (d.key = displayKeys[i]));
    });
  }
</script>

<div class="container">
  <header>
    <h1>Industry Wealth Over Time</h1>
    <p class="subtitle">Stacked area view of billionaire wealth by industry</p>
  </header>

  <div class="controls">
    <div class="slider">
      <h2>{year}</h2>
      <input
        type="range"
        min={Math.min(...years)}
        max={Math.max(...years)}
        bind:value={year}
      />
    </div>
    <div class="filters">
      <button class:selected={selectedFilter === 'all'} on:click={() => selectedFilter = 'all'}>All</button>
      <button class:selected={selectedFilter === 'self-made'} on:click={() => selectedFilter = 'self-made'}>Self-Made</button>
      <button class:selected={selectedFilter === 'inherited'} on:click={() => selectedFilter = 'inherited'}>Inherited</button>
    </div>
  </div>

  <div class="chart-container">
    <LayerCake
      data={stackedSeries}
      accessors={{
        xGet: d => d.data.year,
        yGet: d => d[1] - d[0],
        zGet: d => d.key
      }}
      scales={{
        xScale: 'scaleLinear',
        yScale: 'scaleLinear',
        zScale: 'scaleOrdinal'
      }}
      xDomain={[Math.min(...years), Math.max(...years)]}
      yDomain={[0, null]}
      padding={{ top: 20, right: 20, bottom: 40, left: 60 }}
    >
      <Svg>
        <AxisX />
        <AxisY format={formatMoney} />
        <StackedAreas />
      </Svg>
    </LayerCake>
  </div>
</div>

<style>
  .container {
    max-width: 1200px;
    margin: auto;
    padding: 2rem;
    font-family: system-ui, sans-serif;
  }

  .subtitle {
    color: #666;
    font-size: 1rem;
    margin-top: 0.5rem;
  }

  .controls {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    align-items: center;
  }

  .slider h2 {
    font-size: 2rem;
    margin: 0 1rem 0 0;
    color: #2c3e50;
  }

  .filters button {
    padding: 0.5rem 1rem;
    margin-left: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    background: white;
    cursor: pointer;
  }

  .filters button.selected {
    background-color: #9b59b6;
    color: white;
  }

  .chart-container {
    height: 500px;
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  }
</style>
