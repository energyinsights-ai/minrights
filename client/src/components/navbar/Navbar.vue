<template>
    <v-toolbar
    color="black"
    >
    <v-img
            src="../assets/logo.png"
            style="display:block"
            >
          </v-img>
      <v-toolbar-title>


      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-xs-only">
        <v-btn
          flat
          v-for="item in menuItems"
          :key="item.title"
          :to="item.path">
          <v-icon left dark class="mr-3">{{ item.icon }}</v-icon>
          {{ item.title }}
        </v-btn>
        <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props" class="mr-2">
            <v-avatar color="brown" size="large">
              <span class="text-h5">{{ initials }}</span>
            </v-avatar>
          </v-btn>
        </template>
        <v-card>
          <v-card-text>
            <div class="mx-auto text-center">
              <v-avatar color="brown">
                <span class="text-h5">{{ initials }}</span>
              </v-avatar>
              <h3>{{ fullName }}</h3>
              <p class="text-caption mt-1">{{ email }}</p>
              <v-divider class="my-3"></v-divider>
              <v-btn variant="text" :to="{ name: 'login'}"  rounded> Logout </v-btn>
            </div>
          </v-card-text>
        </v-card>
    </v-menu>
      </v-toolbar-items>
    </v-toolbar>
  </template>
  <script>

export default {


    name: "NavBar",
    props:['userData'],

    data(){
      return {

        initials:this.userData.initials,
        fullName:this.userData.fullName,
        email:this.userData.email,
        appTitle: 'Mineral Rights',
        sidebar: false,
        menuItems: [
            { title: 'Home', path: '/myasset', icon: 'fas fa-home' },
            { title: 'Add Wells', path: '/add_wells', icon: 'fa-solid fa-folder-plus' },
            { title: 'Evaluations', path: '/evaluation', icon: 'fa-solid fa-magnifying-glass-chart' },
       ]
      }
    },
  };
  </script>
  <style>
  
  </style>