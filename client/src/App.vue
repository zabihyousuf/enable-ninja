<template>
  <v-app id="bg">
    <v-main>
      <transition :name="animationName">
        <router-view class="child-view" />
      </transition>
    </v-main>
  </v-app>
</template>

<script>
// import Navbar from './components/navbar.vue';
// import Sidebar from './components/sidebar.vue';
import { mapState } from "vuex";

export default {
  name: "App",
  data: () => ({
    animationName: undefined,
  }),
  created() {
    console.log("App created");
  },
  watch: {
    $route(to, from) {
      const to_depth = to.path.split("/").length;
      const from_depth = from.path.split("/").length;
      this.animationName = to_depth < from_depth ? "fade" : "fade";
    },
  },
  computed: {},
  methods: {},
};
</script>
<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
.child-view {
  /* position: absolute;
  width: 100%;
  left: 0; */
  /* transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1); */
}
/* .slide-left-enter,
.slide-right-leave-active {
  opacity: 0;
  -webkit-transform: translate(30px, 0);
  transform: translate(30px, 0);
}
.slide-left-leave-active,
.slide-right-enter {
  opacity: 0;
  -webkit-transform: translate(-30px, 0);
  transform: translate(-30px, 0);
} */
</style>
