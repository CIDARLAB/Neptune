<template>
  <v-container
    id="wizard"
    tag="section"
  >
    <validation-observer v-slot="{ valid }">
      <base-material-wizard
        v-model="tab"
        :available-steps="availableSteps"
        :items="tabs"
        class="mx-auto"
        @click:next="next(valid)"
        @click:prev="tab--"
      >
        <v-tab-item class="pb-12">
          <form>
            <div class="text-center display-1 font-weight-light mb-6">
              Let's start with basic information (with validation)
            </div>

            <v-row
              class="mx-auto"
              justify="space-around"
              style="max-width: 500px;"
            >
              <v-col
                cols="auto"
                class="text-center"
              >
                <input
                  ref="file"
                  type="file"
                  class="d-none"
                  @change="onChange"
                >
                <v-card
                  :class="image ? 'success--text' : 'grey--text'"
                  class="mx-auto mt-0 d-inline-flex v-card--account"
                  outlined
                  height="106"
                  width="106"
                  @click="$refs.file.click()"
                >
                  <v-img
                    v-if="image"
                    :src="image"
                    height="100%"
                    width="100%"
                  />
                  <v-icon
                    v-else
                    class="mx-auto"
                    size="96"
                  >
                    mdi-account
                  </v-icon>
                </v-card>

                <div class="font-weight-bold grey--text">
                  CHOOSE PICTURE
                </div>
              </v-col>

              <v-col
                cols="12"
                md="6"
              >
                <validation-provider
                  v-slot="{ errors }"
                  rules="required"
                  name="first"
                >
                  <v-text-field
                    v-model="first"
                    :error-messages="errors"
                    color="secondary"
                    label="First Name*"
                    prepend-icon="mdi-face"
                    validate-on-blur
                  />
                </validation-provider>

                <validation-provider
                  v-slot="{ errors }"
                  rules="required"
                  name="last"
                >
                  <v-text-field
                    v-model="last"
                    :error-messages="errors"
                    color="secondary"
                    label="Last Name*"
                    prepend-icon="mdi-account"
                    validate-on-blur
                  />
                </validation-provider>
              </v-col>

              <v-col cols="12">
                <validation-provider
                  v-slot="{ errors }"
                  rules="required"
                  name="email"
                >
                  <v-text-field
                    v-model="email"
                    :error-messages="errors"
                    color="secondary"
                    label="Email*"
                    prepend-icon="mdi-email"
                    validate-on-blur
                  />
                </validation-provider>
              </v-col>
            </v-row>
          </form>
        </v-tab-item>

        <v-tab-item class="pb-12">
          <form>
            <v-responsive
              class="mx-auto"

              max-width="500"
            >
              <div class="text-center display-1 grey--text font-weight-light mb-6">
                What are you doing? (checkboxes)
              </div>

              <validation-provider
                rules="required"
                name="type"
              >
                <input
                  :value="stringAccount"
                  type="hidden"
                >
              </validation-provider>

              <v-item-group
                v-model="account"
                class="row"
                multiple
              >
                <v-item
                  v-for="(account, i) in accounts"
                  :key="i"
                >
                  <template v-slot="{ active, toggle }">
                    <v-col
                      class="text-center"
                      cols="4"
                    >
                      <v-card
                        :class="active ? 'success--text' : 'grey--text'"
                        class="mb-6 mx-auto pa-10 d-inline-block v-card--account"
                        outlined
                        @click="toggle"
                      >
                        <v-icon
                          large
                          v-text="account.icon"
                        />
                      </v-card>

                      <div
                        class="text-uppercase subtitle-2 text--primary"
                        v-text="account.type"
                      />
                    </v-col>
                  </template>
                </v-item>
              </v-item-group>
            </v-responsive>
          </form>
        </v-tab-item>

        <v-tab-item class="pb-12">
          <div class="text-center display-1 grey--text font-weight-light mb-6">
            Are you living in a nice area?
          </div>

          <form>
            <v-row
              class="mx-auto"
              justify="space-around"
              style="max-width: 500px;"
            >
              <v-col
                cols="12"
                md="8"
              >
                <validation-provider
                  v-slot="{ errors }"
                  rules="required"
                  name="address"
                >
                  <v-text-field
                    v-model="address"
                    :error-messages="errors"
                    color="secondary"
                    label="Street Name*"
                    validate-on-blur
                  />
                </validation-provider>
              </v-col>

              <v-col
                cols="12"
                md="4"
              >
                <validation-provider
                  v-slot="{ errors }"
                  rules="required"
                  name="street"
                >
                  <v-text-field
                    v-model="street"
                    :error-messages="errors"
                    color="secondary"
                    label="Street Number*"
                    validate-on-blur
                  />
                </validation-provider>
              </v-col>

              <v-col
                cols="12"
                md="6"
              >
                <validation-provider
                  v-slot="{ errors }"
                  rules="required"
                  name="city"
                >
                  <v-text-field
                    v-model="city"
                    :error-messages="errors"
                    color="secondary"
                    label="City*"
                    validate-on-blur
                  />
                </validation-provider>
              </v-col>

              <v-col
                cols="12"
                md="6"
              >
                <validation-provider
                  v-slot="{ errors }"
                  rules="required"
                  name="state"
                >
                  <v-autocomplete
                    v-model="state"
                    :autocomplete="Date.now()"
                    :error-messages="errors"
                    :items="states"
                    color="secondary"
                    label="State*"
                    validate-on-blur
                  />
                </validation-provider>
              </v-col>
            </v-row>
          </form>
        </v-tab-item>
      </base-material-wizard>
    </validation-observer>
  </v-container>
</template>

<script>
  export default {
    name: 'DashboardFormsWizard',

    data: () => ({
      account: [],
      accounts: [
        {
          icon: 'mdi-pencil',
          type: 'design',
        },
        {
          icon: 'mdi-code-tags',
          type: 'code',
        },
        {
          icon: 'mdi-laptop',
          type: 'develop',
        },
      ],
      address: '',
      city: '',
      email: '',
      first: '',
      image: null,
      last: '',
      state: '',
      states: [
        'Alabama', 'Alaska', 'American Samoa', 'Arizona',
        'Arkansas', 'California', 'Colorado', 'Connecticut',
        'Delaware', 'District of Columbia', 'Federated States of Micronesia',
        'Florida', 'Georgia', 'Guam', 'Hawaii', 'Idaho',
        'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
        'Louisiana', 'Maine', 'Marshall Islands', 'Maryland',
        'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
        'Missouri', 'Montana', 'Nebraska', 'Nevada',
        'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
        'North Carolina', 'North Dakota', 'Northern Mariana Islands', 'Ohio',
        'Oklahoma', 'Oregon', 'Palau', 'Pennsylvania', 'Puerto Rico',
        'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
        'Texas', 'Utah', 'Vermont', 'Virgin Island', 'Virginia',
        'Washington', 'West Virginia', 'Wisconsin', 'Wyoming',
      ],
      street: '',
      tab: 0,
      tabs: ['About', 'Account', 'Address'],
    }),

    computed: {
      stringAccount () {
        return this.account.join(',')
      },
      scope () {
        if (this.tab === 0) return 'about'
        else if (this.tab === 2) return 'address'
        return 'account'
      },
      availableSteps () {
        const steps = [0]

        if (
          this.first &&
          this.last &&
          this.email
        ) steps.push(1)

        if (this.stringAccount && steps.includes(1)) steps.push(2)

        if (
          this.address &&
          this.street &&
          this.city &&
          this.state &&
          steps.includes(2)
        ) steps.push(3)

        return steps
      },
    },

    methods: {
      next (valid) {
        if (!valid) return

        if (this.tab === this.tabs.length - 1) {
          alert('Form finished')
        } else {
          this.tab++
        }
      },
      onChange (val) {
        const value = val.target.files[0]

        if (!value) return (this.image = null)

        this.image = URL.createObjectURL(value)
      },
    },
  }
</script>

<style lang="sass">
  .v-card.v-card.v-card--account
    border-color: currentColor
    border-width: 4px

    .v-icon
      color: inherit

  .v-card--account,
  .v-card--account:before
    border-radius: 50%

</style>
