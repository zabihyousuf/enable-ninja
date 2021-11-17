import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        sessions: [],
        apiUrl: 'http://localhost:5000/api/v1',
        currentSession: {},
        accountExists: false,
        loading: false,
        accountChecked: false,
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
        get(state) {
            return state;
        },
        getSesh(state) {
            return state.sessions;
        },
        getAccountChecked(state) {
            return state.accountChecked;
        }

    },
    actions: {
        async addSession({ commit, dispatch, getters }, form) {
            commit('set', ['loading', true]);
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
            var path = `${this.state.apiUrl}/add-session`
                // var bodyFormData = new FormData();
                // bodyFormData.append('form', this.state.sessions);
            axios.post(path, { form: this.state.sessions })
                .then(function(response) {
                    commit('set', ['sessions', []]);
                    console.log(response);
                    commit('set', ['loading', false]);
                })
                .catch(function(error) {
                    console.log(error);
                    commit('set', ['loading', false]);
                });
        },
        async checkForAccount({ commit, dispatch, getters }) {
            commit('set', ['loading', true]);
            var path = `${this.state.apiUrl}/index`
            if (getters.getAccountChecked == false) {
                axios.get(path)
                    .then(function(response) {
                        console.log(response);
                        if (response.data.success) {
                            commit('set', ['accountExists', true]);
                        }
                        commit('set', ['accountChecked', true]);
                        commit('set', ['loading', false]);
                    })
                    .catch(function(error) {
                        console.log(error);
                        commit('set', ['loading', false]);
                    });
            }
            commit('set', ['loading', false]);
        }
    },
    modules: {}
})