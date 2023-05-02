import React from "react";
import Input from "../../components/UI/BaseInput/BaseInput";
import cls from "./TeachersPage.module.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import ButtonAsLink from "../../components/UI/ButtonAsLink/ButtonAsLink";
import CourseBase from "../../img/course_base.png";
import api from "../../api/api";

const TeacherItem = ({ teacher_data }) => {
    let link = `/teacher/${teacher_data.teacher_info.id}`
  return (
    <>
      <div className={cls.box}>
        <div className={cls.teacher}>
          <img src={CourseBase} alt="about_pic" />
          <div>
            <h3>{teacher_data.teacher_info.username}</h3>
            <span>
            {teacher_data.teacher_info.description}
              Lorem ipsum dolor sit amet consectetur adipisicing elit.
              Reprehenderit harum quos nostrum.
            </span>
          </div>
        </div>
        <div className={cls.statistic}>
          <p>
            Всего курсов: <span>{teacher_data.count_courses}</span>
          </p>
          <p>
            Всего комментариев: <span>{teacher_data.total_reviews}</span>
          </p>
          <p>
            Общий рейтинг: <span>{teacher_data.total_rating}</span>
          </p>
        </div>

        <ButtonAsLink
          href={link}
          button_type="inline"
          btn_action="click"
          className={cls.button_teacher}
        >
          Перейти на страничку
        </ButtonAsLink>
      </div>
    </>
  );
};

export default function TeachersPage() {
    const [teachersList, setTeachersList] = React.useState([])


  React.useEffect(()=> {
    api.getTeachersList().then((res) => {
        setTeachersList(res);
        console.log(res)
      });
  }, [])
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
        {teachersList.map((teacher) => (
          <TeacherItem
            teacher_data={teacher}
          />
        ))}
      </div>
    </section>
  );
}
