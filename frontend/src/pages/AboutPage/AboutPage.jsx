import React from "react";
import cls from "./AboutPage.module.css";
import CourseBase from "../../img/course_base.png";
import ButtonAsLink from "../../components/UI/ButtonAsLink/ButtonAsLink";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGraduationCap } from "@fortawesome/free-solid-svg-icons";

export default function AboutPage() {
  return (
    <section>
      <div className={cls.row}>
        <div className={cls.about_img}>
          <img src={CourseBase} alt="about_pic" />
        </div>
        <div className={cls.content}>
          <h3>Почему стоит выбрать нас</h3>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Totam quasi
            autem exercitationem a ipsum eveniet minima. Pariatur aspernatur
            inventore nam explicabo consequuntur accusamus ab, non recusandae
            vitae, quis, tempore in.
          </p>
          <ButtonAsLink href="/" button_type="inline" btn_action="click">
            Наши курсы
          </ButtonAsLink>
        </div>
      </div>
      <div className={cls.box_container}>
        {/*  */}
        <div className={cls.box}>
          <FontAwesomeIcon icon={faGraduationCap} className={cls.icon} />
          <div>
            <h3>Более 5 курсов!</h3>
            <span>Бесплатных</span>
          </div>
        </div>
        {/*  */}
        <div className={cls.box}>
          <FontAwesomeIcon icon={faGraduationCap} className={cls.icon} />
          <div>
            <h3>Более 5 курсов!</h3>
            <span>Бесплатных</span>
          </div>
        </div>
        {/*  */}
        <div className={cls.box}>
          <FontAwesomeIcon icon={faGraduationCap} className={cls.icon} />
          <div>
            <h3>Более 5 курсов!</h3>
            <span>Бесплатных</span>
          </div>
        </div>

      </div>
    </section>
  );
}
