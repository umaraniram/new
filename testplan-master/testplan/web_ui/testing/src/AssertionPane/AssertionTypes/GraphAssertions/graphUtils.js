/**
 * Helper functions used to add customisation and styling to the graph and
 * chart assertions.
 */

/**
 * Return the JSX for the 'style' parameter for the graph component
 * to help render nicer graphs, not currently set by the user
 *
 * @param {str} graph_type - The type of graph being rendered
 * @return {dict[key: object]} Returns any style required for the graph
 */
export function returnStyle(graph_type){
  if(graph_type === 'Contour'){
     return(
        {
            stroke: '#125C77',
            strokeLinejoin: 'round'
        }
      );
  }
}

/**
 * Return the JSX for the 'XType' parameter for the XYPlot
 * component to be make the x axis increment either numerical or ordinal
 *
 * @param {str} graph_type - The type of graph being rendered
 * @return {str} Returns ordinal if x-axis should be
 *               letters instead of numerical
 */
export function returnXType(graph_type){
  if(graph_type ==='Bar'){
    return("ordinal");
  }
}

const COLOUR_PALETTE=['#1c5c9c', '#68caea', '#7448c5', '#633836',
                      '#485051', '#336a85', '#94b1c5', '#ababab'];
/**
 * Return the colours for every series, given the series_options. Each series'
 * colour assigned depending on whether the user has specified an option,
 * otherwise return from a colour scheme/palette, then random colours
 * (tinted darker/blue)
 *
 * @param {dict[str, dict[str, object]]} series_options - dictionary with
 *                                       series name and user specified options
 * @param {dict[str, list]} data - every data series name along
 *                                 with the relative list of data
 * @return {dict[str, str]} Every series name and it's display colour
 */
export function returnColour(series_options, data){
  const series_names = Object.keys(data);
  let series_colours = {};
  let colour_options = COLOUR_PALETTE.slice();

  series_names.forEach(function(series) {
    //Assign colour from user specified options if possible
    if(series_options != null){
      if(series_options[series]!= null){
        if(series_options[series].colour!= null){
          series_colours[series] =
            series_options[series].colour;
          return;
        }
      }
    }

    //Otherwise choose next colour available from colour palette
    if(colour_options.length !== 0){
       let colour = colour_options[0];
       series_colours[series] = colour;
       colour_options.shift();

    //Otherwise if no more available colours, choose random colour
    } else {
      let colour = '';
      for (let i = 0; i < 4; i++) {
       colour += (Math.round(Math.random() * 15)).toString(16);
      }
      for (let i = 0; i < 2; i++) {
       colour += (10+ Math.round(Math.random() * 5)).toString(16);
      }
      series_colours[series] = colour;
    }
  });

  return series_colours;
}

/**
 * Return an xAxisTitle for the graph component
 * or nothing if it has not been set
 *
 * @param {dict[str: object]} graph_options - user specified options
 *                                            for the entire graph
 *
 * @return {str/null} The axis title, or null if not set
 */
export function returnXAxisTitle(graph_options){
  if(graph_options == null){
    return;
  }
  if(graph_options.xAxisTitle !== null){
    return graph_options.xAxisTitle;
  }
}

/**
 * Return an yAxisTitle for the graph component
 * or nothing if it has not been set
 * @param {dict[str: object]} graph_options - user specified options
 *                                            for the entire graph
 *
 * @return {str/null} The axis title, or null if not set
 */
export function returnYAxisTitle(graph_options){
  if(graph_options == null){
    return;
  }
  if(graph_options.yAxisTitle !== null){
    return graph_options.yAxisTitle;
  }
}
