import React from 'react'
import cls from "./BaseButton.module.css";
export default function BaseButton({children, ...props}) {
  return (
    <button {...props} className={[props.className, cls.btn].join(' ')}>
        {children}
    </button>
  )
}
