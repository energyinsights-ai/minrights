<template>

        <v-data-table
        :items="wells" 
        :headers="headers" 
        :loading="loading"
        item-value="api"
        v-model="selected"
        height="300px"
        show-select
        return-object
        select-strategy="single"
        v-if="wells.length > 0"
        >
        
      </v-data-table>
      <h1>{{ selected }}</h1>
</template>
  <script>
  export default {
    name: 'WellTable',
    props: ['wells'],
    data() {
      return {
        loading: false,
        selected:[],
        headers: [
        {'title':'API','value':'api','key':'api'},
        {'title':'Well Name','value':'well_name'},
        {'title':'Operator','value':'operator'},
        {'title':'State','value':'state'},
        {'title':'County','value':'county'},
        {'title':'Legal','value':'trs'}

      ]
      }
    },
    // created() {
    //   this.fetchData();

    watch: {
      selected(newVal) {
        console.log('selected')
        if (newVal.length > 0){
          this.$store.dispatch('load_assets',newVal[0])
        }
        else {
          this.$store.dispatch('load_assets',{})}
          
        
      }
    },
  }
  </script>