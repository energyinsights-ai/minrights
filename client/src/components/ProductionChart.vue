
  
<template>
<div class="chart-container" >
    <Chart type="line" :data="asset_prod_data" :options="chartOptions" style="width: 100%; height: 100%"/>
</div>
</template>
<style>
.chart-container {
  position: relative;
  height: 100%;
  width: 100%;
}
</style>
<script>

import Chart from 'primevue/chart';
import { mapState } from 'vuex'; 
export default {
  name: 'AssetProdChart',
  components: {
    Chart
  },
  data() {
    return {
    }
  },
  computed: {
    ...mapState(['asset_prod_data']),
      
        chartOptions() { return {
            responsive: true,
            maintainAspectRatio: false,
          
            scales:{
                y: {
                    type: 'linear',
                    display: 'auto',
                    position: 'left',

                },
                y1: {
                    type: 'linear',
                    display: 'auto',
                    position: 'right',
                },
            }
        }}
    }
    }
  </script>
  