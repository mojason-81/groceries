<template>
  <div class="columns">
    <div class="column is-5">
      <form class="form-signin" @submit.prevent="login">
        <h2 class="subtitle">Profile</h2>

        <div class="field">
          <label for="inputUsername" class="label">Username</label>
          <div class="control">
            <input v-model="username" type="text" id="inputUsername" class="input" placeholder="{{ username }}" required autofocus>
          </div>
        </div>

        <div class="field">
          <label for="inputPassword" class="label">Password</label>
          <div class="control">
            <input v-model="password" type="password" id="inputPassword" class="input" placeholder="Password" required>
          </div>
        </div>
        <div class="field">
          <div class="control">
            <button class="button is-link" type="submit">Sign in</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login() {
      this.$http({
        method: 'put',
        url: '/users',
        headers: {
          'Authorization': 'Bearer ' + localStorage.token
        }
      })
        .then((response) => this.loginSuccessful(response))
        .catch(() => this.loginFailed())
    },

    loginSuccessful(res) {
      if (!res.data.token) {
        this.loginFailed()
        return
      }

      localStorage.token = res.data.token
      localStorage.current_user_id = res.data.user_id
      this.error = false

      this.$router.replace(this.$route.query.redirect || '/groceries')
    },

    loginFailed() {
      this.error = 'Update failed!'
      delete localStorage.token
      this.$router.replace(this.$route.query.redirect)
    }
  },
  created() {
    // this.$root.title = 'Update'
  }
}
</script>

