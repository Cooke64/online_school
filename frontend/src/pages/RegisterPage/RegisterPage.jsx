import React from "react";
import cls from "./RegisterPage.module.css";
import ButtonAsLink from "../../components/UI/ButtonAsLink/ButtonAsLink";
export default function RegisterPage() {
  return (
    <section>
      <h1 className="section_header">Страничка регистрации</h1>
      <form action="" method="post">
        <h3>Обновить профиль</h3>
        <p>Имя</p>
        <input type="text" placeholder="Ddtlbnt bvz" className={cls.box} />
        <p>Емайл</p>
        <input type="text" placeholder="Ddtlbnt bvz" className={cls.box} />
        <p>Пароль</p>
        <input type="text" placeholder="Ddtlbnt bvz" className={cls.box} />
        <p>Подтвердите пароль</p>
        <input type="text" placeholder="Ddtlbnt bvz" className={cls.box} />
        <p>Обновить аву</p>
        <input type="file" name="" accept="image/*" className={cls.box} />
        <ButtonAsLink button_type="inline" btn_action="click">
          Обновить
        </ButtonAsLink>
      </form>
    </section>
  );
}
