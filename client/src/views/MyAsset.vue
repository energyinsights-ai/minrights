<template>
    <div style="height:100vh">
        <Navbar
        :userData="userData"
        />
        <AddWellModal :dialog="dialog" @close-dialog="dialog = false"/>
        <v-container style="height:90%">
            <v-row style="height:100%;">
                <v-col style="height:100%" cols="4">
                    <div class="d-flex flex-column justify-center align-center">
                        <h4 class="uppercase font-bold">Well List</h4>
                        <ModalButton @open-dialog="dialog = true" class="mt-3"/>
                        <WellTable :wells="asset_wells" class="mt-3"/>
                    </div>
                    
                </v-col>
                <v-col cols="8">
                    <v-container style="height:100%">
                        <v-row style="height:50%">
                            <v-col style="height:100%">
                                <AssetProdChart v-if="$store.state.asset_wells.length>0"/>
                            </v-col>
                        </v-row>
                        <v-row style="height:50%">
                            <v-col style="height:100%">
                                <AssetRevChart v-if="$store.state.asset_wells.length>0"/>
                            </v-col>
                        </v-row>
                    </v-container>

                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
import AssetProdChart from '../components/ProductionChart.vue';
import WellTable from '../components/WellTable.vue';
import Navbar from '../components/navbar/Navbar.vue'
import AssetRevChart from '../components/AssetRevenue.vue'
import ModalButton from '../components/ModalButton.vue';

import { supabase } from "../clients/supabase";
import AddWellModal from '../components/AddWellModal.vue';
const { data: { user } } = await supabase.auth.getUser()
const initials = user.user_metadata.firstName[0] + user.user_metadata.lastName[0]
const fullName = user.user_metadata.firstName + ' ' + user.user_metadata.lastName
const email = user.email
const user_id = user.id


export default {
    name: 'MyAsset',
    components: {AssetProdChart,Navbar,WellTable,AssetRevChart,ModalButton,AddWellModal},
    data() {
        return {
            userData: {
                initials: initials,
                fullName: fullName,
                email: email,
                user_id: user_id
            },
            dialog: false,
            write_wells:null
        }
    },
    async created() {
        await this.$store.commit('set_user',{user:this.userData});
        this.$store.dispatch('load_assets',{});
    },
    computed:{
        asset_wells(){
            return this.$store.state.asset_wells;
        },
        loadAssetsOnSuccess() {
            if (this.write_wells === 'success') {
                print('loading assets')
                this.$store.dispatch('load_assets', { user_id: user.id });
            }
        }
    },
    methods:{
        watchStore(){
            this.$store.watch(
                () => this.$store.getters.write_wells,
                data => this.write_wells = data)

        }
    },
    mounted(){
        this.watchStore();
    }

};
</script>

<style>

</style>