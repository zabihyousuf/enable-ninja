<template>
  <v-row  justify="center">
    <v-col cols="8">
      <v-container fill-height>
        <v-row></v-row>
        <v-row></v-row>
        <v-row></v-row>
        <v-row class="mb-n9">
          <v-card-title style="font-size: 72px; color: white"
            >SELECT TRACK</v-card-title
          >
        </v-row>
        <v-row class="mt-n9" justify="center">
          <v-select
            v-model="selectedTrack"
            @change="goToTimer()"
            :items="items"
            item-text="trackName"
            item-value="id"
            solo
            outlined
            return-object
            label="CHOOSE A PRESAVED TRACK"
          ></v-select>
        </v-row>
        <v-row></v-row>
        <v-row></v-row>
        <v-row></v-row>
      </v-container>
    </v-col>
  </v-row>
</template>
<script>
export default {
  name: "track-selector",
  data() {
    return {
      selectedTrack: null,
      items: [
        {
          trackName: "SUMMIT POINT MAIN",
          startLong: "",
          startLat: "",
          trackID: 1,
        },
        {
          trackName: "SUMMIT POINT SIDE",
          startLong: "",
          startLat: "",
          trackID: 2,
        },
        { trackName: "NC CAR", startLong: "", startLat: "", trackID: 3 },
        { trackName: "NJ RACE BIKE", startLong: "", startLat: "", trackID: 4 },
      ],
    };
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