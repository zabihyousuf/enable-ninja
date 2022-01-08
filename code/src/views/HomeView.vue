<template>
  <v-app>
    <loading></loading>
    <v-layout style="overflow: hidden !important" id="bg">
      
      <home-track-selector></home-track-selector>
    </v-layout>
  </v-app>
</template>

<script>
import HomeTrackSelector from "../components/home/home-track-selector.vue";
import Loading from "../components/shared/loading.vue";
export default {
  title: "Home-Enable-Ninja",
  components: { Loading, HomeTrackSelector },
  data() {
    return {};
  },
  created() {
    // call store method for index page that will check to see if the results contain an associated account
    // if not, it will redirect to a page that says to register the device
    this.onCreated();
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