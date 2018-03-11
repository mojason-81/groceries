<template>
  <div>
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h2 class="title">Page Title Goes Here</h2>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="card">
          <div class="card-content">
            <p class="title"></p>
            <!-- TODO: Decide what goes here and get that info from API & display -->
            <p class='subtitle'>{{ msg }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'Home',
    data () {
      return {
        msg: 'Home screen for a user will be and entry point to the app doing stuff and such.'
      }
    },
    methods: {
      doSomething () {
        this.msg = this.getSomething()
      },
      getSomething () {
        const path = `http://localhost:5000/api/users/1/menus`
        axios.get(path,
          {
            // FIXME: Don't hard code a token.  user must sign in via the front end, getting a token,
            // and storing it in the session.  Supply token here from that session.
            headers: { "Authorization":  "Bearer " + "Cw/wmgcchnJtNnUmCAg9G6s9GFOCIbe/" }
          }
        ).then(
          response => {
            this.msg = response.data
          }).catch(
            error => {
              console.log(error)
            })
      }
    },
    created () {
      this.doSomething()
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
    margin: 0 10px;
  }
  a {
    color: #42b983;
  }
</style>
