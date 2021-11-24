<template>
  <v-row id="bg">
    <v-col>
      <!-- back button that will go back to the page it came from  -->
      <v-btn class="pl-9" x-large icon @click="$router.go(-1)">
        <v-icon color="white">mdi-arrow-left</v-icon>
        <v-card-title class="ml-n3" style="color: white">Back</v-card-title>
      </v-btn>
    </v-col>
    <v-col cols="8">
      <v-container fill-height fluid id="bg">
        <div id="clock">
          <v-row class="mb-n9" justify="center">
            <div class="mt-9 mr-9">
              <v-card-title
                id="app_text"
                class="mt-9 mb-9"
                style="font-size: 42px"
                >Fastest Lap</v-card-title
              >
              <v-card-text style="font-size: 54px"
                ><strong>{{ fastestLap }}</strong></v-card-text
              >
            </div>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <div>
              <span id="app_text" style="font-size: 42px">Lap </span
              ><span style="font-size: 9em">
                <strong>{{ lapNumber }}</strong></span
              >
            </div>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <div class="mt-9 ml-9">
              <v-card-title
                id="app_text"
                class="mt-9 mb-9"
                style="font-size: 42px"
                >Average Lap</v-card-title
              >
              <v-card-text style="font-size: 54px"
                ><strong>{{ averageLap }}</strong></v-card-text
              >
            </div>
          </v-row>
          <span class="time">{{ time }}</span>

          <v-row justify="center">
            <v-spacer></v-spacer>
            <v-btn
              x-large
              style="font-size: 4em"
              id="start"
              text
              color="success"
              class="white--text"
              @click="start()"
              >Start Session</v-btn
            >
            <v-spacer></v-spacer>
            <v-btn
              light
              x-large
              style="font-size: 4em"
              v-if="running"
              id="stop"
              text
              class="white--text"
              @click="lap()"
              >Lap</v-btn
            >

            <v-spacer v-if="running"></v-spacer>
            <v-btn
              v-if="running"
              x-large
              style="font-size: 4em"
              id="reset"
              color="error"
              text
              class="white--text"
              @click="reset('end')"
              >End Session</v-btn
            >
            <v-spacer v-if="running"></v-spacer>
          </v-row>
        </div> </v-container
    ></v-col>
    <v-col> </v-col>
    <v-col> </v-col>
    <v-col> </v-col>
    <v-col> </v-col>
    <v-col> </v-col>
    <v-col> </v-col>
    <v-col> </v-col>
    <v-col> </v-col>
    <v-col> </v-col>
  </v-row>
</template>

<script>
export default {
  name: "timer-component",
  props: {
    selectedTrack: {
      type: String,
      default: "",
      required: false,
    },
  },
  data() {
    return {
      time: "00:00.000",
      laps: [],
      latestLap: "",
      snackbar: false,
      timeBegan: null,
      timeStopped: null,
      stoppedDuration: 0,
      started: null,
      running: false,
      fastestLap: "00:00.000",
      averageLap: "00:00.000",
      lapNumber: 1,
      previousLap: 1,
      timeElapsed: 0,
    };
  },
  methods: {
    start() {
      if (this.running) return;

      if (this.timeBegan === null) {
        this.reset();
        this.timeBegan = new Date();
      }

      if (this.timeStopped !== null) {
        this.stoppedDuration += new Date() - this.timeStopped;
      }

      this.started = setInterval(this.clockRunning, 10);
      this.running = true;

      if(this.running === true){
        event.preventDefault();
      }
    },
    stop() {
      this.running = false;
      this.timeStopped = new Date();
      clearInterval(this.started);
    },
    reset(calledFrom) {
      if (calledFrom === "end") {
        if (this.lapNumber == 1) {
          this.laps.push({
            time: this.time,
            lap: this.lapNumber,
            timeDiff: this.timeElapsed.getTime(),
          });
          this.calcAvgAndFastest();
        }
        this.$store.dispatch("addSession", {
          laps: this.laps,
          fastestLap: this.fastestLap,
          avgLap: this.averageLap,
        });
        this.running = false;
        clearInterval(this.started);
        this.stoppedDuration = 0;
        this.timeBegan = null;
        this.timeStopped = null;
        this.time = "00:00.000";
        this.lapNumber = 1;
        this.fastestLap = "00:00.000";
        this.averageLap = "00:00.000";
      } else if (calledFrom === "lap") {
        this.running = false;
        clearInterval(this.started);
        this.stoppedDuration = 0;
        this.timeBegan = null;
        this.timeStopped = null;
        this.time = "00:00.000";
      }
    },
    clockRunning() {
      var currentTime = new Date();
      this.timeElapsed = new Date(
        currentTime - this.timeBegan - this.stoppedDuration
      );
      var min = this.timeElapsed.getUTCMinutes();
      var sec = this.timeElapsed.getUTCSeconds();
      var ms = this.timeElapsed.getUTCMilliseconds();

      this.time =
        this.zeroPrefix(min, 2) +
        ":" +
        this.zeroPrefix(sec, 2) +
        "." +
        this.zeroPrefix(ms, 3);
    },
    zeroPrefix(num, digit) {
      var zero = "";
      for (var i = 0; i < digit; i++) {
        zero += "0";
      }
      return (zero + num).slice(-digit);
    },
    lap() {
      const tempDate = new Date(
        new Date() - this.timeBegan - this.stoppedDuration
      ).getTime();

      this.laps.push({
        time: this.time,
        lap: this.lapNumber,
        timeDiff: this.timeElapsed.getTime(),
      });
      this.lapNumber++;
      this.latestLap = this.time;
      this.calcAvgAndFastest();
      this.reset("lap");
      this.start();
    },
    calcAvgAndFastest() {
      var totalTime = 0;
      for (var i = 0; i < this.laps.length; i++) {
        totalTime += this.laps[i].timeDiff;
      }
      this.fastestLap = this.msToTime(
        Math.min(...this.laps.map((lap) => lap.timeDiff))
      );

      var tempAvgTime = totalTime / this.laps.length;
      this.averageLap = this.msToTime(tempAvgTime);
    },
    msToTime(duration) {
      var milliseconds = parseInt(duration % 1000),
        seconds = parseInt((duration / 1000) % 60),
        minutes = parseInt((duration / (1000 * 60)) % 60),
        minutes = minutes < 10 ? "0" + minutes : minutes;
      seconds = seconds < 10 ? "0" + seconds : seconds;

      return minutes + ":" + seconds + "." + milliseconds;
    },
  },
};
</script>
