<template>
  <div id="app">
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h2 class="title">This is in App.vue</h2>
        </div>
      </div>
    </section>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style lang="scss">
  @import '~bulma/bulma'
</style>
