import React from "react";
import cls from "./BaseButton.module.css";
export default function BaseButton({ children, ...props }) {
  return (
    <button {...props} className={[cls.btn, props.className].join(" ")}>
      {children}
    </button>
  );
}
