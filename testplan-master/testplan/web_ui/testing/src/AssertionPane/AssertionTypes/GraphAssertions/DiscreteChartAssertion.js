import React, {Component} from 'react';
import PropTypes from 'prop-types';
import 'react-vis/dist/style.css';
import * as GraphUtil from './graphUtils';
import {
  RadialChart,
  Hint,
  DiscreteColorLegend
} from 'react-vis';

/**
 * Component that are used to render a Chart (Data visualisations that don't
 * require an XY axis). Class currently only will render radial charts
 * correctly (not generalised for other charts).
 */
class DiscreteChartAssertion extends Component  {
  components = {
    Pie: RadialChart
   }

  state = {
    value: null
  };

  render(){
    let data = this.props.assertion.graph_data;
    const graph_type = this.props.assertion.graph_type;
    const GraphComponent = this.components[graph_type];
    const series_options = this.props.assertion.series_options;
    let series_colours = GraphUtil.returnColour(series_options, data);
    let plots = [];
    let legend = [];

    for (let key in data) {
        plots.push(
           <GraphComponent
            colorType={series_colours[key]}
            key={key}
            data={data[key]}
            width={400}
            height={300}
            onValueMouseOver={v => this.setState(
                                  {value: {'Label': v.name}}
                                  )}
            onSeriesMouseOut={v => this.setState({value: null})}
            >
            {this.state.value !== null
             && <Hint value={this.state.value}/>}
           </GraphComponent>
         );

        legend = data[key].map( slice => {
                    return {title: slice.name, color: slice.color};
                 });
       }

      return (
       <div>
          {plots}
          <DiscreteColorLegend
            orientation='horizontal'
            width={750}
            items={legend}
          />
          <br/>
          <p>(Hover over chart to see labels)</p>
       </div>
     );
  }
}
DiscreteChartAssertion.propTypes = {
  /** Assertion being rendered */
  assertion: PropTypes.object,
};


export default DiscreteChartAssertion;
