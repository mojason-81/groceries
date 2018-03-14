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
          <hr class="navbar-divider">
          <a class="navbar-item" href="#">
            Profile
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
      title: 'This needs fixed'
    }
  }
}
</script>

<style lang="scss">
@import '~bulma/bulma'
</style>
