<template>
  <div>
    <section class="section">
      <div class="container">
        <div class="card">
          <div class="card-content">
            <p class="title"></p>
            <!-- TODO: Display pretty data -->
            <p>{{ msg }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      msg: 'Home screen for a user will be and entry point to the app doing stuff and such.'
    }
  },
  methods: {
    getGroceries() {
      console.log(sessionStorage.blah);
      this.$http({
        method: 'get',
        url: `/users/${localStorage.current_user_id}/groceries`,
        headers: {
          'Authorization': 'Bearer ' + localStorage.token
        }
      })
        .then((response) => { this.msg = response.data })
        .catch( error => { console.log(error) })
    }
  },
  created() {
    sessionStorage.blah = "Consider using session storage for token and user_id.\nThat might be deleted if you close your browser though.  Maybe useful for a remember_me feature."
    this.getGroceries()
  }
}
</script>
