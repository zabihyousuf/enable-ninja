<template>
  <v-app>
      <timer-component  id="bg" ></timer-component>

  </v-app>
</template>

<script>
import TimerComponent from '../components/timer/timer-component.vue';
export default {
  name: "Timer",
  components: {
    TimerComponent,
  },
  data() {
    return {

    };
  },
  created(){
    console.log("Timer created");
    this.onTimerCreated();
  },
  methods: {
    async onTimerCreated(){
      this.$store.dispatch("getRaceTrack");
    },
  },
};
</script>