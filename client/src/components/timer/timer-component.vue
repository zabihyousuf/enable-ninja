<template>
  <v-row id="bg">
    <v-col></v-col>
    <v-col>
      <v-container fill-height fluid id="bg">
        <div id="clock">
          <v-row class="mb-n9" justify="center">
            <div class="mt-9">
              <v-card-title style="font-size: 18px">Fastest Lap</v-card-title>
              <v-card-text style="font-size: 24px"
                ><strong>{{ fastestLap }}</strong></v-card-text
              >
            </div>
            <v-spacer></v-spacer>
            <div>
              <span style="font-size: 24px">Lap </span
              ><span style="font-size: 6em">
                <strong>{{ lapNumber }}</strong></span
              >
            </div>
            <v-spacer></v-spacer>
            <div class="mt-9">
              <v-card-title style="font-size: 18px">Average Lap</v-card-title>
              <v-card-text style="font-size: 24px"
                ><strong>{{ averageLap }}</strong></v-card-text
              >
            </div>
          </v-row>
          <span class="time">{{ time }}</span>

          <v-row justify="center">
            <v-spacer></v-spacer>
            <v-btn
              style="font-size: 2em"
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
              v-if="running"
              style="font-size: 2em"
              id="stop"
              text
              class="white--text"
              @click="lap()"
              >Lap</v-btn
            >

            <v-spacer v-if="running"></v-spacer>
            <v-btn
              v-if="running"
              style="font-size: 2em"
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
  </v-row>
</template>

<script>
export default {
  name: "timer-component",
  props: {
    longitude: {
      type: Number,
      default: 0,
      required: false,
    },
    latitude: {
      type: Number,
      default: 0,
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
    },
    stop() {
      debugger;
      this.running = false;
      this.timeStopped = new Date();
      clearInterval(this.started);
    },
    reset(calledFrom) {
      if (calledFrom === "end") {
        
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
      var currentTime = new Date(),
        timeElapsed = new Date(
          currentTime - this.timeBegan - this.stoppedDuration
        ),
        min = timeElapsed.getUTCMinutes(),
        sec = timeElapsed.getUTCSeconds(),
        ms = timeElapsed.getUTCMilliseconds();

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
        timeDiff: tempDate,
      });
      this.lapNumber++;
      this.latestLap = this.time;
      this.calculateAverage();
      this.reset("lap");
      this.start();
    },
    calculateAverage() {
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
