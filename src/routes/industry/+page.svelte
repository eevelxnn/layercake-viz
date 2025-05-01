<script>
  import { LayerCake, Svg, flatten, stack } from 'layercake';
  import { scaleOrdinal } from 'd3-scale';
  import AxisX from '../_components/AxisX.svelte';
  import AxisY from '../_components/AxisY.svelte';
  import AreaStacked from '../_components/StackedAreas.svelte';

  import raw from '../_data/industry_wealth.json';

  const xKey = 'year';
  const zKey = 'key';

  const rawKeys = Object.keys(raw[0]).filter(k => k !== 'year' && k !== 'filter');
  const clean = k => k.replace(/[\[\]']/g, '').trim();
  const keyMap = {};
  rawKeys.forEach(k => keyMap[clean(k)] = k);
  const seriesNames = Object.keys(keyMap);

  const colorScale = scaleOrdinal()
    .domain(seriesNames)
.range([
  '#1f77b4', // blue
  '#ff7f0e', // orange
  '#2ca02c', // green
  '#d62728', // red
  '#9467bd', // purple
  '#8c564b', // brown
  '#e377c2', // pink
  '#7f7f7f', // gray
  '#bcbd22', // lime
  '#17becf'  // cyan
])


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
</script>

<div class="chart-container">
  <LayerCake
    padding={{ top: 20, right: 20, bottom: 30, left: 40 }}
    x={d => d.data.year}
    y={[0, 1]}
    z={d => d.key}
    zScale={colorScale}
    zDomain={seriesNames}
    flatData={flatData}
    data={stackedData}
  >
    <Svg>
      <AxisX />
      <AxisY />
      <AreaStacked />
    </Svg>
  </LayerCake>
</div>

<style>
  .chart-container {
    width: 100%;
    height: 300px;
  }
</style>
