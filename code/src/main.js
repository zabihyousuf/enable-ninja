import Vue from 'vue';
import Vuex from 'vuex';
import VueRouter from 'vue-router';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import store from './store';

Vue.use(VueRouter);
Vue.use(Vuex);
Vue.use(vuetify)
Vue.config.productionTip = false;
const DEFAULT_TITLE = 'Enable-Ninja-Repo';
router.afterEach((to, from) => {
    // Use next tick to handle router history correctly
    // see: https://github.com/vuejs/vue-router/issues/914#issuecomment-384477609
    Vue.nextTick(() => {
        document.title = to.meta.title || DEFAULT_TITLE;
    });
});
new Vue({
    router,
    vuetify,
    store,
    render: (h) => h(App),
}).$mount('#app');

require('./assets/scss/app.scss')
require('fs')