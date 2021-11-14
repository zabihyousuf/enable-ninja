<template>
  <v-app>
    <v-layout>
      <timer-component  id="bg" ></timer-component>
    </v-layout>

  </v-app>
</template>

<script>
import TimerComponent from '../components/timer/timer-component.vue';
export default {
  name: "App",
  components: {
    TimerComponent,
  },
  data() {
    return {

    };
  },
  methods: {
  },
};
</script>