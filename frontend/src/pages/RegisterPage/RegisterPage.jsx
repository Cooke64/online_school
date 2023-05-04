import React from "react";
import cls from "./RegisterPage.module.css";
import ButtonAsLink from "../../components/UI/ButtonAsLink/ButtonAsLink";
import BaseInput from "../../components/UI/BaseInput/BaseInput";
export default function RegisterPage() {
  return (
    <section>
      <h1 className="section_header">Страничка регистрации</h1>
      <form action="" method="post">
        <h3>Введите Ваши данные</h3>
        <p>username</p>
        <BaseInput type="text" placeholder="Ddtlbnt bvz" className={cls.box} />
        <p>first_name</p>
        <BaseInput type="text" placeholder="Ddtlbnt bvz" className={cls.box} />
        <p>last_name</p>
        <BaseInput type="text" placeholder="Ddtlbnt bvz" className={cls.box} />
        <p>email</p>
        <BaseInput type="text" placeholder="Ddtlbnt bvz" className={cls.box} />
        <p>password</p>
        <BaseInput type="password" placeholder="Ddtlbnt bvz" className={cls.box} />
        <p>phone</p>
        <BaseInput type="text" placeholder="Ddtlbnt bvz" className={cls.box} />
        <ButtonAsLink button_type="inline" btn_action="click">
          Зарегестрироваться
        </ButtonAsLink>
      </form>
    </section>
  );
}
