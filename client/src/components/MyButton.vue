
<template>
    <button @click="navigate">{{ label }}</button>
  </template>
  
  <script>
  export default {
    props: {
      to: {
        type: String,
        required: true
      },
      label: {
        type: String,
        required: true
      }
    },
    methods: {
      navigate() {
        this.$router.push(this.to);
      }
    }
  };
  </script>

