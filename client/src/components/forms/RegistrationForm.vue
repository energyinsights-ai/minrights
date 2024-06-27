<template>
	<v-sheet class="mx-auto" width="300">
	  <v-card-title class="headline">MineralRights.AI Registration</v-card-title>
	  <v-form>
		<v-text-field
		  v-model="firstName"
		  label="First name"
		></v-text-field>
		<v-text-field
		  v-model="lastName"
		  label="Last name"
		></v-text-field>
		<v-text-field
		  v-model="email"
		  label="Email"
		></v-text-field>
		<v-text-field type="password" v-model="password"> </v-text-field>
		<v-btn class="mt-2" @click="createAccount" block>Register</v-btn>
	  </v-form>
	</v-sheet>
  </template>
  
<script>
  	import axios from 'axios';
	import { supabase } from "../../clients/supabase";
	
	export default {
		data() {
		return {
			firstName:"",
			lastName:"",
			email:"",
			password:"",
		}
		},
		methods: {
			async createAccount() {
				console.log(this.password)
				const { data, error } = await supabase.auth.signUp({
					
					email: this.email,
					password: this.password,
					
					options: {
						data: {
							firstName: this.firstName,
							lastName: this.lastName


						}
					}
				})
				const my_id = data.user.id
				
				// const response = await axios.post('http://0.0.0.0:5000/register', {
				// 	'id': my_id,
				// 	'first_name': this.firstName,
				// 	'last_name': this.lastName,
				// 	'email': this.email
				// })
				// alert('Account created, please login')
				// this.$router.push('/login');
			}
		}
	}
</script>