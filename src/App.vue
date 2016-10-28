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
                :fill="state === highlightedState ? '#66bb6a' : '#ccc'"
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
                <h4>
                  {{ highlightedCounty ? highlightedCounty.name : '&nbsp;' }}
                </h4>
                <svg
                  id="selected-state-svg"
                  :height="selectedStateSvgHeight"
                  v-on:mouseover.stop="unhighlightCounty"
                >
                  <g :transform="selectedStateTransform">
                    <g v-for="county in selectedState.counties">
                      <path
                        class="county"
                        :d="county.path"
                        :fill="county === highlightedCounty ? '#4caf50' : '#a5d6a7'"
                        v-on:mouseover.stop="highlightCounty(county)"
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
      highlightedCounty: null,
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
      const svgWidthAndHeight = 800
      const padding = 50
      const maxWidthOrHeight = svgWidthAndHeight - 2 * padding
      const scale = maxWidthOrHeight / Math.max(height, width)
      const xPadding = (svgWidthAndHeight - scale * width) / 2
      const yPadding = padding
      const translateX = -left + xPadding / scale
      const translateY = -top + yPadding / scale
      this.selectedStateSvgHeight = height * scale + yPadding * 2
      return `scale(${scale}, ${scale}) translate(${translateX}, ${translateY})`
    }
  },
  methods: {
    highlightCounty (county) {
      this.highlightedCounty = county
    },
    highlightState (state) {
      this.highlightedState = state
    },
    selectState (state) {
      this.selectedState = state
      this.unhighlightCounty()
    },
    unhighlightCounty () {
      this.highlightedCounty = null
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
