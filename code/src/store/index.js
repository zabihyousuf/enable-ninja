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
        errorOnPage: false,
        getWifiNames: [],
        trackLatitude: 0,
        trackLongitude: 0,
        trackName: '',

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
        async addSession({ commit, }, form) {
            commit('set', ['loading', true]);
            commit('set', ['errorOnPage', false]);
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
                    commit('set', ['errorOnPage', true]);
                    commit('set', ['loading', false]);
                });
        },
        async checkForAccount({ commit, getters }) {
            commit('set', ['loading', true]);
            commit('set', ['errorOnPage', false]);
            var path = `${this.state.apiUrl}/checkForAccount`
            if (getters.getAccountChecked == false) {
                axios.get(path)
                    .then(function(response) {
                        console.log(response);
                        if (response.data.success) {
                            commit('set', ['accountExists', true]);
                        }
                        commit('set', ['accountChecked', true]);
                    })
                    .catch(function(error) {
                        console.log(error);
                        commit('set', ['errorOnPage', true]);
                    });
            }
            commit('set', ['loading', false]);
        },
        async wifiConnection({ commit, getters }) {
            commit('set', ['loading', true]);
            commit('set', ['errorOnPage', false]);
            var path = `${this.state.apiUrl}/getWifiNames`
            if (getters.getAccountChecked == false) {
                axios.get(path)
                    .then(function(response) {
                        console.log(response);
                        commit('set', ['getWifiNames', []]);
                    })
                    .catch(function(error) {
                        console.log(error);
                        commit('set', ['errorOnPage', true]);
                    });
            }
            commit('set', ['loading', false]);
        },
        async getRaceTrack({ commit }) {
            commit('set', ['loading', true]);
            commit('set', ['errorOnPage', false]);
            var path = `${this.state.apiUrl}/getRaceTrack`

            axios.get(path)
                .then(function(response) {
                    console.log(response);
                    commit('set', ['trackLatitude', response.data.latitude]);
                    commit('set', ['trackLongitude', response.data.longitude]);
                    commit('set', ['trackName', response.data.name]);
                })
                .catch(function(error) {
                    console.log(error);
                    commit('set', ['errorOnPage', true]);
                });

            commit('set', ['loading', false]);
        }
    },
    modules: {}
})