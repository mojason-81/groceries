<template>
  <div>
    <section class="section">
      <div class="container">
        <div class="card">
          <div class="card-content">
            <p class="title"></p>
            <p class="subtitle">Add a button to "Add Grocery"</p>
            <!-- TODO: Display pretty data -->
            <p>{{ msg }}</p>
            <!--
            <hr>
            <p>{{ groceryData }}</p>
            <hr>
            <p>{{ storeData }}</p>
            <hr>
            -->
            <hr>
            <table id='grocery-table' class='table is-striped is-hoverable'>
              <th class='th'>
                Name
              </th>
              <th class='th'>
                Price
              </th>
              <th class='th'>
                Count
              </th class='th'>
              <tr v-for="item in groceryData.items" class="tr">
                <td class="td">
                  {{ item.name }}
                </td>
                <td class="td">
                  ${{ item.price / 100 }}
                </td>
                <td class="td">
                  {{ item.count }}
                </td>
              </tr>
            </table>
            <hr>
            <div :class="display">
              TODO: Grocery form goes here<br>
              TODO: Add multiple groceries at once.
              <button v-on:click="addGrocery()">
                Faux submit button
              </button>
            </div>
            <button v-on:click="exposeGroceryForm()">
              Add Grocery
            </button>
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
      msg: 'Home screen for a user will be an entry point to the app doing stuff and such I think maybe.',
      groceryData: '',
      storeData: '',
      display: 'is-hidden',
      grocery_name: 'rice',
      grocery_price: '1.49',
      grocery_count: '1',
      store_id: '1'
    }
  },

  methods: {
    getGroceries() {
      // maybe post to something like /users/:id/:store_id/groceries
      this.$http({
        method: 'get',
        url: `/users/${localStorage.current_user_id}/groceries`,
        headers: {
          'Authorization': 'Bearer ' + localStorage.token
        }
      })
        .then((response) => { this.setGroceryData(response) })
        .then(() => { this.getStores() })
        .catch((e) => this.flashSomeKindOfError(e))
    },

    addGrocery() {
      this.$http({
        method: 'post',
        url: `/users/${localStorage.current_user_id}/groceries`,
        headers: {
          'Authorization': 'Bearer ' + localStorage.token
        },
        data: {
          name: this.grocery_name,
          price: this.grocery_price,
          count: this.grocery_count,
          store_id: this.store_id
        }
      })
        .then((res) => this.addToGroceryData(res))
        .catch((e) => this.flashSomeKindOfError(e))
    },

    // The data here should probably be computed properties.
    // Hopefully it will refresh on page refresh
    getStores() {
      var uid = localStorage.current_user_id;
      var tkn = localStorage.token;
      this.$http({
        method: 'get',
        url: `/users/${localStorage.current_user_id}/stores`,
        headers: {
          'Authorization': 'Bearer ' + localStorage.token
        }
      })
        .then((response) => this.setStoreData(response))
        .catch((e) => this.flashSomeKindOfError(e))
    },

    setStoreData(res) {
      this.storeData = res.data
    },

    setGroceryData(res) {
      this.groceryData = res.data
    },

    addToGroceryData(res) {
      this.groceryData.items.push(res.data)
    },

    flashSomeKindOfError(e) {
      alert("Something failed:\n" + e + `\n${localStorage.token}`)
    },

    exposeGroceryForm() {
      this.display = ''
    }
  },

  created() {
    sessionStorage.blah = "Consider using session storage for token and user_id.\nThat might be deleted if you close your browser though.  Maybe useful for a remember_me feature."
    this.getGroceries()
  }
}
</script>
