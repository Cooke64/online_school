import React from "react";
import cls from "./CreatePollPage.module.css";
import { useParams } from "react-router-dom";
import BaseInput from "../../components/UI/BaseInput/BaseInput";
import Checkbox from "@mui/material/Checkbox";
import BaseButton from "../../components/UI/BaseButton/BaseButton";

export default function CreatePollPage() {
  const { lesson_id } = useParams();
  const [questionText, setQuestionText] = React.useState("");
  const [isQuestion, setIsQuestion] = React.useState(true);
  const [answers, setAnswers] = React.useState([
    {
      answer_text: "",
      is_correct: false,
    },
  ]);
  const onClickHandler = (e) => {
    e.preventDefault();
    setIsQuestion(false);
  };

  const addAnotherAnswer = (e) => {
    e.preventDefault();
    let newAnswer = { answer_text: "", is_correct: false };
    setAnswers([...answers, newAnswer]);
  };

  const handleFormChange = (index, event) => {
    let data = [...answers];
    console.log(event.target.type);
    if (event.target.type === "checkbox") {
      data[index][event.target.name] = event.target.checked;
    } else {
      data[index][event.target.name] = event.target.value;
    }
    setAnswers(data);
  };

  const addPoll = (e) => {
    e.preventDefault();
    console.log({
      answers_list: answers,
    });
  };

  const removeFields = (index) => {
    let data = [...answers];
    data.splice(index, 1)
    setAnswers(data)
  }

  return (
    <section>
      <h1 className="section_header">Добавить опрос к уроку</h1>
      {isQuestion ? (
        <form>
          <p>Добавить вопрос тесту</p>
          <BaseInput
            type="text"
            placeholder="Введи вопрос"
            className={cls.box}
            onChange={(e) => setQuestionText(e.target.value)}
          />

          <BaseButton className="btn_block" onClick={onClickHandler}>
            Добавить название
          </BaseButton>
        </form>
      ) : (
        <div>
          <form>
            {answers.map((answer, index) => (
              <div className={cls.answer_item} key={index}>
                <p>Добавить вопрос тесту</p>
                <BaseInput
                  type="text"
                  placeholder="Введи вопрос"
                  name="answer_text"
                  className={cls.box}
                  value={answer.answer_text}
                  onChange={(event) => handleFormChange(index, event)}
                />
                <p>Правильный ответ</p>
                <input
                  type="checkbox"
                  onChange={(event) => handleFormChange(index, event)}
                  checked={answer.is_correct}
                  name="is_correct"
                ></input>
                <div>
                  <BaseButton className="btn_red" onClick={() => removeFields(index)}>Удалить вопрос</BaseButton>
                </div>
                <hr/>
              </div>
              
            ))}
            <BaseButton className="btn_block" onClick={addAnotherAnswer}>
              Добавить еще
            </BaseButton>
            <BaseButton className="btn_block" onClick={addPoll}>
              Добавить опрос
            </BaseButton>
          </form>
        </div>
      )}
    </section>
  );
}
