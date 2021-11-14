<template>
  <v-app >
   
    <v-main >
      <router-view />
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
    drawer: false,
    messages: 11,
    show: false,
    fab: false,
    termsDialog: false,
    privacyDialog: false,
    links: ["Support", "Terms", "Privacy Policy"],
  }),
  created() {
    this.$vuetify.breakpoint.mdAndUp
      ? (this.drawer = true)
      : (this.drawer = false);
    this.$vuetify.goTo(0);
  },
  computed: {
    moveIcons() {
      var ret;
      this.$vuetify.breakpoint.mdAndDown ? (ret = true) : (ret = false);
      return ret;
    },
    //...mapState(["userProfile"]),
    showNav() {
      if (this.userProfile != null) {
        var ret = Object.keys(this.userProfile).length > 1;
        return ret;
      }
      return false;
    },
    topStyle() {
      if (this.showNav) {
        return "margin-top:-250px";
      }
      return "";
    },
  },
  methods: {
    onScroll(e) {
      if (typeof window === "undefined") return;
      const top = window.pageYOffset || e.target.scrollTop || 0;
      this.fab = top > 20;
    },
    toTop() {
      this.$vuetify.goTo(0);
    },
    // logout() {
    //   this.$store.dispatch("logout");
    //   this.$vuetify.breakpoint.mdAndUp
    //     ? (this.drawer = true)
    //     : (this.drawer = false);
    // },
    getRouterName() {
      return this.$route.name;
    },
  },
};
</script>

