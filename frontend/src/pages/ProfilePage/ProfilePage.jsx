import React from "react";
import cls from "./ProfilePage.module.css";
import CourseBase from "../../img/course_base.png";
import ButtonAsLink from "../../components/UI/ButtonAsLink/ButtonAsLink";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBookReader,
  faComment,
  faHeart,
} from "@fortawesome/free-solid-svg-icons";
export default function ProfilePage() {
  return (
    <section>
      <h1 className="section_header">Страничка профиля</h1>

      <div className={cls.details}>
        <div className={cls.user}>
          <img src={CourseBase} alt="about_pic" />
          <h3>Username</h3>
          <p>Status</p>
          <ButtonAsLink to={`/update_profile`}>Редактировать</ButtonAsLink>
        </div>

        <div className={cls.container}>
          <div className={cls.box}>
            <div className={cls.flex}>
              <FontAwesomeIcon icon={faBookReader} className={cls.save_icon} />
              <div>
                <h3>33</h3>
                <span>пройденных урока</span>
              </div>
            </div>
            <ButtonAsLink button_type="inline" btn_action="click">
              Смотреть уроки
            </ButtonAsLink>
          </div>

          <div className={cls.box}>
            <div className={cls.flex}>
              <FontAwesomeIcon icon={faHeart} className={cls.save_icon} />
              <div>
                <h3>33</h3>
                <span>понравившиеся уроки</span>
              </div>
            </div>
            <ButtonAsLink button_type="inline" btn_action="click">
              Смотреть уроки
            </ButtonAsLink>
          </div>

          <div className={cls.box}>
            <div className={cls.flex}>
              <FontAwesomeIcon icon={faComment} className={cls.save_icon} />
              <div>
                <h3>44</h3>
                <span>комментариев</span>
              </div>
            </div>
            <ButtonAsLink button_type="inline" btn_action="click">
              Смотреть комментарии
            </ButtonAsLink>
          </div>
        </div>
      </div>
    </section>
  );
}
