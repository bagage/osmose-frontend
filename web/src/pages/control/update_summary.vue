<template>
  <div>
    <vue-topprogress ref="topProgress"></vue-topprogress>
    <div v-if="error">{{ error }}</div>
    <table
      v-else
      class="table table-striped table-bordered table-hover table-sm"
    >
      <template v-for="remote in remote_keys">
        <thead :key="'h' + remote" class="thead-dark">
          <tr>
            <th>
              <router-link :to="`update_matrix?remote=${remote}`">
                {{ hostnames[remote] || remote }}
              </router-link>
              ({{ min_versions[remote] }} - {{ max_versions[remote] }})
            </th>
          </tr>
        </thead>
        <tbody :key="'b' + remote">
          <tr>
            <td>
              <span
                is="delay"
                v-for="country in summary[remote]"
                :key="country.country"
                :v="country.min_age"
                :opacity="opacity(country.count, max_count)"
              >
                <router-link
                  :to="`../errors/?country=${country.country}&item=xxxx`"
                  >{{ country.country }}</router-link
                ><sup>{{ country.count }}</sup
                >&nbsp;{{ country.min_age | numFormat("0.0") }}-<span
                  is="delay"
                  :v="country.max_age"
                  :opacity="opacity(country.count, max_count)"
                  >{{ country.max_age | numFormat("0.0") }}
                </span>
              </span>
            </td>
          </tr>
        </tbody>
      </template>
    </table>
  </div>
</template>

<script>
import VueParent from "../Parent.vue";
import Delay from "../../components/delay.vue";

export default VueParent.extend({
  data() {
    return {
      error: false,
      remote_keys: null,
    };
  },
  components: {
    Delay,
  },
  mounted() {
    this.fetchJsonProgressAssign(
      API_URL + window.location.pathname + ".json" + window.location.search
    );
    document.title = "Osmose - " + this.$t("Updates summary");
  },
  methods: {
    opacity(count, max) {
      return (0.66 * count) / max + 0.33;
    },
  },
});
</script>
