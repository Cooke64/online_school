import React from "react";
import cls from "./ContactUs.module.css";
import CourseBase from "../../img/course_base.png";
import { InputBase } from "@mui/material";
import Input from "../../components/UI/BaseInput/Input";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBookBookmark,
  faCalendar,
  faEnvelope,
  faMapMarkedAlt,
  faPhone,
} from "@fortawesome/free-solid-svg-icons";

export default function ContactUs() {
  return (
    <section>
      <div className={cls.row}>
        <div className={cls.contact_image}>
          <img src={CourseBase} alt="about_pic" />
        </div>
        <form action="" method="post">
          <h3>Будем на связи!</h3>
          <Input
            type="text"
            placeholder="Введите ваше имя"
            className={cls.box}
            required
          />
          <Input
            type="text"
            placeholder="Введите ваше email"
            className={cls.box}
            required
          />
          <textarea
            type="text"
            placeholder="Введите ваше сообщение"
            className={cls.box}
            required
          />
          <input type="submit" value="Отправить" className={cls.dubmit_btn} />
        </form>
      </div>

      <div className={cls.box_container}>
        <div className={cls.box}>
          <FontAwesomeIcon icon={faPhone} className={cls.save_icon} />
          <h3>Телефоны</h3>
          <a href="tel:+89999999999">89999999999</a>
          <a href="tel:+89999999999">89999999999</a>
        </div>
        <div className={cls.box}>
          <FontAwesomeIcon icon={faEnvelope} className={cls.save_icon} />
          <h3>Почта</h3>
          <a href="mailto:a@mail.ru">a@mail.ru</a>
          <a href="mailto:a@mail.ru">a@mail.ru</a>
        </div>
        <div className={cls.box}>
          <FontAwesomeIcon icon={faMapMarkedAlt} className={cls.save_icon} />
          <h3>Геолокация</h3>
          <a href="/">  addressaddressaddressaddressaddressaddress</a>
          <a href="/">  addressaddressaddressaddressaddressaddress</a>
        </div>
      </div>
    </section>
  );
}
