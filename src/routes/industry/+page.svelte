<script>
	import { onMount } from 'svelte';
	import { scaleLinear, scaleBand } from 'd3-scale';
	import { max } from 'd3-array';
	import { format } from 'd3-format';
	import { forceSimulation, forceX, forceY, forceCollide, forceManyBody } from 'd3-force';
	import raw from '../_data/industry_wealth.json';

	// Layout and state
	const margin = { top: 40, right: 30, bottom: 50, left: 60 };
	let width = 1100;
	let height = 600;
	let years = [];
	let selectedYear = 2023;
	let isLoading = true;

	// Industry setup
	let industryColors = {};
	function getRandomColor() {
		const hue = Math.floor(Math.random() * 360);
		return `hsl(${hue}, 60%, 60%)`;
	}

	// the nine industries to display stats for:
	const focusIndustries = [
		'Technology',
		'Fashion and Retail',
		'Finance and Investments',
		'Diversified',
		'Manufacturing',
		'Real Estate',
		'Energy',
		'Healthcare',
		'Food and Beverage'
	];

	let topIndustries = [];
	let industryScale, rScale;
	let filtered = [];
	let nodes = [];
	let simulation;

	// per-industry stats
	let industryStats = [];

	// normalize keys ("&" → "and", strip brackets/quotes)
	const data = raw.map(d => {
		const nd = { year: d.year, filter: d.filter };
		Object.entries(d).forEach(([k, v]) => {
			if (k !== 'year' && k !== 'filter') {
				const norm = k
					.replace(/&/g, 'and')
					.replace(/[\[\]']/g, '')
					.replace(/\s+/g, ' ')
					.trim();
				nd[norm] = (nd[norm] || 0) + v;
			}
		});
		return nd;
	});

	onMount(() => {
		years = [...new Set(data.map(d => d.year))].sort();
		if (years.length) selectedYear = years[years.length - 1];

		const industryTotals = {};
		data.forEach(d => {
			Object.keys(d).forEach(k => {
				if (k !== 'year' && k !== 'filter') {
					industryTotals[k] = (industryTotals[k] || 0) + (d[k] || 0);
				}
			});
		});
		topIndustries = Object.entries(industryTotals)
			.sort((a, b) => b[1] - a[1])
			.slice(0, 10)
			.map(([k]) => k);

		topIndustries.forEach(ind => {
			if (!industryColors[ind]) industryColors[ind] = getRandomColor();
		});

		updateVis();
		isLoading = false;
	});

	function updateVis() {
		filtered = data.filter(d => d.year === selectedYear && d.filter === 'all');

		industryStats = focusIndustries.map(ind => {
			const val = filtered[0]?.[ind] || 0;
			return { industry: ind, count: Math.max(1, Math.round(val)) };
		});

		let allCircles = [];
		topIndustries.forEach(industry => {
			const val = filtered[0]?.[industry] || 0;
			const count = Math.max(1, Math.round(val));
			for (let j = 0; j < count; j++) {
				allCircles.push({
					industry,
					value: 1,
					color: industryColors[industry] || '#ccc',
					key: `${industry}-${j}`
				});
			}
		});

		industryScale = scaleBand()
			.domain(topIndustries)
			.range([margin.left, width - margin.right])
			.padding(0.1);

		const maxVal = max(allCircles, d => d.value) || 1;
		rScale = scaleLinear().domain([0, maxVal]).range([0.5, 3]);

		nodes = allCircles.map(d => ({
			...d,
			x:
				industryScale(d.industry) +
				industryScale.bandwidth() / 2 +
				(Math.random() - 0.5) * industryScale.bandwidth() * 0.6,
			y: margin.top + Math.random() * (height - margin.top - margin.bottom),
			r: rScale(d.value)
		}));

		if (simulation) simulation.stop();
		simulation = forceSimulation(nodes)
			.force(
				'x',
				forceX(d => industryScale(d.industry) + industryScale.bandwidth() / 2).strength(0.5)
			)
			.force('y', forceY(height / 2).strength(0.05))
			.force('collide', forceCollide(d => d.r + 1).strength(1))
			.force('repulse', forceManyBody().strength(-0.03))
			.alpha(0.7)
			.alphaDecay(0.03)
			.on('tick', () => {
				nodes.forEach(d => {
					const start = industryScale(d.industry),
						end = start + industryScale.bandwidth();
					d.x = Math.max(start + d.r, Math.min(end - d.r, d.x));
				});
				nodes = [...nodes];
			});
	}

	function onYear(e) {
		selectedYear = +e.target.value;
		updateVis();
	}
</script>

<div class="container">
	<header>
		<h1>Industry Wealth Distribution</h1>
		<p class="subtitle">How industry composition of billionaire wealth has evolved over time</p>
	</header>

	<!-- show each focus industry's billionaire counts -->
	<div class="stats-cards">
		{#each industryStats as s}
			<div class="stat-card" style="border-top-color: {industryColors[s.industry]};">
				<h3>{s.industry}</h3>
				<p class="stat-label">Number of billionaires:</p>
				<p class="stat-value">{s.count}</p>
			</div>
		{/each}
	</div>

	<div class="controls-container">
		<div class="year-slider">
			<div class="year-display">
				<span>Selected Year: <strong>{selectedYear}</strong></span>
			</div>
			<input
				type="range"
				min={Math.min(...years)}
				max={Math.max(...years)}
				bind:value={selectedYear}
				on:input={onYear}
				class="timeline-slider"
			/>
			<div class="year-labels">
				<span>{Math.min(...years)}</span>
				<span>{Math.max(...years)}</span>
			</div>
		</div>
	</div>

	<div class="chart-container">
		<svg {width} {height}>
			{#each topIndustries as industry, i}
				{#if i > 0}
					<line
						x1={industryScale(industry)}
						x2={industryScale(industry)}
						y1={margin.top}
						y2={height - margin.bottom}
						stroke="#eee"
						stroke-width="1"
						stroke-dasharray="4,2"
						class="industry-separator"
					/>
				{/if}
				<line
					x1={industryScale(industry) + industryScale.bandwidth() / 2}
					x2={industryScale(industry) + industryScale.bandwidth() / 2}
					y1={margin.top}
					y2={height - margin.bottom}
					class="grid-line"
				/>
			{/each}

			{#each nodes as d (d.key)}
				<circle cx={d.x} cy={d.y} r={d.r} fill={d.color} stroke="#fff" stroke-width="1" />
			{/each}
		</svg>
	</div>

	<div class="chart-legend">
		{#each topIndustries as industry}
			<div class="legend-item">
				<span class="legend-color" style="background-color: {industryColors[industry]}"></span>
				<span class="legend-label">{industry}</span>
			</div>
		{/each}
	</div>
</div>

<a href="/age-distribution" class="arrow-float left" aria-label="Previous page">←</a>
<a href="/map" class="arrow-float right" aria-label="Next page">→</a>

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
		font-size: 2.5rem;
		margin-bottom: 0.5rem;
		color: #2c3e50;
	}

	.subtitle {
		font-size: 1.1rem;
		color: #7f8c8d;
		margin-top: 0;
	}

	/* stats cards grid for nine industries */
	.stats-cards {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
		gap: 1rem;
		margin: 1.5rem 0;
	}

	.stat-card {
		background-color: rgba(255, 255, 255, 0.9);
		padding: 1rem 1.5rem;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
		text-align: center;
		border-top: 4px solid;
	}

	.stat-card h3 {
		font-size: 1rem;
		margin-bottom: 0.25rem;
	}

	.stat-label {
		font-size: 0.9rem;
		color: #666;
		margin: 0.25rem 0;
	}

	.stat-value {
		font-size: 1.6rem;
		font-weight: bold;
		margin: 0.25rem 0;
	}

	.controls-container {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		margin-bottom: 2rem;
		background-color: rgba(255, 255, 255, 0.9);
		padding: 1.5rem;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
	}

	.year-slider {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.year-display {
		font-size: 1.2rem;
		text-align: center;
		margin-bottom: 0.5rem;
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
		position: absolute;
		top: 100%;
		left: 10px;
		right: 10px;
		text-align: center;
		font-size: 0.8rem;
		color: #7f8c8d;
	}

	.chart-container {
		background-color: white;
		border-radius: 8px;
		padding: 1rem;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
		overflow: hidden;
		width: 100%;
		height: 600px;
	}

	.grid-line {
		stroke: #eee;
		stroke-width: 1;
	}

	.chart-legend {
		display: flex;
		flex-wrap: nowrap;
		justify-content: center;
		gap: 1rem;
		margin-top: 2rem;
		overflow-x: auto;
	}

	.legend-item {
		flex: 0 0 auto;
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

	.legend-label {
		white-space: normal;
		word-break: break-word;
		max-width: 6rem;
		text-align: center;
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
