<script>
	import { onMount } from 'svelte';
	import { geoPath, geoMercator } from 'd3-geo';
	import { scaleLinear } from 'd3-scale';
	import { feature } from 'topojson-client';

	import worldData from '../_data/land-50m.json';
	import countryData from '../_data/billionaires_country.json';

	let width = 1200;
	let height = 600;
	let year = 1997;
	let filter = 'overall'; // 'overall', 'selfmade', or 'inherited'

	let mapFeatures = [];
	const dataByFilter = {
		overall: {},
		selfmade: {},
		inherited: {}
	};

	// tooltip state
	let showTooltip = false;
	let tooltipX = 0;
	let tooltipY = 0;
	let tooltipContent = '';

	onMount(() => {
		mapFeatures = feature(worldData, worldData.objects.countries).features;

		countryData.forEach(d => {
			const y = +d.year;
			const c = d.country_of_citizenship;
			const sm = d.self_made;

			// Overall count
			dataByFilter.overall[y] = dataByFilter.overall[y] || {};
			dataByFilter.overall[y][c] = (dataByFilter.overall[y][c] || 0) + 1;

			// Self-made
			if (sm === true) {
				dataByFilter.selfmade[y] = dataByFilter.selfmade[y] || {};
				dataByFilter.selfmade[y][c] = (dataByFilter.selfmade[y][c] || 0) + 1;
			}

			// Inherited
			if (sm === false) {
				dataByFilter.inherited[y] = dataByFilter.inherited[y] || {};
				dataByFilter.inherited[y][c] = (dataByFilter.inherited[y][c] || 0) + 1;
			}
		});
	});

	$: counts = dataByFilter[filter][year] || {};
	$: maxCount = Math.max(...Object.values(counts), 1);
	$: colorScale = scaleLinear().domain([0, maxCount]).range(['#f2e5f7', '#9b59b6']);

	function getColor(feature) {
		const name = feature.properties.name;
		const value = counts[name] || 0;
		return value > 0 ? colorScale(value) : '#eee';
	}

	const projection = geoMercator()
		.scale(130)
		.translate([width / 2, height / 1.5]);
	const path = geoPath(projection);

	function handleMouseMove(event, feature) {
		const name = feature.properties.name;
		const count = counts[name] || 0;
		tooltipContent = `${name}: ${count}`;
		showTooltip = true;
		const { pageX, pageY } = event;
		tooltipX = pageX + 10;
		tooltipY = pageY + 10;
	}

	function handleMouseOut() {
		showTooltip = false;
	}
</script>

<div class="container">
	<header>
		<h1>Global Distribution of Billionaires</h1>
		<p class="subtitle">Use the slider and filters below to explore {year} data</p>
	</header>

	<div class="controls-container">
		<div class="year-slider">
			<div class="year-display">
				<span>Selected Year: <strong>{year}</strong></span>
			</div>
			<input
				type="range"
				min="1997"
				max="2024"
				step="1"
				bind:value={year}
				class="timeline-slider"
			/>
			<div class="year-labels">
				<span>1997</span>
				<span>2024</span>
			</div>
		</div>

		<div class="filter-buttons">
			<button on:click={() => (filter = 'overall')} class:selected={filter === 'overall'}
				>Overall</button
			>
			<button on:click={() => (filter = 'selfmade')} class:selected={filter === 'selfmade'}
				>Self-Made</button
			>
			<button on:click={() => (filter = 'inherited')} class:selected={filter === 'inherited'}
				>Inherited</button
			>
		</div>
	</div>

	<div class="map-wrapper">
		<svg {width} {height}>
			{#if mapFeatures.length}
				{#each mapFeatures as country}
					<path
						d={path(country)}
						class="country"
						fill={getColor(country)}
						on:mousemove={e => handleMouseMove(e, country)}
						on:mouseout={handleMouseOut}
					/>
				{/each}
			{/if}
		</svg>
		{#if showTooltip}
			<div class="tooltip" style="left: {tooltipX}px; top: {tooltipY}px">
				{tooltipContent}
			</div>
		{/if}
	</div>

	<a href="/industry" class="arrow-float left" aria-label="Previous page">←</a>
	<a href="/intro" class="arrow-float right" aria-label="Next page">→</a>
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
		margin-bottom: 1rem;
	}
	h1 {
		font-size: 2rem;
		margin-bottom: 0.5rem;
		color: #2c3e50;
	}
	.subtitle {
		font-size: 1rem;
		color: #7f8c8d;
		margin-top: 0;
	}

	.controls-container,
	.map-wrapper {
		width: 1200px;
		margin: 0 auto 2rem;
		background-color: #fff;
		padding: 1rem;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
	}

	.year-slider {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		width: 100%;
	}
	.year-display {
		font-size: 1.2rem;
		text-align: center;
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
		font-size: 0.8rem;
		color: #7f8c8d;
	}

	.filter-buttons {
		display: flex;
		justify-content: center;
		gap: 1rem;
		margin-top: 1rem;
	}
	.filter-buttons button {
		padding: 0.5rem 1rem;
		border: 1px solid #ccc;
		background: #fff;
		cursor: pointer;
		border-radius: 4px;
		font-size: 1rem;
	}
	.filter-buttons button.selected {
		background: #9b59b6;
		color: #fff;
		border-color: #9b59b6;
	}

	svg {
		width: 100%;
		height: auto;
		border-radius: 4px;
	}
	.map-wrapper {
		position: relative;
	}
	.country {
		stroke: #fff;
		stroke-width: 0.5px;
		cursor: pointer;
	}
	.tooltip {
		position: absolute;
		background: rgba(0, 0, 0, 0.7);
		color: #fff;
		padding: 6px 10px;
		border-radius: 4px;
		pointer-events: none;
		font-size: 0.9rem;
		white-space: nowrap;
		z-index: 10;
	}

	.arrow-float {
		position: fixed;
		top: 50%;
		transform: translateY(-50%);
		font-size: 2.5rem;
		color: white;
		background-color: #2c3e50;
		padding: 0.75rem 1rem;
		border-radius: 8px;
		text-decoration: none;
		z-index: 999;
		transition: background 0.2s ease;
	}
	.arrow-float:hover {
		background-color: #34495e;
	}
	.arrow-float.left {
		left: 20px;
	}
	.arrow-float.right {
		right: 20px;
	}
</style>
