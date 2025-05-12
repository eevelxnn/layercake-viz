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
  import { format } from 'd3-format';

  const { data, width, height } = getContext('LayerCake');


  export let valueKey = 'value';
  export let idKey = 'id';
  export let manyBodyStrength = -10;
  export let nodeStroke = '#fff';
  export let nodeStrokeWidth = 1;

  const maxValue = 5000;
  const rScale = scaleSqrt().domain([0, maxValue]).range([5, 80]);
  const formatBillion = format(',.2f');

  const getColor = d => d.self_made ? '#9b59b6' : '#d3d3d3';

  let nodes = [];
  let simulation;

  const findExistingNode = id => nodes.find(n => n[idKey] === id);

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  let tooltip = null;
  let tooltipX = 0;
  let tooltipY = 0;
  let hoveredId = null;

  function handleMouseMove(event) {
    tooltipX = event.clientX + 12;
    tooltipY = event.clientY + 12;
  }

  $: if ($data.length) {
const nextNodes = $data.map(d => {
  const existing = findExistingNode(d[idKey]);
  const r = rScale(d[valueKey]);

  return existing
    ? {
        ...d,
        r,
        x: existing.x,
        y: existing.y,
        vx: existing.vx || 0,
        vy: existing.vy || 0
      }
    : {
        ...d,
        r,
        x: Math.random() * $width,
        y: $height + 100,
        vx: 0,
        vy: 0
      };
});


    if (simulation) simulation.stop();

    simulation = forceSimulation(nextNodes)
      .force('x', forceX($width / 2).strength(0.1))
.force('y', forceY(d => d.self_made ? $height / 3 : ($height * 2) / 3).strength(0.15))
      .force('center', forceCenter($width / 2, $height / 2))
      .force('charge', forceManyBody().strength(manyBodyStrength))
      .force('collision', forceCollide().radius(d => d.r + 2).strength(0.75))
      .alpha(0.3).alphaDecay(0.01)
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

<div on:mousemove={handleMouseMove} style="position: relative;">
  <svg {width} {height}>
{#each nodes as d (d[idKey])}
<g
        transform={`translate(${d.x}, ${d.y})`}
        on:mouseenter={() => {
          tooltip = d;
          hoveredId = d[idKey];
        }}
        on:mouseleave={() => {
          tooltip = null;
          hoveredId = null;
        }}
      >
        <circle
          r={rScale(d[valueKey])}
          fill={getColor(d)}
          stroke={hoveredId === d[idKey] ? '#000' : nodeStroke}
          stroke-width={hoveredId === d[idKey] ? 3 : nodeStrokeWidth}
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

  {#if tooltip}
    <div
      class="tooltip"
      style="top: {tooltipY}px; left: {tooltipX}px;"
    >
      <strong>{tooltip[idKey]}</strong><br />
      Net Worth: ${formatBillion(tooltip[valueKey])}B<br />
      {tooltip.self_made ? "Self-Made" : "Inherited"}
    </div>
  {/if}
</div>

<style>
  svg {
    width: 100%;
    height: 100%;
    display: block;
    overflow: visible;
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
</style>