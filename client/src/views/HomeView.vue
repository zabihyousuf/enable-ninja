<template>
  <v-app>
    <v-layout> </v-layout>
  </v-app>
</template>

<script>
export default {
  name: "Home",
  components: {},
  data() {
    return {};
  },
  created() {
    // call store method for index page that will check to see if the results contain an associated account
    // if not, it will redirect to a page that says to register the device 
    await this.onCreated();
  },
  mounted() {},
  methods: {
    async onCreated() {
      // call store method for index page that will check to see if the results contain an associated account
      // if not, it will redirect to a page that says to register the device 
      this.$store.dispatch("checkForAccount");
    },
  },
};
</script>