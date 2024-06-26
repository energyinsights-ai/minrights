
<template>
	<v-sheet class="mx-auto" width="300">
	  <v-card-title class="headline">Login</v-card-title>
	  <v-form @submit.prevent="'submit'">
		<v-text-field
		  v-model="email"
		  label="Email"
		></v-text-field>
    <v-text-field type="password" v-model="password"> </v-text-field>
    <v-btn
        :loading="loading"
        class="mt-2"
        text="Submit"
        block
        @click="submit"
      ></v-btn>

	  </v-form>
    <h6 style="color:red; margin:auto; margin-top:30px; text-align:center">{{ error }}</h6>
    <h6 style="margin:auto; margin-top:30px; text-align:center">Don't have an account?</h6>
    <v-btn type="link" block to="/register">Register</v-btn>
	</v-sheet>
  </template>

<script>
import MyButton from '../MyButton.vue';
import { supabase } from "../../clients/supabase";
import { c } from 'naive-ui';
export default {
  data() {
    return {

        email: '',
        password: '',
        loading: false,
        error: null,

    }
  },
  methods: {
    async submit(event) {
      try {
        const { data, error } = await supabase.auth.signInWithPassword({
        email: this.email,
        password: this.password
      })
      if (error)
      {
        console.log(error);
      }
      else
      {
        this.$router.push('/myasset');
      }
      }
      catch (error) {
        console.log(error);
        this.error=error.message;
      }
      finally {
        this.error='ERROR: Invalid email or password. Please try again.';
      }


    }
  },
  components: {
    MyButton
  }
}
</script>