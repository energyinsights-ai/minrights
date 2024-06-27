<template>
    <div>
        <v-dialog v-model="dialogVisible" width="auto">
            <v-sheet width="auto" height="auto" class="p-3">
                <v-form @submit.prevent="'submit'">
                <v-textarea label="Paste in API (14 digit)" v-model="apis"></v-textarea>
                <v-row>
                    <v-col>
                        <div class="flex justify-start">
                            <v-btn
                                text="Find Wells"
                                :loading="find_wells_loading"
                                @click="submit"
                                v-if="apis.length>0"
                                ></v-btn>
                            <v-btn
                                class="ml-2"
                                text="Add Wells"
                                @click="loadwells"
                                :loading="loading"
                                v-if="$store.state.wells.length>0"></v-btn>
                        </div>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col>
                        <v-data-table
                        :items="wells" 
                        :headers="headers" 
                        :loading="loading"
                        item-value="api"
                        @input="handleSelection"
                        height="300px"
                        select-strategy="single"
                        v-if="wells.length > 0"
                        >
                        </v-data-table>
                    </v-col>
                </v-row>
                </v-form>
            </v-sheet>
        </v-dialog>
    </div>
</template>

<script>
import axios from 'axios';
import { supabase } from "../clients/supabase";

const { data: { user } } = await supabase.auth.getUser()
const initials = user.user_metadata.firstName[0] + user.user_metadata.lastName[0]
const fullName = user.user_metadata.firstName + ' ' + user.user_metadata.lastName
const email = user.email

export default {
    data() {
        return {
    
            apis:[],
            find_wells_loading: false,
            loading: false,
            userData: {
                initials: initials,
                fullName: fullName,
                email: email
            },
            wells: [],
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
  props: {
    dialog: {
      type: Boolean,
      required: true
    }
  },
  computed: {
    dialogVisible: {
      get() {
        return this.dialog;
      },
      set(value) {
        this.$emit('close-dialog', value);
      }
    },
    
  },
  methods: {
    closeDialog() {
      this.$emit('close-dialog', false);
      this.apis=[]
      this.wells=[]
    },
    async submit(event) {
        this.find_wells_loading = true
        await this.$store.dispatch('get_wells', {apis:this.apis,user_id:user.id})
        this.wells = this.$store.state.wells
        this.find_wells_loading = false

    },
    async loadwells(event) {
        // this.loading = true
        // await axios.post('http://0.0.0.0:5000/addwells', {wells:this.$store.state.wells,user_id:user.id})
        // .then(response => {
        //     this.$store.commit('run_wells',response.data)
        // })
        // this.loading = false
        // this.$store.dispatch('load_assets')
        // this.closeDialog()
    }
    
  },
  watch:{
    dialog(){
        if (this.dialog === false){
            this.apis = []
            this.wells = []
            this.$store.commit('clear_wells')
        }
    }
  }
};
</script>
<style>
/* Add any custom styles here */
</style>