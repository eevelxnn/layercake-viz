<script>
  import { getContext } from 'svelte';
  import {
    forceSimulation,
    forceX,
    forceY,
    forceManyBody,
    forceCollide,
    forceCenter
  } from 'd3-force';
  import { scaleSqrt } from 'd3-scale';

  const { data, width, height } = getContext('LayerCake');

  export let valueKey = 'value';
  export let idKey = 'id';
  export let manyBodyStrength = -10;
  export let nodeStroke = '#fff';
  export let nodeStrokeWidth = 1;

  const maxValue = 5000;
  const rScale = scaleSqrt().domain([0, maxValue]).range([10, 80]);

  const getColor = d => d.self_made ? '#69b3a2' : '#ccc';

  let nodes = [];
  let simulation;

  const findExistingNode = id => nodes.find(n => n[idKey] === id);

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  $: if ($data.length) {
    const nextNodes = $data.map(d => {
      const existing = findExistingNode(d[idKey]);
      const r = rScale(d[valueKey]);

      return existing
        ? { ...existing, ...d, r }
        : {
            ...d,
            x: Math.random() * $width,
            y: $height + 100, // animate from below
            r
          };
    });

    if (simulation) simulation.stop();

    simulation = forceSimulation(nextNodes)
      .force('x', forceX($width / 2).strength(0.1))
      .force('y', forceY($height / 2).strength(0.1))
      .force('center', forceCenter($width / 2, $height / 2))
      .force('charge', forceManyBody().strength(manyBodyStrength))
      .force('collision', forceCollide().radius(d => d.r + nodeStrokeWidth / 2).strength(1))
      .alpha(1)
      .restart();

    simulation.on('tick', () => {
      nodes = simulation.nodes().map(d => {
        d.x = clamp(d.x, d.r, $width - d.r);
        d.y = clamp(d.y, d.r, $height - d.r);
        return d;
      });
    });
  }
</script>

<svg {width} {height}>
  {#each nodes as d, i (d[idKey] + '-' + d[valueKey])}
    <g transform={`translate(${d.x}, ${d.y})`}>
      <circle
        r={rScale(d[valueKey])}
        fill={getColor(d)}
        stroke={nodeStroke}
        stroke-width={nodeStrokeWidth}
      />
      {#if rScale(d[valueKey]) > 25}
        <text
          text-anchor="middle"
          dy=".3em"
          font-size="10"
          fill="#333"
        >
          {d[idKey]}
        </text>
      {/if}
    </g>
  {/each}
</svg>

<style>
  svg {
    width: 100%;
    height: 100%;
    display: block;
    overflow: visible;
  }
</style>
