import React from "react";
import cls from "./QuickSection.module.css";
import ButtonAsLink from "../../../components/UI/ButtonAsLink/ButtonAsLink";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCamera,
  faCode,
  faVial,
  faVirus,
} from "@fortawesome/free-solid-svg-icons";
import IconLink from "../../../components/UI/IconLink/IconLink";

export default function QuickSection() {
  return (
    <section className={cls.quick_section}>
      <h1 className={cls.section_header}>quick options</h1>

      <div className={cls.container}>
        <div className={cls.box}>
          {/* Отображение всех алйков и комментариев. Нужна ли ссылка куда-то это вопрос */}
          <h3 className={cls.title}>Комментарии и лайки</h3>
          <p>
            Total likes: <span>14</span>
          </p>
          <ButtonAsLink
            href="index.html"
            button_type="inline"
            btn_action="click"
          >
            view likes
          </ButtonAsLink>
          <p>
            Total comments: <span>14</span>
          </p>
          <ButtonAsLink
            href="index.html"
            button_type="inline"
            btn_action="click"
          >
            view comments
          </ButtonAsLink>
          <p>
            Total comments: <span>14</span>
          </p>
          <ButtonAsLink
            href="index.html"
            button_type="inline"
            btn_action="click"
          >
            view comments
          </ButtonAsLink>
        </div>
        <div className={cls.box}>
          <h3 className={cls.title}>Категории</h3>
          {/* ОТображение групп. */}
          <div className={cls.flex}>
            <IconLink icon={faCamera} link={"index.html"} />
            <IconLink icon={faCode} link={"index.html"} />
            <IconLink icon={faVial} link={"index.html"} />
            <IconLink icon={faVirus} link={"index.html"} />
          </div>
        </div>
        <div className={cls.box}>
          <h3 className={cls.title}>Популярные записи</h3>
          {/* ОТображение групп. */}
          <div className={cls.flex}>
            <IconLink icon={faCamera} link={"index.html"} />
            <IconLink icon={faCode} link={"index.html"} />
            <IconLink icon={faVial} link={"index.html"} />
            <IconLink icon={faVirus} link={"index.html"} />
          </div>
        </div>

        {/* Секция стать преподавателем */}
        <div className={cls.box}>
          <div className={cls.tutor}>
            <h3 className={cls.title}>Стать преподавателем</h3>
            <p>Lorem ipsum dolor sit.</p>
            <ButtonAsLink
              href="index.html"
              button_type="inline"
              btn_action="click"
            >
              Стать преподавателем
            </ButtonAsLink>
          </div>
        </div>
      </div>
    </section>
  );
}
