<script>
  import { getContext, createEventDispatcher } from 'svelte';
  import { area } from 'd3-shape';

  const dispatch = createEventDispatcher();
  const { data, xGet, yScale } = getContext('LayerCake');

  const industryColors = {
    'Manufacturing': '#9c8c61',
    'Technology': '#1f77b4',
    'Real Estate': '#ff7f0e',
    'Fashion & Retail': '#2ca02c',
    'Diversified': '#d62728',
    'Finance & Investments': '#9467bd',
    'Finance and Investments': '#8c564b',
    'Healthcare': '#e377c2',
    'Energy': '#7f7f7f',
    'Food and Beverage': '#bcbd22'
  };

  $: areaGen = area()
    .x(d => $xGet(d))
    .y0(d => $yScale(d[0]))
    .y1(d => $yScale(d[1]));
</script>

<g>
  {#each $data as d}
    <path
      d={areaGen(d)}
      fill={industryColors[d.key] || '#ccc'}
      stroke="white"
      stroke-width="0.5"
      on:mousemove={(e) => dispatch('hover', { e, d })}
      on:mouseleave={() => dispatch('leave')}
    />
  {/each}
</g>

<style>
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

  path {
    cursor: pointer;
  }
</style>
