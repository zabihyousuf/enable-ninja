import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        sessions: [],
        apiUrl: 'http://localhost:5000/api/v1/',
    },
    mutations: {
        set(state, payload) {
            state[payload[0]] = payload[1];
        },
        addSesh(state, payload) {
            state.sessions.push(payload);
        }
    },
    getters: {

    },
    actions: {
        async addSession({ commit, dispatch }, form) {
            axios.defaults.headers.post['Content-Type'] = 'application/json;charset=utf-8';
            axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
            var today = new Date();
            var dd = String(today.getDate()).padStart(2, '0');
            var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
            var yyyy = today.getFullYear();

            today = mm + '/' + dd + '/' + yyyy;
            var tempSesh = {
                sessionDate: today,
                laps: form.laps,
                fastestLap: form.fastestLap,
                avgLap: form.avgLap,
            }
            commit('addSesh', tempSesh);
            var path = `${this.state.apiUrl}add-session`
                // var bodyFormData = new FormData();
                // bodyFormData.append('form', this.state.sessions);
            axios.post(path, { form: this.state.sessions })
                .then(function(response) {
                    commit('set', ['sessions', []]);
                    console.log(response);
                })
                .catch(function(error) {
                    console.log(error);
                });
        },
    },
    modules: {}
})