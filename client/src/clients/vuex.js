
import { createStore } from 'vuex'
import axios from 'axios';
import { set } from 'ol/transform';



// Create a new store instance.
const store = createStore({
    state:{
        prodData : {
        },
        wells:[],
        write_wells:"",
        asset_wells:[],
        asset_prod_data:{},
        asset_rev_data:[],
        user:null,
        selected_wells:null
    },
    mutations:{

        set_wells(state, payload){
            state.wells = payload            
        },
        run_wells(state, payload){
            state.write_wells = payload
        },
        set_asset_wells(state, payload){
            state.asset_wells = payload
        },
        set_asset_prod_data(state, payload){
            state.asset_prod_data = payload
        },
        set_asset_rev_data(state, payload){
            state.asset_rev_data = payload
        },
        set_prod_data(state,payload){
            state.prodData = payload
        },
        set_user(state, payload){
            state.user = payload
        },
        clear_wells(state){
            state.wells = []
        },
        set_selected_wells(state, payload){
            state.selected_wells = payload
        }

    },
    actions:{
        async get_wells({commit}, payload){

            const response = await axios.get('https://0.0.0.0:5000/lookup_wells', {responseType:'json','params':{
                'apis': payload.apis,
                'user_id': payload.user_id}});
            commit('set_wells', response.data);

        },
        async load_assets({commit},payload){
            const response = await axios.get('https://0.0.0.0:5000/get_assets', {responseType:'json',headers:{'Content-Type':'application/json'},'params':{
                'user_id': this.state.user.user.user_id,'api':payload.api}});
            console.log(response.data);
            commit('set_asset_wells', response.data.well_data);
            commit('set_asset_prod_data', response.data.prod_data);
            
        },
        set_rev_data({commit}, payload){
            commit('set_asset_rev_data', payload)
        },

    },
    modules:{},
    getters:{
        get_write_wells(state){
            return state.write_wells
        }
    }
  
})
export default store;