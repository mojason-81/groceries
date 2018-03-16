<template>
  <div id="app">
    <nav class="navbar" role="navigation">
      <a class="navbar-item" href="#">
        Feed The Family
      </a>

      <div class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link">
          Stuff Is Right Here
        </a>

        <div class="navbar-dropdown">
          <a class="navbar-item" href="#">
            Groceries
          </a>
          <a class="navbar-item" href="#">
            Menus
          </a>
          <a class="navbar-item" href="#">
            Meals
          </a>
          <a class="navbar-item" href="#">
            Stores
          </a>
          <hr v-if="loggedIn()" class="navbar-divider">
          <a v-if="loggedIn()" class="navbar-item">
            Profile
          </a>
          <a v-if="loggedIn()" v-on:click="logOut()" class="navbar-item">
            Log Out
          </a>
        </div>
      </div>
    </nav>

    <section class="hero is-primary">
      <div class="hero-body">
        <p class="title">
          {{ $root.title || "$root.title didn't show up" }}
        </p>
        <p class="subtitle">
          Some subtitle goes here?
        </p>
      </div>
    </section>

    <section class="section">
      <router-view>
      </router-view>
    </section>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      title: 'This needs fixed',
      groceries: '',
      stores: ''
    }
  },

  methods: {
    loggedIn() {
      console.log("loggedIn Called")
      if (localStorage.token != null && localStorage.current_user_id != null) {
        return true
      }
      return false
    },

    logOut() {
      this.$http({
        method: 'delete',
        url: '/tokens',
        headers: {
          'Authorization': 'Bearer ' + localStorage.token
        }
      })
        .then((response) => { this.logOutSuccessful(response) })
        .catch((error) => { this.logoutFailed(error) })
    },

    logOutSuccessful(res) {
      // TODO: Flash success message
      localStorage.removeItem('token')
      localStorage.removeItem('current_user_id')
      this.error = false
      this.$router.replace(this.$route.query.redirect || '/login')
    },

    logoutFailed(e) {
      console.log(e)
      localStorage.removeItem('token')
      localStorage.removeItem('current_user_id')
    }
  }
}
</script>

<style lang="scss">
@import '~bulma/bulma'
</style>
