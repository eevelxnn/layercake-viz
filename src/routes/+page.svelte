<script>
  import { LayerCake } from 'layercake';
  import CircleForce from './_components/CircleForce.svelte';
  import raw from './_data/billionaires_by_year.json';

  let width = 800;
  let height = 800;

  const years = Array.from(new Set(raw.map(d => d.year))).sort();

  let year = 2020; // default year
  let data = [];

$: data = raw
  .filter(d => d.year === year && d.avg_net_worth > 0)
  .map(d => ({
    id: d.full_name,
    value: d.avg_net_worth,
    self_made: d.self_made
  }));
</script>

<!-- Year Timeline Control -->
<div style="margin-bottom: 1rem;">
  <label for="year">Year: {year}</label>
<input
  type="range"
  id="year"
  min={Math.min(...years)}
  max={Math.max(...years)}
  bind:value={year}
  step="1"
  style="width: 100%;"
/>
</div>

<!-- Force-directed Circle Pack -->
  <LayerCake {width} {height} {data}>
  <CircleForce />
</LayerCake>

<style>
  input[type="range"] {
    width: 100%;
  }
</style>
