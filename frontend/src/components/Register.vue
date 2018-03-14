<template>
  <div class="columns">
    <div class="column is-5">
      <form class="form-signin" @submit.prevent="register">
        <h2 class="subtitle">Register</h2>

        <div class="field">
          <label for="inputUsername" class="label">Username</label>
          <div class="control">
            <input v-model="username" type="text" id="inputUsername" class="input" placeholder="Username" required autofocus>
          </div>
        </div>

        <div class="field">
          <label for="inputEmail" class="label">Email</label>
          <div class="control">
            <input v-model="email" type="text" id="inputEmail" class="input" placeholder="Email" required autofocus>
          </div>
        </div>

        <div class="field">
          <label for="inputPassword" class="label">Password</label>
          <div class="control">
            <input v-model="password" type="password" id="inputPassword" class="input" placeholder="Password" required>
          </div>
        </div>

        <div class="field">
          <label for="inputPassword2" class="label">Confirm Password</label>
          <div class="control">
            <input v-model="password2" type="password2" id="inputPassword2" class="input" placeholder="Confirm Password" required>
          </div>
        </div>

        <div class="field">
          <div class="control">
            <button class="button is-link" type="submit">Register!</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      password2: '',
      email: ''
    }
  },

  methods: {
    register() {
      if (this.password != this.password2) {
        this.registrationFailed()
      }

      this.$http({
        method: 'post',
        url: '/users',
        data: {
          username: this.username,
          email: this.password,
          password: this.password
        }
      })
        .then((response) => this.registrationSuccessful(response))
        .catch(() => this.registrationFailed())
    },

    registrationSuccessful(res) {
      if (!res.data.token) {
        this.registrationFailed()
        return
      }

      localStorage.setItem('token', res.data.token)
      localStorage.setItem('current_user_id', res.data.id)
      this.error = false

      this.$router.replace(this.$route.query.redirect || '/groceries')
    },

    registrationFailed() {
      this.error = 'Login failed!'
      delete localStorage.token
      this.$router.replace(this.$route.query.redirect)
    }
  },

  created() {
    console.log(this.$root.title || "no title")
    // this.$root.title = 'Register'
  }
}
</script>
