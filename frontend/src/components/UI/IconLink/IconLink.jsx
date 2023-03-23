import React from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'


export default function IconLink({link, icon}) {
  return (
    <a href={link}>
        <FontAwesomeIcon icon={icon} className="icon" />
    </a>
    
  )
}
