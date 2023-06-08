import React from "react";
import BaseButton from "../../components/UI/BaseButton/BaseButton";
import cls from "./Poll.module.css";
export default function PollItem({ question, handlerAnswer }) {
  return (
    <div className={cls.box}>
      <div className={cls.teacher}>
        <div>
          <h3>{question.question_text}</h3>
          {question.answers_list.map((answer) => (
            <div className={cls.statistic} key={answer.id}>
              <BaseButton className={"btn_inline"} onClick={() => handlerAnswer(answer)}>
                {answer.answer_text}
              </BaseButton>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
