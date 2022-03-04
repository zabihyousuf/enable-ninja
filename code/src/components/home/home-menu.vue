<template>
  <v-row justify="center">
    <v-container fill-height fill-width>
      <v-row justify="center">
        <v-row class="mb-n4 ml-n9">
          <v-card-title style="font-size: 72px; color: white"
            >TIMER MENU</v-card-title
          >
        </v-row>
      </v-row>
      <v-row  v-for="item in navItems" :key="item.title" >
        <v-list-item link>
          <v-list-item-icon>
            <v-icon class="white--text">{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title class="white--text">{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-row>
    </v-container>
  </v-row>
</template>
<script>
export default {
  name: "track-selector",
  data() {
    return {
      selectedTrack: null,
      navItems: [
        { title: "Lap Timer", icon: "clock-fast", route: "/Timer" },
        { title: "Connect to Wifi", icon: "clock-fast", route: "/Timer" },
      ],
    };
  },
  computed: {
    getError() {
      return this.$store.state.errorOnPage;
    },
  },
  methods: {
    goToTimer() {
      this.$router.push({
        name: "Timer",
        params: {
          selectedTrack: this.selectedTrack,
        },
      });
    },
  },
};
</script>