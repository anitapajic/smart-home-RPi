import React from 'react';

const GrafanaPanel = () => {
  const grafanaUrl = "http://localhost:3000/d/a144c6c1-3619-4fc7-9881-3a2e06fb2891/dht?orgId=1&from=1703805690891&to=1703809290891&viewPanel=2"; // Replace with your Grafana iframe URL

  return (
    <iframe
      src={grafanaUrl}
      width="800px"
      height="500px"
      frameBorder="0"
    ></iframe>
  );
};

export default GrafanaPanel;
