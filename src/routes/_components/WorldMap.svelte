<script>
  import { Svg } from 'layercake';
  import { feature } from 'topojson-client';
  import { geoPath, geoIdentity } from 'd3-geo';

  export let width;
  export let height;

  import worldData from '../_data/land-50m.json';

  const geojson = feature(worldData, worldData.objects.countries);
  $: projection = geoIdentity()
    .reflectY(true)
    .fitSize([width, height], geojson);
  $: path = geoPath(projection);
      
</script>

<Svg>
  <g>
    {#each geojson.features as feature}
      <path d={path(feature)} fill="#ccc" stroke="#333" />
    {/each}
    {#each geojson.features as feature}
      <text
        x={path.centroid(feature)[0]}
        y={path.centroid(feature)[1]}
        font-size="15"
        text-anchor="middle"
        fill="#333"
      >
        {feature.properties.name}
      </text>
    {/each}
  </g>
</Svg>
