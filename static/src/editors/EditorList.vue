<template>
<div class="card-body" v-if="users && users.length">
  <ul class="list-unstyled list-separated">
    <li class="list-separated-item" v-for="(user, index) in users" :key="index">
      <div class="flex-row align-items-center">
        <div class="flex-column mr-4">
          <span class="avatar avatar-pink">{{ user.first_name.charAt(0) }}{{ user.last_name.charAt(0) }}</span>
        </div>
        <div class="flex-column mr-4 flex-grow-1">
          <div>{{ user.first_name }} {{ user.last_name }}</div>
          <small><a :href="'mailto:' + user.email">{{ user.email }}</a></small>
        </div>
          <div class="flex-column mr-4">
            <button
              class="btn btn-secondary"
              title="Transférer"
              @click="swapEditor(user)">
                <span class="fa fa-exchange-alt mr-2" aria-hidden="true"></span>
                Transférer
            </button>
          </div>
      </div>
    </li>
  </ul>
</div>
</template>

<script>
import Vue from 'vue'

export default Vue.extend({
  props: {
    users: Array,
    questionnaireId: Number,
  },
  methods: {
    swapEditor(user) {
      this.$emit('swap-editor', user)
    },
  },
})
</script>

<style></style>
