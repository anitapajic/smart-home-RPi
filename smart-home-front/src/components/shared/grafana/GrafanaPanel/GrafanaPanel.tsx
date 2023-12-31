import React from 'react';
import { IFrameStyle } from './GrafanaPanel.styled';
export type GrafanaPanelProps = {
  url : string
}

export default function GrafanaPanel({url} : GrafanaPanelProps){
  return (
    <IFrameStyle src={url}/>
  );
}
