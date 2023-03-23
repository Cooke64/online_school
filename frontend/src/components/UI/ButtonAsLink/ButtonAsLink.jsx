import React from "react";
import "./ButtonAsLink.css";

export default function ButtonAsLink({ children, ...props }) {
  // Выбор кнопки действия, которое может совершить пользователь и стиля отображения
  const button_type = props.button_type
  const btn_action = props.btn_action
  let style = 'my_btn'
  if (btn_action === 'option') {
    style += ' option_bg'
  }
  else if (btn_action === 'delete') {
    style += ' delete_bg'
  } else {
    style += ' main_bg'
  }

  if (button_type === 'inline') {
    style += ' inline_style'
  }
  else {
    style += ' block_style'
  }
  return (
      <a {...props} className={style}>
        {children}
      </a>
  );
}

