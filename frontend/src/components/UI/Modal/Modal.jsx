import React from "react";
import cls from "./Modal.module.css";
export default function Modal({ children, visible, setVisible }) {
  const modalStyle = [cls.modal];
  if (visible) {
    modalStyle.push(cls.active);
  }
  return (
    <div className={modalStyle.join(" ")} onClick={() => setVisible(false)}>
      <div className={cls.content} onClick={(e) => e.stopPropagation()}>{children}</div>
    </div>
  );
}
