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

new Vue({
    router,
    vuetify,
    store,
    render: (h) => h(App),
}).$mount('#app');

require('./assets/scss/app.scss')