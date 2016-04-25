  AGENT_FREQUENCY = document.getElementById('agent_frequency');
  chart_data.type = 'bar';
  Plotly.plot( AGENT_FREQUENCY, [chart_data], {margin: { t: 0 } } );