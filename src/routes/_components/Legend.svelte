<script lang="ts">
    /** You can pass a different palette if you ever need to */
    export let items = [
      { label: 'Self-Made',  color: '#69b3a2' },
      { label: 'Inherited', color: '#ccc'    }
    ];
</script>

<div class="legend">
	{#each items as item}
		<div class="item">
			<span class="swatch" style="background:{item.color}" />
			<span class="label">{item.label}</span>
		</div>
	{/each}
</div>

<style>
    .legend{
      position:absolute;
      top:3.5rem;
      right:1rem;
      background:#fff;
      border:1px solid #ccc;
      border-radius:6px;
      padding:0.75rem 1rem;
      font-size:0.75rem;
      box-shadow:0 2px 4px rgba(0,0,0,.15);
      pointer-events:none;       /* don’t block the drag */
    }
    .item{display:flex;align-items:center;gap:0.6rem;margin:0.25rem 0;}
    .swatch{
      width:1.1rem;
      height:1.1rem;
      border-radius:50%;
      border:1px solid #888;
      flex:none;
    }
</style>
