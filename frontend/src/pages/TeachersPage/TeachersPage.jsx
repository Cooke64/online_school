import React from "react";
import Input from "../../components/UI/BaseInput/Input";
import cls from "./TeachersPage.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import ButtonAsLink from "../../components/UI/ButtonAsLink/ButtonAsLink";
import CourseBase from "../../img/course_base.png";

const TeacherItem = ({ teacher_data }) => {
  return (
    <>
      <div className={cls.box}>
        <div className={cls.teacher}>
          <img src={CourseBase} alt="about_pic" />
          <div>
            <h3>Teacher name</h3>
            <span>
              Lorem ipsum dolor sit amet consectetur adipisicing elit.
              Reprehenderit harum quos nostrum.
            </span>
          </div>
        </div>
        <p>
          Course <span>Amount of courses</span>
        </p>
        <p>
          Total comments <span>Amount of comments</span>
        </p>
        <p>
          Total rating courses <span>Total rating</span>
        </p>
        <ButtonAsLink
          href="/teachers/1/profile"
          button_type="inline"
          btn_action="click"
        >
          Перейти на страничку
        </ButtonAsLink>
      </div>
    </>
  );
};

export default function TeachersPage() {
  return (
    <section>
      <h1 className="section_header">преподаватели</h1>
      <div className={cls.search_teacher}>
        <Input required placeholder="Поиск преподавателя" />
        <button>
          <FontAwesomeIcon icon={faSearch} className={cls.side_icon} />
        </button>
      </div>

      <div className={cls.box_container}>
        <div className={[cls.box, cls.offer].join(" ")}>
          <h3>Стать преподавателем</h3>
          <p>
            Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quia, eum.
            Laborum saepe itaque omnis beatae similique magnam delectus tenetur.
            Ipsa eligendi explicabo doloremque iure saepe corporis recusandae
            architecto maxime neque?
          </p>
          <ButtonAsLink
            href="/register"
            button_type="inline"
            btn_action="click"
          >
            зарегестрироваться
          </ButtonAsLink>
        </div>
        <TeacherItem />
        <TeacherItem />
        <TeacherItem />
      </div>
    </section>
  );
}
