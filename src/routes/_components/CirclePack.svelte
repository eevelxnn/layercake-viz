<script>
  import { getContext } from 'svelte';
  import { format } from 'd3-format';
  import { scaleSqrt } from 'd3-scale';

  const { width, height, data } = getContext('LayerCake');

  export let idKey = 'id';
  export let valueKey = 'value';

  export let labelVisibilityThreshold = r => r > 25;
  export let fill = '#fff';
  export let stroke = '#999';
  export let strokeWidth = 1;
  export let textColor = '#333';
  export let textStroke = '#000';
  export let textStrokeWidth = 0;
  export let spacing = 4;

  // Set a consistent radius scale
  const maxValue = 5000;
  const rScale = scaleSqrt().domain([0, maxValue]).range([10, 60]);

  const titleCase = d => d.replace(/^\w/, w => w.toUpperCase());
  const commas = format(',');

  // Layout in grid
  $: descendants = $data.map((d, i) => {
    const value = d[valueKey] || 1;
    const r = rScale(value);

    const cols = Math.floor($width / (r * 2 + spacing));
    const col = i % cols;
    const row = Math.floor(i / cols);

    return {
      ...d,
      x: col * (r * 2 + spacing) + r,
      y: row * (r * 2 + spacing) + r,
      r,
      value
    };
  });
</script>

<svg {width} {height} class="circle-pack-svg">
	{#each descendants as d, i (i)}
		<g transform={`translate(${d.x},${d.y})`}>
			<circle r={d.r} fill={d.self_made ? "#69b3a2" : "#ccc"} {stroke} stroke-width={strokeWidth} />
			{#if labelVisibilityThreshold(d.r)}
				<text
					text-anchor="middle"
					dy=".3em"
					font-size="10"
					fill={textColor}
					style="text-shadow:
            -{textStrokeWidth}px -{textStrokeWidth}px 0 {textStroke},
            {textStrokeWidth}px -{textStrokeWidth}px 0 {textStroke},
            -{textStrokeWidth}px {textStrokeWidth}px 0 {textStroke},
            {textStrokeWidth}px {textStrokeWidth}px 0 {textStroke};"
				>
					{titleCase(d[idKey])}
				</text>
			{/if}
		</g>
	{/each}
</svg>

<style>
  .circle-pack-svg {
    width: 100%;
    height: 100%;
    display: block;
    overflow: visible;
  }
</style>
