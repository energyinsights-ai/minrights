<template>
    <v-btn @click="openDialog" size="small">Add Wells</v-btn>
</template>
  
<script>

export default {
    name: 'ModalButton',
    methods: {
        openDialog() {
            this.$emit('open-dialog');
        }
    }
    };
  </script>
