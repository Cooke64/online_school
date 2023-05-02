import React from 'react'
import cls from "./BaseInput.module.css";

export default function BaseInput(props) {
  return (
    <input {...props} className={cls.input}/>

  )
}