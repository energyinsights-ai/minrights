
  
<template>
    <div class="chart-container" >
        <v-container style="height:100%; width:100%">
            <v-row style="height:100%; width:100%">
                <v-col cols="10">
                    <Chart type="bar" :data="asset_rev_data" :options="asset_rev_options" style="width: 100%; height: 100%" v-if="this.$store.state.asset_prod_data !=undefined"/>
                </v-col>
                <v-col cols="2" style="margin-top:50px">
                    <v-slider
                        v-model="oil_price"
                        :max="100"
                        :min="50"
                        :step="1"
                        thumb-label
                        label="Oil Price"
                    ></v-slider>
                    <v-slider
                        v-model="gas_price"
                        :max="6"
                        :min="1.50"
                        :step=".25"
                        thumb-label
                        label="Gas Price"
                    ></v-slider>
                    <p>$ / NRA: {{ npv }}</p>
                </v-col>
            </v-row>
        </v-container>

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
    import getNPV from '../clients/financials.js'    
    import Chart from 'primevue/chart';
    import store from '../clients/vuex.js';
    export default {
      name: 'AssetRevChart',
      components: {
        Chart
      },
      data() {
        return {
            oil_price:80,
            gas_price:3,
            npv:0

        }
      },
      computed: {
            asset_rev_data() {
                if (this.$store.state.asset_prod_data.datasets == undefined) return;
                else if (this.$store.state.asset_prod_data.datasets.length == 0) return;
                else {
                    let rev_data = store.state.asset_prod_data;
                    let oil_rev = rev_data.datasets[1].data.map((x) => x * this.oil_price);
                    let gas_rev = rev_data.datasets[0].data.map((x) => x * this.gas_price); 
                    let total_rev = oil_rev.map((x,i) => (x + gas_rev[i])/1080*.15);
                    const new_data = {}
                    new_data.labels = rev_data.labels;
                    new_data.datasets = [
                        {
                            label: 'Oil Revenue',
                            data: oil_rev,
                            fill: false,
                            tension: 0.1,
                            backgroundColor:'green'
                        },
                        {
                            label: 'Gas Revenue',
                            data: gas_rev,
                            fill: false,
                            tension: 0.1,
                            backgroundColor:'red'
                        },
                        
                    ]
                    this.$store.commit('set_asset_rev_data',new_data);
                    this.npv = getNPV(.15,0,total_rev);
                    console.log('NPV:',this.npv)
                    return new_data;
                }
            },
            asset_rev_options() { return {
                responsive: true,
                maintainAspectRatio: false,
              
                scales:{
                    y: {
                        type: 'linear',
                        display: 'auto',
                        position: 'left',
                        stacked: true
    
                    },
                    x:{stacked:true}
                }
            }}
        }
        }
      </script>