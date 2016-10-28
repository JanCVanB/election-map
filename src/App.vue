<template>
  <div id="app" class="container">
    <div class="row">

      <div class="col s12" style="text-align: center;">
        <h4>
          Click on a state
        </h4>
        <svg
          id="counties-svg"
          v-on:click.stop="unselectState"
          v-on:mouseover.stop="unhighlightState"
        >
          <g
            v-for="state in states"
            v-on:click.stop="selectState(state)"
            v-on:mouseover.stop="highlightState(state)"
          >
            <g v-for="county in state.counties">
              <path
                class="county"
                :d="county.path"
                :fill="state === highlightedState ? '#4caf50' : '#ccc'"
              />
            </g>
          </g>
        </svg>
      </div>

      <transition
        name="custom-classes-transition"
        mode="out-in"
        enter-active-class="animated fadeInUp"
        leave-active-class="animated fadeOutDown"
      >
        <template v-if="selectedState">
          <div class="col s12" style="text-align: center;">
            <div class="card green lighten-3">
              <div class="card-content">
                <h2>
                  {{ selectedState.name }}
                </h2>
                <svg id="selected-state-svg" :height="selectedStateSvgHeight">
                  <g :transform="selectedStateTransform">
                    <g v-for="county in selectedState.counties">
                      <path
                        class="county"
                        :d="county.path"
                        fill="none"
                      />
                    </g>
                  </g>
                </svg>
              </div>
            </div>
          </div>
        </template>
      </transition>

    </div>
  </div>
</template>

<script>
const _ = require('underscore')
const counties = require('./data/counties.json').counties
const countiesByState = _.groupBy(counties, county => county.stateId)
const stateIds = _.sortBy(Object.keys(countiesByState), key => key)
const stateNames = {
  '01': 'Alabama',
  '02': 'Alaska',
  '04': 'Arizona',
  '05': 'Arkansas',
  '06': 'California',
  '08': 'Colorado',
  '09': 'Connecticut',
  '10': 'Delaware',
  '12': 'Florida',
  '13': 'Georgia',
  '15': 'Hawaii',
  '16': 'Idaho',
  '17': 'Illinois',
  '18': 'Indiana',
  '19': 'Iowa',
  '20': 'Kansas',
  '21': 'Kentucky',
  '22': 'Louisiana',
  '23': 'Maine',
  '24': 'Maryland',
  '25': 'Massachusetts',
  '26': 'Michigan',
  '27': 'Minnesota',
  '28': 'Mississippi',
  '29': 'Missouri',
  '30': 'Montana',
  '31': 'Nebraska',
  '32': 'Nevada',
  '33': 'New Hampshire',
  '34': 'New Jersey',
  '35': 'New Mexico',
  '36': 'New York',
  '37': 'North Carolina',
  '38': 'North Dakota',
  '39': 'Ohio',
  '40': 'Oklahoma',
  '41': 'Oregon',
  '42': 'Pennsylvania',
  '44': 'Rhode Island',
  '45': 'South Carolina',
  '46': 'South Dakota',
  '47': 'Tennessee',
  '48': 'Texas',
  '49': 'Utah',
  '50': 'Vermont',
  '51': 'Virginia',
  '53': 'Washington',
  '54': 'West Virginia',
  '55': 'Wisconsin',
  '56': 'Wyoming',
  '72': 'Puerto Rico'
}
const states = stateIds.map(stateId => (
  {
    id: stateId,
    name: stateNames[stateId],
    counties: countiesByState[stateId]
  }
))

export default {
  name: 'app',
  data () {
    return {
      highlightedState: null,
      selectedState: null,
      selectedStateSvgHeight: null,
      states
    }
  },
  computed: {
    selectedStateTransform () {
      let xCoordinates = []
      let yCoordinates = []
      const coordinateRegex = /(-?[0-9\.]+),\s*(-?[0-9\.]+)/g
      let coordinateMatch
      this.selectedState.counties.forEach(county => {
        while (coordinateMatch = coordinateRegex.exec(county.path)) {
          xCoordinates.push(parseFloat(coordinateMatch[1]));
          yCoordinates.push(parseFloat(coordinateMatch[2]));
        }
      })
      const left = _.min(xCoordinates)
      const top = _.min(yCoordinates)
      const width = _.max(xCoordinates) - _.min(xCoordinates)
      const height = _.max(yCoordinates) - _.min(yCoordinates)
      const center_x = (_.min(xCoordinates) + _.max(xCoordinates)) / 2
      const center_y = (_.min(yCoordinates) + _.max(yCoordinates)) / 2
      const scale_x = 800 / width
      const scale_y = scale_x
      const translate_x = -left
      const translate_y = -top
      this.selectedStateSvgHeight = height * scale_y
      console.log(height * scale_y);
      return `scale(${scale_x}, ${scale_y}) translate(${translate_x}, ${translate_y})`
    }
  },
  methods: {
    highlightState (state) {
      this.highlightedState = state
    },
    selectState (state) {
      this.selectedState = state
    },
    unhighlightState () {
      this.highlightedState = null
    },
    unselectState () {
      this.selectedState = null
    }
  },
  mounted () {
    new Vivus('counties-svg', {
      duration: 150,
      type: 'delayed'
    })
  }
}
</script>

<style>
#counties-svg {
  height: 500px;
  width: 800px;
}

#selected-state-svg {
  width: 800px;
}

.county {
  stroke: white;
  stroke-width: 0.5;
}
</style>
