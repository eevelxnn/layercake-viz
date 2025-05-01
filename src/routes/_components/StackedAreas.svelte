<script>
  import { getContext } from 'svelte';
  import { area } from 'd3-shape';

  const { data, xGet, yScale, zScale } = getContext('LayerCake');

  $: areaGen = area()
    .x(d => $xGet(d))
    .y0(d => $yScale(d[0]))
    .y1(d => $yScale(d[1]));
  
</script>

<g>
  {#each $data as d}
  console.log('key', d.key, zScale(d.key));
    console.log("hello");

<path
  d={areaGen(d)}
  
  fill={$zScale(d.key)}
  stroke="white"
  stroke-width="0.5"
/>
  {/each}
</g>
