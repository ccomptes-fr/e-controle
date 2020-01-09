import '@babel/polyfill'
import './utils/polyfills.js'

import { store } from './store'
import QuestionnaireCreate from './questionnaires/QuestionnaireCreate.vue'
import Vue from 'vue/dist/vue.js'
import Vuex, { mapActions } from 'vuex'

Vue.use(Vuex)

// eslint-disable-next-line no-new
new Vue({
  store,
  el: '#questionnaire-create-vm',
  components: {
    QuestionnaireCreate,
  },
  methods: {
    ...mapActions(['loadConfig', 'fetchControls', 'fetchSessionUser']),
  },
  created() {
    this.loadConfig()
    this.fetchControls()
    this.fetchSessionUser()
  },
})
