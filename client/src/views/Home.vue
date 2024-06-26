
<script>
import Button from '../components/MyButton.vue';
export default {
  components: {
    Button
  }
};
</script>
<template>

    <div class="container w-screen">
      <h1 class="font-bold">
        Chose your path
      </h1>
      <div class="flex">
          <Button to="/myasset" label="Asset Tracking" class="flex-auto border border-sky-500"/>
          <Button to="/evaluation" label="Insant Eval" class="flex-auto border border-sky-50"/>

        </div>
    </div>
</template>